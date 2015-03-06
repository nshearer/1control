'''
Created on Apr 2, 2012

@author: nate
'''
from msg_passing.BrokeredMsg import BrokeredMsg

class RemotePeerBroadcastMsg(BrokeredMsg):
    '''A remote peer broadcast has been received'''
    
    MSG_CLASS_STR='peer_discovery.remote_peer_broadcast'
    
    def __init__(self, peer, msg):
        '''Init
        
        @param peer: DiscoveredPeer object
        '''
        super(RemotePeerBroadcastMsg, self).__init__(self.MSG_CLASS_STR)
        self.parms['peer'] = peer
        self.parms['msg'] = msg
        