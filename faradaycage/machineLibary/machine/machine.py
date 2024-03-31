

class Pin:

    OUT = "out"
    IN = "in"

    def __init__(self, no: int, state: str):

        if no != 16 and no != 17:
            raise ValueError("not a supported Pin. 16 and 17 are supported")

        self.no = no
        self.state = state