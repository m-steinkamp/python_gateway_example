from typing import Callable
from .message import Message


class AbstractReceivePort:
    '''
    Interface for the receiving side of a protocol.
    '''

    def __init__(self, receive_callback: Callable[[Message], None]=None):
        self.receive_callback = receive_callback

    def set_receive_callback(self, receive_callback: Callable[[Message], None], channel: object):
        self.channel = channel
        self.receive_callback = receive_callback

    def process_received_message(self, received_message: Message):
        '''
        call this method in subclass, when the protocol received a new message
        the message buffer must stay valid until the gateway core releases it with release_message_buffer
        '''
        if self.receive_callback:
            self.receive_callback(received_message)
    
    #@abstractmethod
    def release_message_buffer(self, received_message: Message):
        '''
        releases message buffer of a former process_received_message call
        '''
        pass


class AbstractSendPort:
    '''
    Interface for the sending side of a protocol.
    '''

    #@abstractmethod
    def provide_message_buffer(self) -> Message:
        '''
        called by gateway core to allocate a Message buffer which will be filled
        during processing the conversion of a received message.
        '''
        return Message()

    #@abstractmethod
    def send_message(self, outgoing_message: Message):
        '''
        called by gateway core to send given Message with implementing protocol.
        the outgoingMessage buffer must be released after it has been sent.
        '''
        pass


# TODO: diese Klasse nötig? Für bidirektionale Datenkonvertierung hin oder her.
#       ich baue es erstmal unidirektional...
class ProtocolConnector:
    def __init__(self, receive_port: AbstractReceivePort, send_port: AbstractSendPort):
        self.receive_port = receive_port
        self.send_port = send_port