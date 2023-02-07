import sys

class Node():
    def __init__(self, data):
        self.data = data
        self.parent = None
        self.left = None
        self.right = None
        self.color = 1 # 1 = red, 0 = black

class RBTree():
    def __init__(self):
        self.NULL = Node(0)
        self.NULL.color = 0
        self.NULL.left = None
        self.NULL.right = None
        self.root = self.NULL

    def search(self, k):
        return self.searchHelper(self.root, k)

    def searchHelper(self, node, val):
        if node == self.NULL or val == node.data:
            return node
        if val < node.data:
            return self.searchHelper(node.left, val)

        return self.searchHelper(node.right, val)

    def leftRotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.NULL:
            y.left.parent = x

        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def rightRotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.NULL:
            y.right.parent = x

        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y
    
    def insertHelper(self, val):
        while val.parent.color == 1:
            if val.parent == val.parent.parent.right:
                u = val.parent.parent.left
                if u.color == 1:
                    u.color = 0
                    val.parent.color = 0
                    val.parent.parent.color = 1
                    val = val.parent.parent
                else:
                    if val == val.parent.left:
                        val = val.parent
                        self.rightRotate(val)
                    val.parent.color = 0
                    val.parent.parent.color = 1
                    self.leftRotate(val.parent.parent)
            else:
                u = val.parent.parent.right

                if u.color == 1:
                    u.color = 0
                    val.parent.color = 0
                    val.parent.parent.color = 1
                    val = val.parent.parent
                else:
                    if val == val.parent.right:
                        val = val.parent
                        self.leftRotate(val)
                    val.parent.color = 0
                    val.parent.parent.color = 1
                    self.rightRotate(val.parent.parent)
            
            if val == self.root:
                break
                
        self.root.color = 0

    def insert(self, val):
        node = Node(val)
        node.parent = None
        node.data = val
        node.left = self.NULL
        node.right = self.NULL
        node.color = 1

        y = None
        x = self.root

        while x != self.NULL:
            y = x
            if node.data < x.data:
                x = x.left
            else:
                x = x.right

        node.parent = y
        if y == None:
            self.root = node
        elif node.data < y.data:
            y.left = node
        else:
            y.right = node

        if node.parent == None:
            node.color = 0
            return

        if node.parent.parent == None:
            return

        self.insertHelper(node) 

    def fixInsert(self, k):
        while k.parent.color == 1:
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left
                if u.color == 1:
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self.rightRotate(k)
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self.leftRotate(k.parent.parent)
            else:
                u = k.parent.parent.right

                if u.color == 1:
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self.leftRotate(k)
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self.rightRotate(k.parent.parent)
            if k == self.root:
                break
        self.root.color = 0
    
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

if __name__ == "__main__":
    bst = RBTree()
    # bst.insert(5)
    # bst.insert(15)
    # bst.insert(25)
    # bst.insert(35)
    # bst.insert(45)
    # bst.insert(50)
    # bst.insert(55)
    # bst.insert(65)
    # bst.insert(75)
    # bst.insert(80)
    # bst.insert(85)
    bst.insert(10)
    bst.insert(8)
    bst.insert(12)
    bst.print()