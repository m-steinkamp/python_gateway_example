from abc import ABC, abstractmethod
from typing import List, Dict
from .message import Message


class Conversion(ABC):
    '''
    This interface does some kind of conversion within given output Message.
    '''

    @abstractmethod
    def convert(self, input: Message, output: Message):
        pass


class ConversionChain(Conversion):
    '''
    Composite pattern. Combine multiple conversions and execute them in given order.
    '''

    def __init__(self, conversions: List[Conversion]):
        self.conversions = conversions

    def convert(self, input: Message, output: Message):
        for conversion in self.conversions:
            conversion.convert(input, output)


class ConversionFinder(Conversion):
    '''
    Finds the correct conversion (chain) based on received messages address
    '''

    def __init__(self, conversion_map: Dict[object, Conversion]):
        self.conversion_map = conversion_map
    
    def convert(self, input: Message, output: Message):
        if input.address in self.conversion_map:
            self.conversion_map[input.address].convert(input, output)


class AddressMapping(Conversion):
    def __init__(self, address_mapping: Dict[object, object]):
        self.address_mapping = address_mapping

    def convert(self, input: Message, output: Message):
        output.address = self.address_mapping[input.address]


class PayloadToStrConversion(Conversion):
    def convert(self, input: Message, output: Message):
        output.payload = str(input.payload)


class PayloadToIntConversion(Conversion):
    def convert(self, input: Message, output: Message):
        output.payload = int(input.payload)
