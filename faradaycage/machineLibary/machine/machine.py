

class Pin:

    OUT = "out"
    IN = "in"

    def __init__(self, no: int, state: str = OUT):
        self.no = no
        self.state = state

class I2C:

    def __init__(self, i, scl, sda, freq):
        self.i = i 
        self.scl = scl
        self.sda = sda
        self.freq = freq