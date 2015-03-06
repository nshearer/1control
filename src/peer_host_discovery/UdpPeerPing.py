'''
Created on Apr 3, 2012

@author: nate
'''

class MessageSourceMalformed(Exception): pass


class UdpPeerPing(object):
    '''Wraps a broadcast message announcing a peer's presence'''
    
    MSG_TYPE_TOKEN = 'UdpBroadcastPeerFinder'

    HI = 'Hi'
    GOODBYE = 'Goodbye'
    
    def __init__(self, peer_name=None, peer_uid=None, msg=None):
        self.msg_type_id = self.MSG_TYPE_TOKEN
        self.msg = msg or UdpPeerPing.HI
        self.peer_name = peer_name
        self.peer_uid = peer_uid
        
        
    def gen_msg_data(self):
        '''Turn message into a string to send out on the socket'''
        assert self.peer_name is not None
        assert self.peer_uid  is not None
        
        msg = [self.MSG_TYPE_TOKEN,
               self.msg,
               self.peer_name,
               self.peer_uid,
               ]
        msg = "\n".join(msg) + '\n\n'
        
        if not self.is_valid_msg_src(msg):
            raise Exception("Self produced message is not valid!")
        
        return msg
        

    @staticmethod
    def is_valid_msg_src(msg_src):
        '''Check to see if data received on the socket is valid
        
        @param msg_src: Message in string form
        '''
        parts = msg_src.strip().split("\n")
        if len(parts) == 4:
            if parts[0] == UdpPeerPing.MSG_TYPE_TOKEN:
                return True
        return False
        
        
    @staticmethod
    def break_apart_msgs(data):
        '''This method takes the received stream of data and breaks out msgs
        
        Since multiple announcements can be received at once, this method
        handles that by breaking them up.
        
        I'm making an assumption here that we won't get half a broadcast
        message.  If we do, is_valid_msg() should kick it out.
        
        @return gen: Yields the source for individual messages
        '''
        parts = data.split(UdpPeerPing.MSG_TYPE_TOKEN)
        for part in parts:
            if len(part.strip()) > 0:
                yield UdpPeerPing.MSG_TYPE_TOKEN + part
                
                
    @staticmethod
    def decode_msg(msg_src):
        '''Decode message received
        
        @param msg_src: Data received for a message (use break_apart_msgs())
        @return UdpPeerPing
        '''
        if not UdpPeerPing.is_valid_msg_src(msg_src):
            raise MessageSourceMalformed()
        
        parts = msg_src.strip().split("\n")
        
        msg = UdpPeerPing(peer_name=parts[2], peer_uid=parts[3])
        msg.msg = parts[1]
        
        return msg
    