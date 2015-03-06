'''
Created on Apr 2, 2012

@author: nate
'''
import socket
import logging

from msg_passing.app.DirectMsgFeederMonitor import DirectMsgFeederMonitor
from msg_passing.app.DirectMsgFeederMonitor import NoEventMonitored

from DiscoveredPeer import DiscoveredPeer
from msgs.RemotePeerBroadcastMsg import RemotePeerBroadcastMsg
from UdpPeerPing import UdpPeerPing, MessageSourceMalformed

class BroadcastMonitorThread(DirectMsgFeederMonitor):
    '''Thread which listens for UDP broadcasts on socket'''
    
    def __init__(self, sock, port, peer_discovery):
        '''Init
        
        @param sock: Socket to monitor
        @param port: UDP port to listen on
        @param peer_discovery: PeerDiscovery module to pass msgs to
        '''
        self.__sock = sock
        self.__port = port
        self.__timeout_set = False
        self.__buffer = list()
        self.__log = logging.getLogger(self.__class__.__name__)
        
        super(BroadcastMonitorThread, self).__init__(
            parent=peer_discovery,
            thread_name='Discovery Monitor')
        
        
    def get_data(self, timeout_sec):
        '''Watch UDP socket for peer broadcasts
        
        @param timeout_sec: Number of seconds to monitor for
        @return: DiscoveredPeer
        @raise NoEventMonitored: If timeout was reached
        '''
        if not self.__timeout_set:
            self.__sock.settimeout(timeout_sec)
            self.__timeout_set = True
        
        try:
            rcv_data, rcv_addr = self.__sock.recvfrom(self.__port)
            if rcv_data:
                return rcv_data, rcv_addr
        except socket.timeout:
            raise NoEventMonitored()
        

    def handle_data(self, data):
        '''Process any monitored event
        
        @param data: (data received, remote IP address)
        '''
        rcv_data, rcv_addr = data
        
        for msg_src in UdpPeerPing.break_apart_msgs(rcv_data):

            # Construct Discovered Peer message
            try:
                ping_msg = UdpPeerPing.decode_msg(msg_src)

                peer = DiscoveredPeer(uid=ping_msg.peer_uid,
                                      name=ping_msg.peer_name,
                                      ips=[rcv_addr[0], ],
                                      )
                    
                self.feed(RemotePeerBroadcastMsg(peer, ping_msg.msg))
            
            except MessageSourceMalformed:
                text = "Discarding invalid data received from %s: %s"
                self.__log.warn(text % (str(rcv_addr), rcv_data))
    
    
        