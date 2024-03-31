
class HyperVisor(object):
    _instance = None
    cube = None

    def __init__(self):
        raise RuntimeError('Call instance() instead')

    @classmethod
    def instance(cls):
        if cls._instance is None:
            
            cls._instance = cls.__new__(cls)
            cls._instance.cube = cls._instance.start_cube()
            # Put any initialization here.
        return cls._instance


    def start_cube(self):

        if self.cube != None:
            return self.cube

        import threading
        from gigacube import Gigacube

        cube = Gigacube()

        return cube 