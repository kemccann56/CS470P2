class Node:
    #Objects: leftChild, rightChild, parent, isRed, value
    def __init__(self, value):
        self.leftChild = None
        self.rightChild = None
        self.parent = None
        self.isRed = True      #red on creation
        self.value = value

class RBTree:
    #Objects: nil, root 
    def __init__(self):
        self.nil = Node(-1) #nil refers to all nil nodes, -1 value is obsolete, nil pointers circularly point to itself
        self.nil.leftChild = self.nil
        self.nil.rightChild = self.nil
        self.nil.parent = self.nil
        self.root = self.nil
        self.nil.isRed = False
    
    #Operation 1: Search

    #in this imp, key/value are equal
    def search(self, key): 
        self.searchHelper(self.root, key) 

    #pass in self for refrence to nil node, returns entire node
    def searchHelper(self, temp, key): 
        if temp == self.nil or temp.value == key:
            return temp
        
        elif temp.value < key:
            return self.searchHelper(temp.rightChild, key)

        else:
             return self.searchHelper(temp.leftChild, key)

    #Operation 2: Insert

    #z is value of node needing to be inserted
    def insert(self, zValue):
        z = Node(zValue)
        y = self.nil
        x = self.root
        while x != self.root:
            y = x
            if z.value < x.value:
                x = x.leftChild
            else:
                 x = x.rightChild
        z.parent = y
        if y == self.nil:
            self.root = z
        elif z.value < y.value:
            y.leftChild = z
        else:
            y.rightChild = z
        z.leftChild = self.nil
        z.rightChild = self.nil
        self.insertFixup(z)

    def insertFixup(self, z):
        while z.parent.isRed == True:
            if z.parent == z.parent.parent.leftChild:
                pass
                #TODO Finish function and insert functionality



















def main():
    pass

if __name__ == "__main__":
    main()