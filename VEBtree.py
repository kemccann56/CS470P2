from math import log, ceil, floor
import animation
from queue import Queue

step = 0

class VEBanimation():
    def __init__(self, aniQueue, size, text, x, y, orginx, orginy, linex=None, liney=None):
        self.min = animation.Object(0)
        self.max = animation.Object(0)
        aniQueue.append(self.min)
        aniQueue.append(self.max)

        self.summary = None
        self.clusters = dict()

        self.maxAni = None
        self.minAni = None

        self.min.aniQueue.put(animation.Movement(-1,-1,0,[],[],['rectangle',orginx+x,orginy+y,size,text,'lightblue']))
        self.max.aniQueue.put(animation.Movement(-1,-1,0,[],[],['rectangle',orginx+x+size,orginy+y,size,text,'lightblue']))
        if linex:
            self.min.aniQueue.put(animation.Movement(-1,-1,0,[],[x+size+orginx, y+orginy, linex+orginx, liney+orginy]))

class VanEmdeBoasTree:
    """
    Van Emde Boas Tree.
    """

    def __init__(self, valueRange, animationTree=None):
        """
        Generates an empty veb-tree with the given
        range.
        """
        bitSize = ceil(log(valueRange, 2))
        self.valueRange =  1 << bitSize
        self.min = None
        self.max = None
        if self.valueRange > 2:
            halfBitSize = bitSize/2

            self.summary = None
            self.cluster = dict()
            self.lsbSize = floor(halfBitSize)
            self.lsqrt = 1 << self.lsbSize
            self.hsqrt = 1 << ceil(halfBitSize) 
            self.lsbMask = self.lsqrt - 1
        self.aniTree = animationTree


    def clusterIndex(self, x):
        """
        Returns the index of the cluster holding x.
        """
        return x >> self.lsbSize 


    def valueIndex(self, x):
        """
        Returns the index of x inside its cluster.
        """
        return x & self.lsbMask 


    def value(self, clusterIndex, valueIndex):
        """
        Returns the value associated with the pair
        (clusterIndex, valueIndex).
        """
        return (clusterIndex << self.lsbSize) + valueIndex


    def contains(self, x, curAniCluster):
        global step
        """
        Checks whether x is present in the veb-tree.
        """
        curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['yellow']))
        curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['yellow']))
        step += 1
        if self.min == x:
            curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['green']))
            curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
            step += 1
            curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
            step += 1
            return True
        if self.max == x:
            curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
            curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['green']))
            step += 1
            curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
            step += 1
            return True

        if self.min == None:
            curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['red']))
            curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['red']))
            step += 1
            curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
            curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
            step += 1
            return False
        if x < self.min:
            curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['red']))
            curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
            step += 1
            curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
            step += 1
            return False
        if x > self.max:
            curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
            curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['red']))
            step += 1
            curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
            step += 1
            return False
        if self.valueRange == 2:
            curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['red']))
            curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['red']))
            step += 1
            curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
            curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
            step += 1
            return False

        curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
        curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
 
        xCluster = self.cluster.get(self.clusterIndex(x), None)
        return (xCluster != None) and xCluster.contains(self.valueIndex(x), curAniCluster.clusters[self.clusterIndex(x)])


    def predecessor(self, x):
        """
        Returns the predecessor of x in the veb-tree.
        """
        if self.valueRange == 2:
            return 0 if (x == 1 and self.min == 0) else None

        if self.max != None and x > self.max:
            return self.max

        xClusterIndex = self.clusterIndex(x)
        xCluster = self.cluster.get(xClusterIndex, None)
        xIndex = self.valueIndex(x)

        if xCluster != None and xCluster.min < xIndex:
            return self.value(xClusterIndex, xCluster.predecessor(xIndex))

        if self.summary != None:
            predClusterIndex = self.summary.predecessor(xClusterIndex)
            if predClusterIndex != None:
                return self.value(predClusterIndex, self.cluster[predClusterIndex].max)

        return self.min if (self.min != None and x > self.min) else None


    def successor(self, x):
        """
        Returns the successor of x in the veb-tree.
        """
        if self.valueRange == 2:
            return 1 if (x == 0 and self.max == 1) else None

        if self.min != None and x < self.min:
            return self.min

        xClusterIndex = self.clusterIndex(x)
        xCluster = self.cluster.get(xClusterIndex, None)
        xIndex = self.valueIndex(x)

        if xCluster != None and xCluster.max > xIndex:
            return self.value(xClusterIndex, xCluster.successor(xIndex))

        if self.summary != None:
            succClusterIndex = self.summary.successor(xClusterIndex)
            if succClusterIndex != None:
                return self.value(succClusterIndex, self.cluster[succClusterIndex].min)
        
        return self.max if (self.max != None and x < self.max) else None 


    def insert(self, x, curAniCluster, curValue):
        global step
        """
        Inserts value x into the veb-tree.
        """
        curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['yellow']))
        curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['yellow']))
        step += 1
        if x == self.min:
            curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['green']))
            curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
            step += 1
            curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
            step += 1
            return
        if x == self.max:
            curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
            curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['green']))
            step += 1
            curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
            step += 1
            return

        if self.min == None:
            curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['green']))
            curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['green']))
            curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['change_text', str(curValue)]))
            curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['change_text', str(curValue)]))
            curAniCluster.minAni = curValue
            curAniCluster.maxAni = curValue
            step += 1
            curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
            curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
            step += 1
            self.min = self.max = x
            return

        if self.min == self.max:
            if x < self.min:
                curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['green']))
                curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
                curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['change_text', str(curValue)]))
                curAniCluster.minAni = curValue
                step += 1
                curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
                step += 1
                self.min = x
            elif x > self.max:
                curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
                curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['green']))
                curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['change_text', str(curValue)]))
                curAniCluster.maxAni = curValue
                step += 1
                curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
                step += 1
                self.max = x
            return

        if self.valueRange == 2:
            #This case should never happen
            return

        if x < self.min:
            curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['purple']))
            curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
            step += 1
            curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['change_text', str(curValue)]))
            curValue, curAniCluster.minAni = curAniCluster.minAni, curValue
            step += 1
            self.min, x = x, self.min

        elif x > self.max:
            curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
            curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['purple']))
            step += 1
            curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['change_text', str(curValue)]))
            curValue, curAniCluster.maxAni = curAniCluster.maxAni, curValue
            step += 1
            self.max, x = x, self.max

        xClusterIndex = self.clusterIndex(x)
        xCluster = self.cluster.get(xClusterIndex, None)
        xIndex = self.valueIndex(x)

        if xCluster == None:
            if self.summary == None:
                self.summary = VanEmdeBoasTree(self.hsqrt)
            self.summary.insert(xClusterIndex, curAniCluster.summary, xClusterIndex)

            xCluster = VanEmdeBoasTree(self.lsqrt)
            self.cluster[xClusterIndex] = xCluster
        
        curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
        curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
        step += 1

        xCluster.insert(xIndex, curAniCluster.clusters[xClusterIndex], curValue)


    def delete(self, x, curAniCluster):
        global step
        """
        Deletes x from the veb-tree.
        """
        curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['yellow']))
        curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['yellow']))
        step += 1
        if self.min == None or x < self.min or x > self.max:
            curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['red']))
            curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['red']))
            step += 1
            curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
            curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
            step += 1
            return

        if self.min == self.max:
            curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['green']))
            curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['green']))
            curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['change_text', 'null']))
            curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['change_text', 'null']))
            step += 1
            curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
            curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
            step += 1
            self.min = self.max = None
            return

        if self.valueRange == 2:
            if x == 0:
                curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['green']))
                curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
                curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['change_text', str(curAniCluster.maxAni)]))
                step += 1
                curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
                step += 1
                self.min = 1
            else:
                curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
                curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['green']))
                curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['change_text', str(curAniCluster.minAni)]))
                step += 1
                curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
                step += 1
                self.max = 0
            return

        if x == self.min:
            curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['green']))
            curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
            step += 1
            if self.summary == None:
                curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['change_text', str(curAniCluster.maxAni)]))
                curAniCluster.minAni = curAniCluster.maxAni
                step += 1
                curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
                step += 1
                self.min = self.max
                return

            xClusterIndex = self.summary.min
            xCluster = self.cluster[xClusterIndex]
            xIndex = xCluster.min

            curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['change_text', str(curAniCluster.clusters[xClusterIndex].minAni)]))
            curAniCluster.minAni = curAniCluster.clusters[xClusterIndex].minAni
            step += 1
            self.min = self.value(xClusterIndex, xIndex)

        elif x == self.max:
            curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
            curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['green']))
            step += 1
            if self.summary == None:
                curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['change_text', str(curAniCluster.minAni)]))
                curAniCluster.maxAni = curAniCluster.minAni
                step += 1
                curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
                step += 1
                self.max = self.min
                return

            xClusterIndex = self.summary.max
            xCluster = self.cluster[xClusterIndex]
            xIndex = xCluster.max

            curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['change_text', str(curAniCluster.clusters[xClusterIndex].maxAni)]))
            curAniCluster.maxAni = curAniCluster.clusters[xClusterIndex].maxAni
            step += 1
            self.max = self.value(xClusterIndex, xIndex)

        else:
            xClusterIndex = self.clusterIndex(x)
            xCluster = self.cluster.get(xClusterIndex, None)
            xIndex = self.valueIndex(x)
            if xCluster == None:
                curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
                curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
                step += 1
                return

        xCluster.delete(xIndex, curAniCluster.clusters[xClusterIndex])

        if xCluster.min == None:
            del self.cluster[xClusterIndex]
            self.summary.delete(xClusterIndex, curAniCluster.summary)

            if self.summary.min == None:
                self.summary = None

        curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
        curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
        step += 1


    def __iter__(self):
        """
        Iterator over the elements in the veb-tree.
        """
        value = self.min
        while value != None:
            yield value 
            value = self.successor(value)


    def __str__(self):
        """
        Returns a string representing the veb-tree.
        """
        return str(tuple(value for value in self))


    def __repr__(self):
        """
        Represents the veb-tree.
        """
        return str(self)


def startVEBtree(aniQueue, orginx, orginy, screen_width, screen_height, commandQueue):
    global step
    size = screen_height//9
###Draw Tree Start
    #Root Node
    VEBtreeAni =  VEBanimation(aniQueue, size, 'null', screen_width//2 - size, 0, orginx, orginy)  
    VEBtreeAni.summary = VEBanimation(aniQueue, size, 'null', screen_width//6 - size, size * 2, orginx, orginy, screen_width//2, size)
    temp = animation.Object(0)
    aniQueue.append(temp)
    temp.aniQueue.put(animation.Movement(-1,-1,0,[],[],['truerectangle',orginx+screen_width//6 - size,orginy+size*1.3,size,'summary','pink']))
    VEBtreeAni.clusters[0] = VEBanimation(aniQueue, size, 'null', (screen_width//6) * 2 - size, size * 2, orginx, orginy, screen_width//2, size)
    VEBtreeAni.clusters[1] = VEBanimation(aniQueue, size, 'null', (screen_width//6) * 3 - size, size * 2, orginx, orginy, screen_width//2, size)
    VEBtreeAni.clusters[2] = VEBanimation(aniQueue, size, 'null', (screen_width//6) * 4 - size, size * 2, orginx, orginy, screen_width//2, size)
    VEBtreeAni.clusters[3] = VEBanimation(aniQueue, size, 'null', (screen_width//6) * 5 - size, size * 2, orginx, orginy, screen_width//2, size)

    #Root summary
    VEBtreeAni.summary.summary = VEBanimation(aniQueue, size, 'null', (screen_width//14) - size, size * 4, orginx, orginy, screen_width//6, size * 3)
    temp1 = animation.Object(0)
    aniQueue.append(temp1)
    temp1.aniQueue.put(animation.Movement(-1,-1,0,[],[],['truerectangle',orginx+screen_width//14 - size,orginy+size*3.3,size,'summary','pink']))
    VEBtreeAni.summary.clusters[0] = VEBanimation(aniQueue, size, 'null', (screen_width//14) * 2 - size, size * 4, orginx, orginy, screen_width//6, size * 3)
    VEBtreeAni.summary.clusters[1] = VEBanimation(aniQueue, size, 'null', (screen_width//14) * 3 - size, size * 4, orginx, orginy, screen_width//6, size * 3)

    #Root cluster[0]
    VEBtreeAni.clusters[0].summary = VEBanimation(aniQueue, size, 'null', (screen_width//14) * 4 - size, size * 4, orginx, orginy, screen_width//6 * 2, size * 3)
    temp2 = animation.Object(0)
    aniQueue.append(temp2)
    temp2.aniQueue.put(animation.Movement(-1,-1,0,[],[],['truerectangle',orginx+screen_width//14 * 4 - size,orginy+size*3.3,size,'summary','pink']))
    VEBtreeAni.clusters[0].clusters[1] = VEBanimation(aniQueue, size, 'null', (screen_width//14) * 5 - size, size * 4, orginx, orginy, screen_width//6 * 2, size * 3)

    #Root cluster[1]
    VEBtreeAni.clusters[1].summary = VEBanimation(aniQueue, size, 'null', (screen_width//14) * 6 - size, size * 4, orginx, orginy, screen_width//6 * 3, size * 3)
    temp3 = animation.Object(0)
    aniQueue.append(temp3)
    temp3.aniQueue.put(animation.Movement(-1,-1,0,[],[],['truerectangle',orginx+screen_width//14 * 6 - size,orginy+size*3.3,size,'summary','pink']))
    VEBtreeAni.clusters[1].clusters[0] = VEBanimation(aniQueue, size, 'null', (screen_width//14) * 7 - size, size * 4, orginx, orginy, screen_width//6 * 3, size * 3)
    VEBtreeAni.clusters[1].clusters[1] = VEBanimation(aniQueue, size, 'null', (screen_width//14) * 8 - size, size * 4, orginx, orginy, screen_width//6 * 3, size * 3)

    #Root cluster[2]
    VEBtreeAni.clusters[2].summary = VEBanimation(aniQueue, size, 'null', (screen_width//14) * 9 - size, size * 4, orginx, orginy, screen_width//6 * 4, size * 3)
    temp4 = animation.Object(0)
    aniQueue.append(temp4)
    temp4.aniQueue.put(animation.Movement(-1,-1,0,[],[],['truerectangle',orginx+screen_width//14 * 9 - size,orginy+size*3.3,size,'summary','pink']))
    VEBtreeAni.clusters[2].clusters[0] = VEBanimation(aniQueue, size, 'null', (screen_width//14) * 10 - size, size * 4, orginx, orginy, screen_width//6 * 4, size * 3)
    VEBtreeAni.clusters[2].clusters[1] = VEBanimation(aniQueue, size, 'null', (screen_width//14) * 11 - size, size * 4, orginx, orginy, screen_width//6 * 4, size * 3)

    #Root cluster[3]
    VEBtreeAni.clusters[3].summary = VEBanimation(aniQueue, size, 'null', (screen_width//14) * 12 - size, size * 4, orginx, orginy, screen_width//6 * 5, size * 3)
    temp5 = animation.Object(0)
    aniQueue.append(temp5)
    temp5.aniQueue.put(animation.Movement(-1,-1,0,[],[],['truerectangle',orginx+screen_width//14 * 12 - size,orginy+size*3.3,size,'summary','pink']))
    VEBtreeAni.clusters[3].clusters[0] = VEBanimation(aniQueue, size, 'null', (screen_width//14) * 13 - size, size * 4, orginx, orginy, screen_width//6 * 5, size * 3)
    
    ###Draw Tree End
    step += 1

    VEBtree = VanEmdeBoasTree(16, VEBtreeAni)
    
    #for i in range(16):
    #    print(i)
    #    VEBtree.insert(i, VEBtreeAni)
    #for i in range(16):
    #    print(i)
    #    VEBtree.delete(i, VEBtreeAni)

    while 1:
        step = 0
        command = commandQueue.get()
        print(command[0])
        if command[0] == 'break':
            break
        elif command[0] == 'insert':
            VEBtree.insert(int(command[1]), VEBtreeAni, int(command[1]))
        elif command[0] == 'delete':
            VEBtree.delete(int(command[1]), VEBtreeAni)
        elif command[0] == 'search':
            VEBtree.contains(int(command[1]), VEBtreeAni)
