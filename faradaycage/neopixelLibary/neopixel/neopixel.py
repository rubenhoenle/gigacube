from gigacube import HyperVisor

class NeoPixel:

    noMapper = {17: 0,
                16: 1}

    def __init__(self, pin, length):
        
        self.h = HyperVisor.instance()

        self.pin = pin
        self.length = length

        self.data = [None for _ in range(self.length)]
    
    def __getitem__(self, index):
        return self.data[index]

    def __setitem__(self, index, color):
        # validate color
        self.data[index] = color

    def write(self):
        self.show()

    def show(self):
        self.h.cube.setColor(NeoPixel.noMapper.get(self.pin.no), self.data)
        self.h.cube.write()

    def fill(self, color):
        self.data = [color for _ in range(self.length)]
