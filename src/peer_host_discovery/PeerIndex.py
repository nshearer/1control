'''
Created on Apr 2, 2012

@author: nate
'''
from copy import copy


class DuplicatePeerUid(KeyError): pass


class PeerIndex(object):
    '''Collection of DiscoveredPeer objects for known peers
    
    UID is the only attribute that can be used to definitively identify a peer
    '''
    
    def __init__(self):
        self.__by_uid = dict()
        self.__by_ip = dict()
        self.__by_name = dict()
        
        
    def add_peer(self, peer):
        '''Add a peer record to the collection
        
        @param peer: DiscoveredPeer to add to collection
        '''
        
        peer = copy(peer)
        
        if self.__by_uid.has_key(peer.uid):
            text = "Peer with UID %s already exists"
            raise DuplicatePeerUid(text % (peer.uid))
        self.__by_uid[peer.uid] = peer
        
        if not self.__by_name.has_key(peer.name):
            self.__by_name[peer.name] = list()
        self.__by_name[peer.name].append(peer)
        
        for ip in peer.ips:
            if not self.__by_ip.has_key(ip):
                self.__by_ip[ip] = list()
            self.__by_ip[ip].append(peer)
        
                
    def remove_peer(self, peer):
        '''Remove a peer record from the collection
        
        @param peer: DiscoveredPeer to remove from collection
        '''
        peer = self.get_peer_by_uid(peer.uid)
        
        for ip in peer.ips:
            if self.__by_ip.has_key(ip):
                self.__by_ip[ip].remove(peer)
            if len(self.__by_ip[ip]) == 0:
                del self.__by_ip[ip]
                
        if self.__by_name.has_key(peer.name):
            self.__by_name[peer.name].remove(peer)
        if len(self.__by_name[peer.name]) == 0:
            del self.__by_name[peer.name]
            
        del self.__by_uid[peer.uid]
        
    
    def all_peers(self):
        for peer in self.__by_uid.values():
            yield peer
            
                
        
        
    def get_peer_by_uid(self, uid):
        return self.__by_uid[uid]
    
    
    def has_peer_uid(self, uid):
        try:
            return self.get_peer_by_uid(uid) is not None
        except KeyError:
            return False