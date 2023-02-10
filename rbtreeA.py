import sys
from tkinter import *
from queue import Queue
import time

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
    def __init__(self, aniList, originx, originy, yDist, size):
        self.NULL = Node(0)
        self.NULL.color = 0
        self.NULL.left = None
        self.NULL.right = None
        self.root = self.NULL
        self.height = 1
        self.animationList = aniList
        self.originx = originx
        self.originy = originy
        self.step = 0
        self.size = size
        self.yDist = yDist

    def insert(self, val):
        separators = [0,4,2,1,.5,.5]

        # create node
        node = Node(val)
        node.parent = None
        node.data = val
        node.left = self.NULL
        node.right = self.NULL
        node.color = 1

        y = None
        x = self.root

        # find where new node goes in tree
        while x != self.NULL:
            x.aniQueue.put(Movement(-1, -1,self.step, ['gold']))
            if y is not None:
                y.aniQueue.put(Movement(-1, -1,self.step,['gray' if y.color == 0 else 'red']))
            time.sleep(1) # delay so color change can be seen
            y = x
            if node.data < x.data:
                x = x.left
            else:
                x = x.right

        if y is not None:
            y.aniQueue.put(Movement(-1, -1,self.step,['gray' if y.color == 0 else 'red']))

        # put node as either root or as left/right child of their parent
        node.parent = y
        if y == None:
            self.root = node
        elif node.data < y.data:
            y.left = node
        else:
            y.right = node

        # show node first on side of screen with color red
        self.animationList.append(node)
        node.aniQueue.put(Movement(-1,-1,self.step,[],[],['oval',100,200,self.size,str(node.data),'red']))

        # put node at root and return
        if node.parent == None:
            node.x = self.originx
            node.y = self.originy
            node.color = 0
            node.aniQueue.put(Movement(node.x,node.y,self.step,['gray']))
            self.step += 1
            return

        node.y = node.parent.y + self.yDist

        # put node as either left or right child of root, add the line, return
        if node.parent.parent == None:
            if node.parent.right == node:
                node.x = node.parent.x + (self.size * separators[self.getDepth(node) - 1])
                node.aniQueue.put(Movement(node.x,node.y,self.step))
                node.aniQueue.put(Movement(-1,-1,self.step,[],[node.x + 20, node.y, node.parent.x + self.size - 20, node.parent.y + self.size]))
            else:
                node.x = node.parent.x - (self.size * separators[self.getDepth(node) - 1])
                node.aniQueue.put(Movement(node.x,node.y,self.step))
                node.aniQueue.put(Movement(-1,-1,self.step,[],[node.x + self.size - 20, node.y, node.parent.x + 20, node.parent.y + self.size]))
            self.step += 1
            return

        # if node is past second level of the tree, put it where it should be then call insertHelper
        if node.parent.right == node:
            node.x = node.parent.x + (self.size * separators[self.getDepth(node) - 1])
            node.aniQueue.put(Movement(node.x,node.y,self.step))
            node.aniQueue.put(Movement(-1,-1,self.step,[],[node.x + 20, node.y, node.parent.x + self.size - 20, node.parent.y + self.size]))
        else:
            node.x = node.parent.x - (self.size * separators[self.getDepth(node) - 1])
            node.aniQueue.put(Movement(node.x,node.y,self.step))
            node.aniQueue.put(Movement(-1,-1,self.step,[],[node.x + self.size - 20, node.y, node.parent.x + 20, node.parent.y + self.size]))
        
        self.insertHelper(node)
        self.step += 1

    def insertHelper(self, node):
        while node.parent.color == 1:
            if node.parent == node.parent.parent.right:
                u = node.parent.parent.left
                if u.color == 1:
                    u.color = 0
                    u.aniQueue.put(Movement(-1, -1,self.step, ['gray']))
                    node.parent.color = 0
                    node.parent.aniQueue.put(Movement(-1, -1,self.step, ['gray']))
                    node.parent.parent.color = 1
                    node.parent.parent.aniQueue.put(Movement(-1, -1,self.step, ['red']))
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self.rightRotate(node)
                    node.parent.color = 0
                    node.parent.aniQueue.put(Movement(-1, -1,self.step, ['gray']))
                    node.parent.parent.color = 1
                    node.parent.parent.aniQueue.put(Movement(-1, -1,self.step, ['red']))
                    self.leftRotate(node.parent.parent)
            else:
                u = node.parent.parent.right
                if u.color == 1:
                    u.color = 0
                    u.aniQueue.put(Movement(-1, -1,self.step, ['gray']))
                    node.parent.color = 0
                    node.parent.aniQueue.put(Movement(-1, -1,self.step, ['gray']))
                    node.parent.parent.color = 1
                    node.parent.parent.aniQueue.put(Movement(-1, -1,self.step, ['red']))
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        node = node.parent
                        self.leftRotate(node)
                    node.parent.color = 0
                    node.parent.aniQueue.put(Movement(-1, -1,self.step, ['gray']))
                    node.parent.parent.color = 1
                    node.parent.parent.aniQueue.put(Movement(-1, -1,self.step, ['red']))
                    self.rightRotate(node.parent.parent)
            
            if node == self.root:
                break
                
        # make sure root node is always black
        self.root.color = 0
        self.root.aniQueue.put(Movement(-1, -1,self.step, ['gray']))

    def leftRotate(self, node):
        separators = [0, 4, 2, 1, .5, .5]
        y = node.right
        node.right = y.left
        if y.left != self.NULL:
            y.left.parent = node
        y.parent = node.parent

        # set y's coordinates
        if node.parent == None:
            y.x = self.root.x
            y.y = self.root.y
            self.root = y
        elif node == node.parent.left:
            node.parent.left = y
        else:
            node.parent.right = y
        y.left = node
        node.parent = y

        # logic code is done here

        self.root.aniQueue.put(Movement(self.root.x, self.root.y,self.step, ['delete_line']))

        # if there are other children that need to be moved,
        # delete all existing lines and change coordinates to either left or right children of their parents
        # continue iterating through the entire tree and all the children
        z = self.root.left
        while z != self.NULL:
            z.aniQueue.put(Movement(z.x, z.y,self.step, ['delete_line']))
            z.x = z.parent.x - (self.size * separators[self.getDepth(z) - 1])
            z.y = z.parent.y + self.yDist
            k = z.right
            while k != self.NULL:
                k.aniQueue.put(Movement(k.x, k.y,self.step, ['delete_line']))
                k.x = k.parent.x + (self.size * separators[self.getDepth(k) - 1])
                k.y = k.parent.y + self.yDist
                j = k.left
                while j != self.NULL:
                    j.aniQueue.put(Movement(j.x, j.y,self.step, ['delete_line']))
                    j.x = j.parent.x - (self.size * separators[self.getDepth(j) - 1])
                    j.y = j.parent.y + self.yDist
                    j = j.left
                k = k.right
            z = z.left
        z = self.root.right
        while z != self.NULL:
            z.aniQueue.put(Movement(z.x, z.y,self.step, ['delete_line']))
            z.x = z.parent.x + (self.size * separators[self.getDepth(z) - 1])
            z.y = z.parent.y + self.yDist
            k = z.left
            while k != self.NULL:
                k.aniQueue.put(Movement(k.x, k.y,self.step, ['delete_line']))
                k.x = k.parent.x - (self.size * separators[self.getDepth(k) - 1])
                k.y = k.parent.y + self.yDist
                j = k.right
                while j != self.NULL:
                    j.aniQueue.put(Movement(j.x, j.y,self.step, ['delete_line']))
                    j.x = j.parent.x + (self.size * separators[self.getDepth(j) - 1])
                    j.y = j.parent.y + self.yDist
                    j = j.right
                k = k.left
            z = z.right

        # put root where it's going 
        self.root.aniQueue.put(Movement(self.root.x,self.root.y,self.step,[],[],[]))
        # move everything to the left of root where it should be based on their coordinates
        # and add lines
        z = self.root.left
        while z != self.NULL:
            z.aniQueue.put(Movement(-1,-1,self.step,[],[z.x + self.size - 20, z.y, z.parent.x + 20, z.parent.y + self.size]))
            z.aniQueue.put(Movement(z.x,z.y,self.step,[],[],[]))
            k = z.right
            while k != self.NULL:
                k.aniQueue.put(Movement(-1,-1,self.step,[],[k.x + 20, k.y, k.parent.x + self.size - 20, k.parent.y + self.size]))
                k.aniQueue.put(Movement(k.x,k.y,self.step,[],[],[]))
                j = k.left
                while j != self.NULL:
                    j.aniQueue.put(Movement(-1,-1,self.step,[],[j.x + self.size - 20, j.y, j.parent.x + 20, j.parent.y + self.size]))
                    j.aniQueue.put(Movement(j.x,j.y,self.step,[],[],[]))
                    j = j.left
                k = k.right
            z = z.left
        # move everything to the right of root where it should be based on their coordinates
        # and add lines
        z = self.root.right
        while z != self.NULL:
            z.aniQueue.put(Movement(-1,-1,self.step,[],[z.x + 20, z.y, z.parent.x + self.size - 20, z.parent.y + self.size]))
            z.aniQueue.put(Movement(z.x,z.y,self.step,[],[],[]))
            k = z.left
            while k != self.NULL:
                k.aniQueue.put(Movement(-1,-1,self.step,[],[k.x + self.size - 20, k.y, k.parent.x + 20, k.parent.y + self.size]))
                k.aniQueue.put(Movement(k.x,k.y,self.step,[],[],[]))
                j = k.right
                while j != self.NULL:
                    j.aniQueue.put(Movement(-1,-1,self.step,[],[j.x + 20, j.y, j.parent.x + self.size - 20, j.parent.y + self.size]))
                    j.aniQueue.put(Movement(j.x,j.y,self.step,[],[],[]))
                    j = j.right
                k = k.left
            z = z.right

    def rightRotate(self, node):
        separators = [0, 4, 2, 1, .5, .5]
        y = node.left
        node.left = y.right
        if y.right != self.NULL:
            y.right.parent = node
        y.parent = node.parent

        # set y's coordinates
        if node.parent == None:
            y.x = self.root.x
            y.y = self.root.y
            self.root = y
        elif node == node.parent.right:
            node.parent.right = y
        else:
            node.parent.left = y
        y.right = node
        node.parent = y

        # logic code is done here

        self.root.aniQueue.put(Movement(self.root.x, self.root.y,self.step, ['delete_line']))

        # if there are other children that need to be moved,
        # delete all existing lines and change coordinates to either left or right children of their parents
        # continue iterating through the entire tree and all the children
        z = self.root.left
        while z != self.NULL:
            z.aniQueue.put(Movement(z.x, z.y,self.step, ['delete_line']))
            z.x = z.parent.x - (self.size * separators[self.getDepth(z) - 1])
            z.y = z.parent.y + self.yDist
            k = z.right
            while k != self.NULL:
                k.aniQueue.put(Movement(k.x, k.y,self.step, ['delete_line']))
                k.x = k.parent.x + (self.size * separators[self.getDepth(k) - 1])
                k.y = k.parent.y + self.yDist
                j = k.left
                while j != self.NULL:
                    j.aniQueue.put(Movement(j.x, j.y,self.step, ['delete_line']))
                    j.x = j.parent.x - (self.size * separators[self.getDepth(j) - 1])
                    j.y = j.parent.y + self.yDist
                    j = j.left
                k = k.right
            z = z.left
        z = self.root.right
        while z != self.NULL:
            z.aniQueue.put(Movement(z.x, z.y,self.step, ['delete_line']))
            z.x = z.parent.x + (self.size * separators[self.getDepth(z) - 1])
            z.y = z.parent.y + self.yDist
            k = z.left
            while k != self.NULL:
                k.aniQueue.put(Movement(k.x, k.y,self.step, ['delete_line']))
                k.x = k.parent.x - (self.size * separators[self.getDepth(k) - 1])
                k.y = k.parent.y + self.yDist
                j = k.right
                while j != self.NULL:
                    j.aniQueue.put(Movement(j.x, j.y,self.step, ['delete_line']))
                    j.x = j.parent.x + (self.size * separators[self.getDepth(j) - 1])
                    j.y = j.parent.y + self.yDist
                    j = j.right
                k = k.left
            z = z.right

        # put root where it's going
        self.root.aniQueue.put(Movement(self.root.x,self.root.y,self.step,[],[],[]))
        # move everything to the left of root where it should be based on their coordinates
        # and add lines
        z = self.root.left
        while z != self.NULL:
            z.aniQueue.put(Movement(-1,-1,self.step,[],[z.x + self.size - 20, z.y, z.parent.x + 20, z.parent.y + self.size]))
            z.aniQueue.put(Movement(z.x,z.y,self.step,[],[],[]))
            k = z.right
            while k != self.NULL:
                k.aniQueue.put(Movement(-1,-1,self.step,[],[k.x + 20, k.y, k.parent.x + + self.size - 20, k.parent.y + self.size]))
                k.aniQueue.put(Movement(k.x,k.y,self.step,[],[],[]))
                j = k.left
                while j != self.NULL:
                    j.aniQueue.put(Movement(-1,-1,self.step,[],[j.x + self.size - 20, j.y, j.parent.x + 20, j.parent.y + self.size]))
                    j.aniQueue.put(Movement(j.x,j.y,self.step,[],[],[]))
                    j = j.left
                k = k.right
            z = z.left
        # move everything to the right of root where it should be based on their coordinates
        # and add lines
        z = self.root.right
        while z != self.NULL:
            z.aniQueue.put(Movement(-1,-1,self.step,[],[z.x + 20, z.y, z.parent.x + self.size - 20, z.parent.y + self.size]))
            z.aniQueue.put(Movement(z.x,z.y,self.step,[],[],[]))
            k = z.left
            while k != self.NULL:
                k.aniQueue.put(Movement(-1,-1,self.step,[],[k.x + self.size - 20, k.y, k.parent.x + 20, k.parent.y + self.size]))
                k.aniQueue.put(Movement(k.x,k.y,self.step,[],[],[]))
                j = k.right
                while j != self.NULL:
                    j.aniQueue.put(Movement(-1,-1,self.step,[],[j.x + 20, j.y, j.parent.x + self.size - 20, j.parent.y + self.size]))
                    j.aniQueue.put(Movement(j.x,j.y,self.step,[],[],[]))
                    j = j.right
                k = k.left
            z = z.right

    def getDepth(self, node):
        depth = 0
        while node is not None:
            depth += 1
            node = node.parent
        return depth
    
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
        originx = 600
        originy = 25
        # step = 0
        yDist = 75
        size = 50

        bst = RBTree(aniList, originx, originy, yDist, size)
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
            bst.insert(myList[placeHolder].userNum)
            placeHolder += 1

        # while 1:
            # if delete button pressed:
                # add the value to myList?? 
                # bst.delete(value written in box, myList, step, size, placeHolder)
            # if insert button pressed:
                # add value written in box to myList
                # step += 1
                # bst.insert(myList[placeHolder].userNum, step)
                # placeHolder += 1
            # if exit button pushed
                # return 0??