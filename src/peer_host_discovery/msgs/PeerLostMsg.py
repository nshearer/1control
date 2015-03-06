'''
Created on Mar 12, 2012

@author: nate
'''
from msg_passing.BrokeredMsg import BrokeredMsg

class PeerLostMsg(BrokeredMsg):
    '''A new peer is no longer being seen on the network'''
    
    MSG_CLASS_STR='discovery.peer_lost'
    
    def __init__(self, peer_name, peer_uid):
        '''Init
        
        @param peer_name: Name/alias for peer
        @param peer_uid: Unique ID for this peer
        @param peer_addresses: List of IP Address to connect to peer
        '''
        super(PeerLostMsg, self).__init__(self.MSG_CLASS_STR)
        self.parms['peer_uid'] = peer_uid
        self.parms['peer_name'] = peer_name
        