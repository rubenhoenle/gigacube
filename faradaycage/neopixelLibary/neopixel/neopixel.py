

class NeoPixel:

    def __init__(self, pin, length):

        self.pin = pin
        self.length = length

        self.data = [None for _ in range(self.length)]
        print("Hello from emulated class")
    
    def __getitem__(self, index):
        return self.data[index]

    def __setitem__(self, index, color: tuple):
        # validate color
        return self.data[index] = color

    def write(self):
        self.show()

    def show(self):
        pass

    def fill(sefl, color: type):
        self.data = [color for _ in range(self.length)]