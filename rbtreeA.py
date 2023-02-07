import sys
from tkinter import *
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

class Node(Object):
    def __init__(self, data):
        super().__init__(data)
        self.data = data
        self.parent = None
        self.left = None
        self.right = None
        self.color = 1 # 1 = red, 0 = black

class RBTree():
    def __init__(self, aniList, originx, originy):
        self.NULL = Node(0)
        self.NULL.color = 0
        self.NULL.left = None
        self.NULL.right = None
        self.root = self.NULL
        self.animationList = aniList
        self.originx = originx
        self.originy = originy
        self.step = 0
        self.size = 50

    def insert(self, val, step):
        node = Node(val)
        node.parent = None
        node.data = val
        node.left = self.NULL
        node.right = self.NULL
        node.color = 1

        self.originx = 600
        self.originy = 50

        y = None
        x = self.root

        while x != self.NULL:
            y = x
            self.originy += 100
            if node.data < x.data:
                x = x.left
                self.originx -= 100
            else:
                x = x.right
                self.originx += 100

        node.parent = y
        if y == None:
            self.root = node
        elif node.data < y.data:
            y.left = node
        else:
            y.right = node

        if node.parent == None:
            node.color = 0
            self.animationList.append(node)
            node.aniQueue.put(Movement(-1,-1,step,[],[],['oval',self.originx,self.originy,self.size,str(node.data),'gray']))
            node.x = self.originx
            node.y = self.originy
            return

        if node.parent.parent == None:
            self.animationList.append(node)
            node.aniQueue.put(Movement(-1,-1,step,[],[],['oval',self.originx,self.originy,self.size,str(node.data),'red']))
            node.x = self.originx
            node.y = self.originy
            #Create line to parent node
            if node.parent.right == node:
                node.aniQueue.put(Movement(-1,-1,step,[],[node.x, node.y, node.parent.x + self.size, node.parent.y + self.size]))
            else:
                node.aniQueue.put(Movement(-1,-1,step,[],[node.x + self.size, node.y, node.parent.x, node.parent.y + self.size]))
            return

        self.animationList.append(node)
        node.aniQueue.put(Movement(-1,-1,step,[],[],['oval',self.originx,self.originy,self.size,str(node.data),'red']))
        node.x = self.originx
        node.y = self.originy
        if node.parent.right == node:
            node.aniQueue.put(Movement(-1,-1,step,[],[node.x, node.y, node.parent.x + self.size, node.parent.y + self.size]))
        else:
            node.aniQueue.put(Movement(-1,-1,step,[],[node.x + self.size, node.y, node.parent.x, node.parent.y + self.size]))

        self.insertHelper(node, step)

    def insertHelper(self, node, step):
        while node.parent.color == 1:
            if node.parent == node.parent.parent.right:
                u = node.parent.parent.left
                if u.color == 1:
                    u.color = 0
                    node.aniQueue.put(Movement(-1,-1,step,[],[],['oval',u.x,u.y,self.size,str(u.data),'gray']))
                    node.parent.color = 0
                    node.aniQueue.put(Movement(-1,-1,step,[],[],['oval',node.parent.x,node.parent.y,self.size,str(node.parent.data),'gray']))
                    node.parent.parent.color = 1
                    node.aniQueue.put(Movement(-1,-1,step,[],[],['oval',node.parent.parent.x,node.parent.parent.y,self.size,str(node.parent.parent.data),'red']))
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self.rightRotate(node, step)
                    node.parent.color = 0
                    node.aniQueue.put(Movement(-1,-1,step,[],[],['oval',node.parent.x,node.parent.y,self.size,str(node.parent.data),'gray']))
                    node.parent.parent.color = 1
                    node.aniQueue.put(Movement(-1,-1,step,[],[],['oval',node.parent.parent.x,node.parent.parent.y,self.size,str(node.parent.parent.data),'red']))
                    self.leftRotate(node.parent.parent, step)
            else:
                u = node.parent.parent.right
                if u.color == 1:
                    u.color = 0
                    node.aniQueue.put(Movement(-1,-1,step,[],[],['oval',u.x,u.y,self.size,str(u.data),'gray']))
                    node.parent.color = 0
                    node.aniQueue.put(Movement(-1,-1,step,[],[],['oval',node.parent.x,node.parent.y,self.size,str(node.parent.data),'gray']))
                    node.parent.parent.color = 1
                    node.aniQueue.put(Movement(-1,-1,step,[],[],['oval',node.parent.parent.x,node.parent.parent.y,self.size,str(node.parent.parent.data),'red']))
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        node = node.parent
                        self.leftRotate(node, step)
                    node.parent.color = 0
                    node.aniQueue.put(Movement(-1,-1,step,[],[],['oval',node.parent.x,node.parent.y,self.size,str(node.parent.data),'gray']))
                    node.parent.parent.color = 1
                    node.aniQueue.put(Movement(-1,-1,step,[],[],['oval',node.parent.parent.x,node.parent.parent.y,self.size,str(node.parent.parent.data),'red']))
                    self.rightRotate(node.parent.parent, step)
            
            if node == self.root:
                break
                
        self.root.color = 0
        node.aniQueue.put(Movement(-1,-1,step,[],[],['oval',self.root.x,self.root.y,self.size,str(self.root.data),'gray']))

    def leftRotate(self, node, step):
        y = node.right
        node.right = y.left
        if y.left != self.NULL:
            y.left.parent = node

        y.parent = node.parent
        if node.parent == None:
            self.root = y
        elif node == node.parent.left:
            node.parent.left = y
        else:
            node.parent.right = y
        y.left = node
        node.parent = y

    def rightRotate(self, node, step):
        y = node.left
        node.left = y.right
        if y.right != self.NULL:
            y.right.parent = node

        y.parent = node.parent
        if node.parent == None:
            self.root = y
        elif node == node.parent.right:
            node.parent.right = y
        else:
            node.parent.left = y
        y.right = node
        node.parent = y
    
    def delete(self, data):
        self.deleteHelper(self.root, data)

    def deleteHelper(self, node, val):
        x = self.NULL
        while node != self.NULL:
            if node.data == val:
                x = node
            
            if node.data <= val:
                node = node.right
            else:
                node = node.left

        if x == self.NULL:
            print("Value is not in tree")
            return

        y = x
        yOrigColor = y.color
        if x.left == self.NULL:
            z = x.right
            self.rbtransplant(x, x.right)
        elif x.right == self.NULL:
            z = x.left
            self.rbtransplant(x, x.left)
        else:
            y = self.minimum(x.right)
            yOrigColor = y.color
            z = y.right
            if y.parent == x:
                z.parent = y
            else:
                self.rbtransplant(y, y.right)
                y.right = x.right
                y.right.parent = y

            self.rbtransplant(x, y)
            y.left = x.left
            y.left.parent = y
            y.color = x.color

        if yOrigColor == 0:
            self.fixDelete(z)

    def fixDelete(self, x):
        while x != self.root and x.color == 0:
            if x == x.parent.left:
                s = x.parent.right
                if s.color == 1:
                    s.color = 0
                    x.parent.color = 1
                    self.leftRotate(x.parent)
                    s = x.parent.right

                if s.left.color == 0 and s.right.color == 0:
                    s.color = 1
                    x = x.parent
                else:
                    if s.right.color == 0:
                        s.left.color = 0
                        s.color = 1
                        self.rightRotate(s)
                        s = x.parent.right

                    s.color = x.parent.color
                    x.parent.color = 0
                    s.right.color = 0
                    self.leftRotate(x.parent)
                    x = self.root
            else:
                s = x.parent.left
                if s.color == 1:
                    s.color = 0
                    x.parent.color = 1
                    self.rightRotate(x.parent)
                    s = x.parent.left

                if s.left.color == 0 and s.right.color == 0:
                    s.color = 1
                    x = x.parent
                else:
                    if s.left.color == 0:
                        s.right.color = 0
                        s.color = 1
                        self.leftRotate(s)
                        s = x.parent.left

                    s.color = x.parent.color
                    x.parent.color = 0
                    s.left.color = 0
                    self.rightRotate(x.parent)
                    x = self.root
        x.color = 0

    def search(self, k):
        return self.searchHelper(self.root, k)

    def searchHelper(self, node, val):
        if node == self.NULL or val == node.data:
            return node
        if val < node.data:
            return self.searchHelper(node.left, val)

        return self.searchHelper(node.right, val)

    def rbtransplant(self, u, v):
        if u.parent == None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def minimum(self, node):
        while node.left != self.NULL:
            node = node.left
        return node
    
    def maximum(self, node):
        while node.right != self.NULL:
            node = node.right
        return node

    def printHelper(self, node, indent, last):
        if node != self.NULL:
            sys.stdout.write(indent)
            if last:
                sys.stdout.write("R----")
                indent += "     "
            else:
                sys.stdout.write("L----")
                indent += "|    "

            sColor = "RED" if node.color == 1 else "BLACK"
            print(str(node.data) + "(" + sColor + ")")
            self.printHelper(node.left, indent, False)
            self.printHelper(node.right, indent, True)

    def print(self):
        self.printHelper(self.root, "", True)

    def rbTree(aniList):
        # orginx = 600
        # orginy = 0
        step = 0
        # size = 50

        bst = RBTree(aniList, 600, 50)
        myList = []

        dataFile = open('smallerdataset.txt', 'r')
        for line in dataFile:
            if(not line.isspace() and len(line) > 0):
                #Only time you use aniList is to append Objects
                #Do not remove or move or anything else
                aniList.append(Object(int(line)))

                #Everything in python is a pointer so populate your data structure with the aniList objects
                myList.append(aniList[-1])
        dataFile.close()

        placeHolder = 0
        for i in myList:
            bst.insert(myList[placeHolder].userNum, step)
            step += 1
            placeHolder += 1

        # while 1:
            # if delete button pressed:
                # add the value to myList?? 
                # bst.delete(value written in box, myList, step, size, placeHolder)
            # if insert button pressed:
                # add value written in box to myList
                # step += 1
                # bst.insert(myList[placeHolder].userNum, myList, step, size, placeHolder)
                # placeHolder += 1
            # if exit button pushed
                # return 0??