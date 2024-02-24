class Message:
    def __init__(self, address=None, payload=None):
        self.address = address
        self.payload = payload

    def __str__(self):
        return f'Message({self.address} as {type(self.address)}, {self.payload} as {type(self.payload)})'