from queue import Queue

class Object:
    def __init__(self,num):
        self.shape = None
        self.text = None
        self.lineToParent = None
        self.x = -1
        self.y = -1
        self.aniQueue = Queue()
        self.moveQueue = Queue()
        self.userNum = num

class Movement:
    def __init__(self,x,y,step=0,args=[],newLine=[],newObject=[]):
        self.x = x
        self.y = y
        self.step = step
        self.args = args
        self.newLine = newLine
        self.newObject = newObject
