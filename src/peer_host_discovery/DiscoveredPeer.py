'''
DiscoveredPeer class

@author: nate
'''
from datetime import datetime, timedelta

class DiscoveredPeer(object):
    '''Encapsulates knowledge of a discovered peer'''
    
    def __init__(self, uid, name, ips):
        '''Init
        
        @param uid: Unique ID for peer
        @param name: Unique name for peer
        @param ips: List of IPs peer can be connected at
        '''
        self.__name = name
        self.__ip = tuple(ips)
        self.__uid = uid
        self.first_discovered = datetime.now()
        self.last_confirmed = datetime.now()
        
        
    @property
    def uid(self):
        return self.__uid
    
    @property
    def name(self):
        return self.__name
    
    
    @property
    def ips(self):
        '''IPs that the peer can be contacted at'''
        return list(self.__ip)
        
    
    def __str__(self):
        return "%s (%s)" % (self.uid, self.name)    
    
        
    def __eq__(self, peer):
        if self.uid == peer.uid:
            return True
        return False
        
        
    def seconds_since_last_seen(self):
        '''Determine the number of seconds since this peer was last seen'''
        return (datetime.now() - self.last_confirmed).total_seconds()
        
        
    def update_confirmed_ts(self):
        '''Update the peer data to show that it was just confirmed'''
        self.last_confirmed = datetime.now()
        
        
