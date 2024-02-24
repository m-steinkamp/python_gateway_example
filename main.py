from gateway.message import *
from gateway.ports import *
from gateway.logging_ports import *
from gateway.gateway import *
from gateway.conversion import *
from test_modbus_connector import ModbusConnector


to_int_conversion = PayloadToIntConversion()
to_str_conversion = PayloadToStrConversion()


rest_receiver = ReceivePortLogger('REST.Receiver', AbstractReceivePort())
rest_sender = SendPortLogger('REST.Sender', AbstractSendPort())
rest_to_modbus_address_mapping = AddressMapping({
    'rest/getter': 1000,
    'rest/setter': 1001
})
rest_to_modbus_conversion_config = ConversionFinder({
    'rest/getter': ConversionChain([rest_to_modbus_address_mapping]),
    'rest/setter': ConversionChain([rest_to_modbus_address_mapping, to_int_conversion])
})


modbus_connector = ModbusConnector()
modbus_to_rest_address_mapping = AddressMapping({1000: 'rest/getter'})
modbus_to_rest_conversion_config = ConversionFinder({1000: ConversionChain([modbus_to_rest_address_mapping, to_str_conversion])})


the_gateway = Gateway()
the_gateway.add_channel(rest_receiver, modbus_connector.send_port, rest_to_modbus_conversion_config)
the_gateway.add_channel(modbus_connector.receive_port, rest_sender, modbus_to_rest_conversion_config)

print('\n## Message 1 ##')
rest_receiver.process_received_message(Message(address='rest/getter'))

print('\n## Message 2 ##')
rest_receiver.process_received_message(Message(address='rest/setter', payload='20'))

print('\n## Message 3 ##')
rest_receiver.process_received_message(Message(address='rest/getter'))
