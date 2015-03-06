'''
Peer Discovery Module

This module is responsible for detecting other peers on the local network that
it can communicate with.


MESSAGE TYPES:

discovery.peer_discovered: Peer Discovered
    Signifies that a new peer has been discovered
    
    This event tells us that a host has been detected on the network that uses 
    the same protocol.  This does not tell us whether or not we should trust the
    other host though.
    
discovery.peer_lost: Peer No Longer Reachable
    Signifies that a known peer is no longer reachable
    
    This event tells us that a peer that was announced reachable is no longer
    seen.
      
      
cron.request_timer: Request Timer
    Request a timer for the ping_for_peer event.


LISTENING FOR MESSAGES:
    
cron.ping_for_peer:
    Sends out discovery broadcast every so often

peer_connected:
    When a TCP connection is established with a peer, this module will start
    letting the active connection module track whether the peer is reachable or
    not.
    
    Also, this suppresses responses to discovery broadcasts from the connected
    peer as well.

peer_disconnected:
    Will begin watching for this node again.
    

'''
import gflags
import logging
from socket import socket
from socket import AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_BROADCAST
from IN import SO_REUSEADDR

from p2p_filesync.FileSyncContext import get_filesync_context

from msg_passing.app.MsgDrivenModule import MsgDrivenModule
from msg_passing.msgs.StartShutdownMsg import StartShutdownMsg
from msg_passing.GlobMsgPattern import GlobMsgPattern
from msg_passing.cron.CronMsg import CronMsg
from msg_passing.cron.TimerRequestMsg import TimerRequestMsg

from BroadcastMonitorThread import BroadcastMonitorThread

from DiscoveredPeer import DiscoveredPeer
from PeerIndex import PeerIndex
from UdpPeerPing import UdpPeerPing

from msgs.RemotePeerBroadcastMsg import RemotePeerBroadcastMsg
from msgs.PeerDiscoveredMsg import PeerDiscoveredMsg
from msgs.PeerLostMsg import PeerLostMsg

gflags.DEFINE_string(
    name = 'discovery_port',
    default = 30000,
    help = '''\
        Port to do host discovery on
        
        UDP packets will be broadcasted and received on this port to discover
        other peers on the network.
        ''')


class PeerDiscoveryMod(MsgDrivenModule):
    '''This module is responsible for detecting other peers'''
    
    PING_INTERVAL_SECS = 15
    
    # -- Module Setup ---------------------------------------------------------
    
    def __init__(self, broker):
        self.__context = get_filesync_context()
        self.__known_peers = PeerIndex()
        self.__log = logging.getLogger(self.__class__.__name__)

        # UDP Socket
        self.__sock = None
        self.__port = gflags.FLAGS.discovery_port

        super(PeerDiscoveryMod, self).__init__(broker, 'PeerDiscovery')


    def _thread_shutdown(self):
        self._send_broadcast_leaving()
        super(PeerDiscoveryMod, self)._thread_shutdown()


    def pre_module_run_init(self):
        '''Does setup for module inside thread execution'''
        
        # Ping for peers prompt
        msg_class = CronMsg.calc_msg_class('ping_for_peers')
        self.listen_for(GlobMsgPattern(msg_class), 'prc_ping_for_peers_msg')
        

    def run_module(self):
        '''Begin execution of module'''
        # Register ping_for_peers timer
        self.broker.dispatch(TimerRequestMsg(
            action='ping_for_peers',
            seconds=str(self.PING_INTERVAL_SECS)))
        
        # Build Socket
        self.__sock = self._build_socket()
        
        # Start monitor for remote peer broadcasts
        monitor = BroadcastMonitorThread(self.__sock, self.__port, self)
        self.start_monitor_thread(monitor)
        self.listen_for(RemotePeerBroadcastMsg.MSG_CLASS_STR,
                        'prc_remote_peer_broadcast_msg')
        
        # Initial Announcement
        self._send_broadcast()
        
        # Resume module
        super(PeerDiscoveryMod, self).run_module()
        
        
    def prc_ping_for_peers_msg(self, msg):
        '''Broadcast presence to other peers on network'''
        # Send Peer Broadcast
        self._send_broadcast()
        
        # Check for expired peers
        self._check_expired_peers()
        
        
    def prc_remote_peer_broadcast_msg(self, msg):
        '''Broadcast received from another peer on the network'''
        if msg.parms['msg'] == UdpPeerPing.HI:
            self._handle_peer_discovered(msg.parms['peer'])
        elif msg.parms['msg'] == UdpPeerPing.GOODBYE:
            self._handle_peer_missing(msg.parms['peer'])
        else:
            text = "Unknown message in ping: '%s'"
            self.__log.error(text % (msg.parms['msg']))
        
        
    def prc_do_shutdown_msg(self, msg):
        self.broker.dispatch(StartShutdownMsg())
        
        
    # -- Peer Discovery -------------------------------------------------------
    
    def _build_socket(self):
        '''Build a socket for sending and receiving UDP packets'''
        
        text = "Binding to UDP port %s for peer discovery"
        self.__log.info(text % (self.__port))
        
        s = socket(AF_INET, SOCK_DGRAM)
        s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        s.bind(('', self.__port))
        s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        
        return s
    
    
    def _send_broadcast(self):
        '''Send broadcast announcing this peer'''
        ping = UdpPeerPing(peer_name=self.__context.peer_alias,
                           peer_uid=self.__context.peer_id)
        msg_src = ping.gen_msg_data()
        self.__sock.sendto(msg_src, ('<broadcast>', self.__port))


    def _send_broadcast_leaving(self):
        '''Send broadcast announcing this peer'''
        ping = UdpPeerPing(peer_name=self.__context.peer_alias,
                           peer_uid=self.__context.peer_id,
                           msg=UdpPeerPing.GOODBYE)
        msg_src = ping.gen_msg_data()
        self.__sock.sendto(msg_src, ('<broadcast>', self.__port))


    def _check_expired_peers(self):
        '''Check for expired peers'''
        timeout_secs = 2.5 * self.PING_INTERVAL_SECS
        for peer in self.__known_peers.all_peers():
            if peer.seconds_since_last_seen() > timeout_secs:
                self._handle_peer_missing(peer)
        
        
    def _handle_peer_discovered(self, new_peer):
        '''Add a newly discovered peer
        
        @param new_peer: DiscoveredPeer
        '''
        if new_peer.uid == self.__context.peer_id:
            return
        
        try:
            # Known peer
            peer = self.__known_peers.get_peer_by_uid(new_peer.uid)
            peer.update_confirmed_ts()
            
        except KeyError:
            # Record peer
            self.__known_peers.add_peer(new_peer)
            
            # Announce peer
            msg = PeerDiscoveredMsg(peer_name = new_peer.name,
                                    peer_uid = new_peer.uid,
                                    peer_addresses = new_peer.ips)
            self.broker.dispatch(msg)

    
    def _handle_peer_missing(self, peer):
        '''Note that a peer is no longer seen
        
        @param new_peer: DiscoveredPeer
        '''
        msg = PeerLostMsg(peer_name = peer.name,
                          peer_uid = peer.uid
                          )
        self.__known_peers.remove_peer(peer)
        self.broker.dispatch(msg)
        
    