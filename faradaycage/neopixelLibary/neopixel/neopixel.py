from hypervisor import HyperVisor

class NeoPixel:

    def __init__(self, pin, length):
        
        self.h = HyperVisor.instance()

        self.pin = pin
        self.length = length

        self.data = [None for _ in range(self.length)]
        print("Hello from emulated class")
    
    def __getitem__(self, index):
        return self.data[index]

    def __setitem__(self, index, color):
        # validate color
        self.data[index] = color

    def write(self):
        self.show()

    def show(self):
        self.h.cube.setColor(0, self.data)
        self.h.cube.write()

    def fill(self, color):
        self.data = [color for _ in range(self.length)]

n = NeoPixel(0, 15 * 15 * 2)
n[15] = (0, 255, 0)
n.write()