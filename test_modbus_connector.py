from gateway.ports import *
from gateway.logging_ports import *

class ModbusConnector(ProtocolConnector):
    class Sender(AbstractSendPort):
        '''
        In diesem Beispiel Code dient der "Sender" als der Code, der eine Nachricht vom Gateway
        bekommt, entscheidet was damit zu tun ist und schickt ggfs. eine Antwort per Receiver.
        '''

        def __init__(self, receiver: 'ModbusConnector.Receiver'):
            self.test_value = 0
            self.receiver = receiver

        def provide_message_buffer(self) -> Message:
            return Message()
        
        def send_message(self, outgoing_message: Message):
            if outgoing_message.address == 1001:
                # setter
                self.test_value = outgoing_message.payload
            else:
                # getter
                response = Message(1000, self.test_value)
                self.receiver.process_received_message(response)

    def __init__(self):
        receiver = ReceivePortLogger('MODBUS.Receiver', AbstractReceivePort())
        sender = SendPortLogger('MODBUS.Sender', self.Sender(receiver))
        super().__init__(receiver, sender)
