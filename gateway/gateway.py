from .message import Message
from .ports import *
from .conversion import Conversion


class ConversionChannel:
    '''
    This class sets up an uni-directional message conversion channel between the two protocols.
    '''
    def __init__(self, receiver: AbstractReceivePort, sender: AbstractSendPort, conversion: Conversion):
        self.receiver = receiver
        self.sender = sender
        self.conversion = conversion
        receiver.set_receive_callback(self._received_message_callback, self)

    def _received_message_callback(self, received_message: Message):
        # TODO: wo kommt das passende 'self' her?
        outgoing_message = self.sender.provide_message_buffer()
        self.conversion.convert(received_message, outgoing_message)
        self.receiver.release_message_buffer(received_message)
        self.sender.send_message(outgoing_message)


class Gateway:
    '''
    This class just holds all conversion channels.
    '''
    def __init__(self):
        self.channels = {}

    def add_channel(self, receiver: AbstractReceivePort, sender: AbstractSendPort, conversion: Conversion):
        self.channels[receiver] = ConversionChannel(receiver, sender, conversion)
