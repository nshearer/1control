'''
Created on Mar 12, 2012

@author: nate
'''
from msg_passing.BrokeredMsg import BrokeredMsg

class PeerDiscoveredMsg(BrokeredMsg):
    '''A new peer has been found on the network'''
    
    MSG_CLASS_STR='discovery.peer_discovered'
    
    def __init__(self, peer_name, peer_uid, peer_addresses):
        '''Init
        
        @param peer_name: Name/alias for peer
        @param peer_uid: Unique ID for this peer
        @param peer_addresses: List of IP Address to connect to peer
        '''
        super(PeerDiscoveredMsg, self).__init__(self.MSG_CLASS_STR)
        self.parms['peer_uid'] = peer_uid
        self.parms['peer_name'] = peer_name
        self.parms['peer_addresses'] = peer_addresses
        