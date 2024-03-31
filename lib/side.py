from .enums import Direction

class Side:
    def __init__(self, name, size):
        self.name = name
        self.size = size

        self.top_dir = None
        self.down_dir = None
        self.left_dir = None
        self.right_dir = None

    def __str__(self):
        return self.name

    def attach_top(self, side, direction):
        self.top = side
        self.top_dir = direction
    
    def attach_down(self, side, direction):
        self.down = side
        self.down_dir = direction

    def attach_left(self, side, direction):
        self.left = side
        self.left_dir = direction

    def attach_right(self, side, direction):
        self.right = side
        self.right_dir = direction

    def transfer_up(self, pos):
        if hasattr(self, "top"):
            pos.side = self.top
            if self.top_dir == Direction.DOWN:
                pos.y = 0 
            elif self.top_dir == Direction.LEFT:
                pos.y = self.size - pos.x - 1
                pos.x = 0
            elif self.top_dir == Direction.RIGHT:
                pos.y = pos.x
                pos.x = self.size - 1    

            return self.invert(self.top_dir)           
        raise ValueError("out of bounds")

    def transfer_down(self, pos):
        if hasattr(self, "down"):
            pos.side = self.down
            pos.y = self.size - 1
            return self.invert(self.down_dir)
        raise ValueError("out of bounds")

    def transfer_left(self, pos):
        if hasattr(self, "left"):
            pos.side = self.left
            if self.left_dir == Direction.RIGHT:
                pos.x = self.size - 1
            elif self.left_dir == Direction.UP:
                pos.x = self.size - pos.y
                pos.y = self.size - 1
            elif self.left_dir == Direction.DOWN:
                pos.x = self.size - pos.y - 1
                pos.y = 0

            return self.invert(self.left_dir)
        raise ValueError("out of bounds")

    def transfer_right(self, pos):
        if hasattr(self, "right"):
            pos.side = self.right
            if self.right_dir == Direction.LEFT:
                pos.x = 0
            elif self.right_dir == Direction.UP:
                pos.x = pos.y
                pos.y = self.size - 1
            elif self.right_dir == Direction.DOWN:
                pos.x = pos.y
                pos.y = 0

            return self.invert(self.right_dir)
        raise ValueError("out of bounds")

    
    def invert(self, direction):

        if(direction == Direction.DOWN): return Direction.UP
        if(direction == Direction.UP): return Direction.DOWN
        if(direction == Direction.LEFT): return Direction.RIGHT
        if(direction == Direction.RIGHT): return Direction.LEFT





    