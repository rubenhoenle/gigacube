
class HyperVisor(object):
    _instance = None
    cube = None

    def __init__(self):
        raise Runtimerror('Call instance() instead')

    @classmethod
    def instance(cls):
        if cls._instance is None:
            
            cls._instance = cls.__new__(cls)
            cls._instance.cube = cls._instance.start_cube()
        return cls._instance

    def start_cube(self):

        if self.cube != None:
            return self.cube

        import threading
        from .gigacube import Gigacube

        self.cube = Gigacube()

        return self.cube 

    def isUp(self):
        return list(self.cube.pressed_keys.values())[0]

    def isDown(self):
        return list(self.cube.pressed_keys.values())[1]
    
    def isLeft(self):
        return list(self.cube.pressed_keys.values())[2]

    def isRight(self):
        return list(self.cube.pressed_keys.values())[3]

    def getButtons(self):
        return self.cube.buttons

    def isCenter(self):
        return all(value == 0 for value in self.cube.pressed_keys.values())
