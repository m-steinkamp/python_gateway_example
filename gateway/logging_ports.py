from .ports import *


class ReceivePortLogger(AbstractReceivePort):
    '''
    Decorator which prints the method calls.
    '''

    def __init__(self, name: str, receiver: AbstractReceivePort):
        self.name = name
        self.receiver = receiver

    def set_receive_callback(self, receive_callback: Callable[[object, Message], None], channel: object):
        self.receiver.set_receive_callback(receive_callback, channel)

    def process_received_message(self, received_message: Message):
        print(f'{self.name}.process_received_message({received_message})')
        self.receiver.process_received_message(received_message)
    
    def release_message_buffer(self, received_message: Message):
        print(f'{self.name}.release_message_buffer({received_message})')
        self.receiver.release_message_buffer(received_message)


class SendPortLogger(AbstractSendPort):
    '''
    Decorator which prints the method calls.
    '''

    def __init__(self, name: str, sender: AbstractSendPort):
        self.name = name
        self.sender = sender

    def provide_message_buffer(self) -> Message:
        print(f'{self.name}.provide_message_buffer()')
        return self.sender.provide_message_buffer()
    
    def send_message(self, outgoing_message: Message):
        print(f'{self.name}.send_message({outgoing_message})')
        self.sender.send_message(outgoing_message)
