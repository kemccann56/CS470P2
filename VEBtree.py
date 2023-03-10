"""
VEB Tree Animation Implementation
Group 3: Andrew Hankins, Alex Reese, Manjiri Gunaji, Kyle McCann, Nicholas Callahan
Luke Lindsay, and Shelby Deerman

References:
-----------
https://github.com/jhomswk/Van_Emde_Boas_Tree
https://www.youtube.com/watch?v=hmReJCupbNU
"""
from math import log, ceil, floor
import animation
from queue import Queue

step = 0

class VEBanimation():
    """
    Object that creates and links the animation pieces together
    """
    def __init__(self, aniQueue, size, text, x, y, orginx, orginy, linex=None, liney=None):
        """
        Arguments:
        ----------
        aniQueue : queue
            Queue of animation operations to be performed
        size : int
            Horizontal component for formatting animation component locations
        text : str
            Text for placement in the generated object
        x : int
            X coordinate for the animation component
        y : int
            Y coordinate for the animation component
        originx : int
            Origin in the horizontal direction
        originy : int
            Origin in the vertical direction
        linex : int
            Horizontal location of the line's start point
        liney : int
            Vertical location of the line's end point
        
        """
        # add animation min and max
        self.min = animation.Object(0)
        self.max = animation.Object(0)
        # add them to end of queue
        aniQueue.append(self.min)
        aniQueue.append(self.max)

        # start with empty summary VEB
        self.summary = None
        # include mapping to animation clusters
        self.clusters = dict()

        # include animation max and minimum
        self.maxAni = None
        self.minAni = None

        # add the rectangles defined by arguments into the queue
        self.min.aniQueue.put(animation.Movement(-1,-1,0,[],[],['rectangle',orginx+x,orginy+y,size,text,'lightblue']))
        self.max.aniQueue.put(animation.Movement(-1,-1,0,[],[],['rectangle',orginx+x+size,orginy+y,size,text,'lightblue']))
        # if a line is needed, start it
        if linex:
            self.min.aniQueue.put(animation.Movement(-1,-1,0,[],[x+size+orginx, y+orginy, linex+orginx, liney+orginy]))

class VanEmdeBoasTree:
    """
    Van Emde Boas Tree.
    Attributes:
    -----------
    min : int
        Minimum value for the entire class
    max : int
        Maximum value for the entire class
    valueRange : int
        Number of clusters in the tree
    summary : VanEmdeBoasTree
        VEB tree tracking locations of elements in the primary tree
    cluster : dict
        Stores references to the child VEB Trees, keys are calculated integers corresponding
        to appropriate locations in an integer array of the full valueRange, values are VEB Trees
        in the same layer
    """

    def __init__(self, valueRange, animationTree=None):
        """
        Generates an empty veb-tree with the given
        range.
        Arguments:
        ----------
        valueRange : int
            Universe size for the tree, total number of integers in the array
        animationTree : VEBanimation
            Reference to class for operating the animation
        """
        # calculate the new sizes/ranges for the layer
        bitSize = ceil(log(valueRange, 2))
        self.valueRange =  1 << bitSize
        # Min and Max are initially empty
        self.min = None
        self.max = None
        # cases when the tree being generated is in the bottom layer
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
        Arguments:
        ----------
        x : int
            Value whose cluster is being located
        
        Returns: int
        """
        return x >> self.lsbSize


    def valueIndex(self, x):
        """
        Returns the index of x inside its cluster.
        Arguments:
        ----------
        x : int
            Value whose location within the cluster is being located
        
        Returns: int
        """
        return x & self.lsbMask


    def value(self, clusterIndex, valueIndex):
        """
        Returns the value associated with the pair
        (clusterIndex, valueIndex).
        Arguments:
        ----------
        clusterIndex : int
            Location of the desired cluster
        valueIndex : int
            Location within the desired cluster
        
        Returns: int
        """
        return (clusterIndex << self.lsbSize) + valueIndex


    def contains(self, x, curAniCluster):
        global step
        """
        Checks whether x is present in the VEB tree.
        Arguments:
        ----------
        x : int
            Value being searched for in the VEB tree
        curAniCluster : VEBanimation
            Animation object corresponding to the current cluster location in the full animation tree

        Returns: bool
        """
        # once cluster is opened in animation, color it yellow
        curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['yellow']))
        curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['yellow']))
        step += 1
        # if the minimum is equal to the searched value, highlight green in animation and return True
        if self.min == x: 
            curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['green']))
            curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
            step += 1
            curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
            step += 1
            return True
        # if the maximum is equal to the searched value, highlight in animation and return True
        if self.max == x:
            curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
            curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['green']))
            step += 1
            curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
            step += 1
            return True
        # if min is None, meaning the searched cluster is empty, highlight red and return False
        if self.min == None:
            curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['red']))
            curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['red']))
            step += 1
            curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
            curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
            step += 1
            return False
        # if value is less than the minimum of the node, highlight red and return False
        if x < self.min:
            curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['red']))
            curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
            step += 1
            curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
            step += 1
            return False
        # if the value is greater than the maximum of the node, highlight red and return False
        if x > self.max:
            curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
            curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['red']))
            step += 1
            curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
            step += 1
            return False
        # if the layer being reached is the final layer, highlight red and return False
        if self.valueRange == 2:
            curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['red']))
            curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['red']))
            step += 1
            curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
            curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
            step += 1
            return False

        # otherwise, move to next appropriate cluster in the next layer of the tree
        curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
        curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))

        xCluster = self.cluster.get(self.clusterIndex(x), None)
        return (xCluster != None) and xCluster.contains(self.valueIndex(x), curAniCluster.clusters[self.clusterIndex(x)])


    def predecessor(self, x):
        """
        Returns the predecessor of x in the veb-tree.
        Arguments:
        ----------
        x : int
            Value whose predecessor is being searched for

        Returns : Union[int, None]
        """
        # return either 0 or None if reaching the final layer
        if self.valueRange == 2:
            return 0 if (x == 1 and self.min == 0) else None

        # return the maximum if value is greater than the maximum
        if self.max != None and x > self.max:
            return self.max

        # get location of the value for determining next checks
        xClusterIndex = self.clusterIndex(x)
        xCluster = self.cluster.get(xClusterIndex, None)
        xIndex = self.valueIndex(x)

        # get predecessor within the value's cluster
        if xCluster != None and xCluster.min < xIndex:
            return self.value(xClusterIndex, xCluster.predecessor(xIndex))

        # if the value is the minimum, the predecessor must be the max of the next lowest cluster
        if self.summary != None:
            predClusterIndex = self.summary.predecessor(xClusterIndex)
            if predClusterIndex != None:
                return self.value(predClusterIndex, self.cluster[predClusterIndex].max)

        return self.min if (self.min != None and x > self.min) else None


    def successor(self, x):
        """
        Returns the successor of x in the veb-tree.
        Arguments:
        ----------
        x : int
            Value whose successor is being searched for

        Returns : Union[int, None]
        """
        # return either 0 or None if reaching the final layer
        if self.valueRange == 2:
            return 1 if (x == 0 and self.max == 1) else None

        # return the minimum if value is less than the minimum
        if self.min != None and x < self.min:
            return self.min

        # get location of the value for determining next checks
        xClusterIndex = self.clusterIndex(x)
        xCluster = self.cluster.get(xClusterIndex, None)
        xIndex = self.valueIndex(x)

        # get successor within the value's cluster
        if xCluster != None and xCluster.max > xIndex:
            return self.value(xClusterIndex, xCluster.successor(xIndex))

        # if the value is the maximum, the successor must be the min of the next highest cluster
        if self.summary != None:
            succClusterIndex = self.summary.successor(xClusterIndex)
            if succClusterIndex != None:
                return self.value(succClusterIndex, self.cluster[succClusterIndex].min)

        return self.max if (self.max != None and x < self.max) else None


    def insert(self, x, curAniCluster, curValue):
        global step
        """
        Inserts value x into the veb-tree.
        Arguments:
        ----------
        x : int
            Value being inserted into the VEB tree
        curAniCluster : VEBanimation
            Reference to animation object at current location in animation
        curValue : int
            The value of the current position for being propagated through the animation
        
        Returns: None
        """
        # highlight the location in the tree currently being analyzed
        curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['yellow']))
        curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['yellow']))
        step += 1
        # if the inserted value is already in the minimum of the tree, highlight green and return
        if x == self.min:
            curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['green']))
            curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
            step += 1
            curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
            step += 1
            return
        # if the inserted value is already in the maximum of the tree, highlight green and return
        if x == self.max:
            curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
            curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['green']))
            step += 1
            curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
            step += 1
            return
        # if the current tree location is empty, insert into that location and highlight green
        if self.min == None:
            # highlight green
            curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['green']))
            curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['green']))
            # update animation text
            curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['change_text', str(curValue)]))
            curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['change_text', str(curValue)]))
            # update animation values
            curAniCluster.minAni = curValue
            curAniCluster.maxAni = curValue
            step += 1
            curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
            curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
            step += 1
            # update tree values
            self.min = self.max = x
            return

        # if there is only one element in the tree location and ...
        if self.min == self.max:
            # the insertion value is lower than the value in the tree...
            if x < self.min:
                # highlight green
                curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['green']))
                curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
                # update animation text
                curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['change_text', str(curValue)]))
                # update animation value
                curAniCluster.minAni = curValue
                step += 1
                curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
                step += 1
                # update tree value
                self.min = x
            # the insertion value is greater than the value in the tree...
            elif x > self.max:
                # highlight green
                curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
                curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['green']))
                # update text
                curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['change_text', str(curValue)]))
                # update animation value
                curAniCluster.maxAni = curValue
                step += 1
                curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
                step += 1
                # update tree value
                self.max = x
            # break for all the above cases
            return

        if self.valueRange == 2:
            #This case should never happen
            return

        # if insertion value is less than the tree's minimum
        if x < self.min:
            # highlight purple
            curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['purple']))
            curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
            step += 1
            curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['change_text', str(curValue)]))
            # swap animation insertion and minimum values
            curValue, curAniCluster.minAni = curAniCluster.minAni, curValue
            step += 1
            # swap insertion and minimum values
            self.min, x = x, self.min

        # if insertion value is greater than the tree's maximum
        elif x > self.max:
            # highlight purple
            curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
            curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['purple']))
            step += 1
            curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['change_text', str(curValue)]))
            # swap animation maximum and insertion values
            curValue, curAniCluster.maxAni = curAniCluster.maxAni, curValue
            step += 1
            # swap maximum and insertion values
            self.max, x = x, self.max

        # get the next potential location of the insertion value in the tree
        xClusterIndex = self.clusterIndex(x)
        xCluster = self.cluster.get(xClusterIndex, None)
        xIndex = self.valueIndex(x)

        # if the expected location is not currently created
        if xCluster == None:
            # add a summary vector if not present
            if self.summary == None:
                self.summary = VanEmdeBoasTree(self.hsqrt)
            # update the summary
            self.summary.insert(xClusterIndex, curAniCluster.summary, xClusterIndex)

            # create a new cluster for mapping
            xCluster = VanEmdeBoasTree(self.lsqrt)
            # map the expected index to the newly created cluster
            self.cluster[xClusterIndex] = xCluster

        curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
        curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
        step += 1
        # insert into the next layer, constant time operation guaranteed
        xCluster.insert(xIndex, curAniCluster.clusters[xClusterIndex], curValue)


    def delete(self, x, curAniCluster):
        global step
        """
        Deletes x from the veb-tree.
        Arguments:
        ----------
        x : int
            Value being deleted from the VEB tree
        curAniCluster : VEBanimation
            Reference to animation object at current location in animation
        curValue : int
            The value of the current position for being propagated through the animation
        
        Returns: None
        """
        # highlight the location in the tree currently being analyzed
        curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['yellow']))
        curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['yellow']))
        step += 1
        # if tree is empty or delete value is outside the range of the tree
        if self.min == None or x < self.min or x > self.max:
            # highlight red and return
            curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['red']))
            curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['red']))
            step += 1
            curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
            curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
            step += 1
            return

        # if only one value exists in the cluster
        if self.min == self.max:
            # highlight green
            curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['green']))
            curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['green']))
            # update animation text
            curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['change_text', 'null']))
            curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['change_text', 'null']))
            step += 1
            curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
            curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
            step += 1
            # update tree value
            self.min = self.max = None
            return

        # if the last layer of the tree has been reached
        if self.valueRange == 2:
            # if the deletion value is equal to zero
            if x == 0:
                # highlight green
                curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['green']))
                curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
                curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['change_text', str(curAniCluster.maxAni)]))
                step += 1
                curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
                step += 1
                # update tree min
                self.min = 1
            # if the deletion value is equal to one
            else:
                # highlight green
                curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
                curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['green']))
                curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['change_text', str(curAniCluster.minAni)]))
                step += 1
                curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
                step += 1
                # update tree max
                self.max = 0
            return

        # if the deletion value is found to be the minimum of the tree
        if x == self.min:
            # highlight left side green
            curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['green']))
            curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
            step += 1
            # if the summary vector is nonexistent
            if self.summary == None:
                curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['change_text', str(curAniCluster.maxAni)]))
                # update animation min
                curAniCluster.minAni = curAniCluster.maxAni
                step += 1
                curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
                step += 1
                # update tree min/max
                self.min = self.max
                return

            # get the location of the value to be deleted
            xClusterIndex = self.summary.min
            xCluster = self.cluster[xClusterIndex]
            xIndex = xCluster.min

            # update animation text
            curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['change_text', str(curAniCluster.clusters[xClusterIndex].minAni)]))
            # update animation value
            curAniCluster.minAni = curAniCluster.clusters[xClusterIndex].minAni
            step += 1
            # update tree minimum
            self.min = self.value(xClusterIndex, xIndex)

        # otherwise if the deletion value is equal to the tree's maximum
        elif x == self.max:
            # hightlight right side green
            curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
            curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['green']))
            step += 1
            # if the summary vector is nonexistent
            if self.summary == None:
                curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['change_text', str(curAniCluster.minAni)]))
                # update animation max
                curAniCluster.maxAni = curAniCluster.minAni
                step += 1
                curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
                step += 1
                # update the tree maximum
                self.max = self.min
                return

            # get the location of the value to be deleted
            xClusterIndex = self.summary.max
            xCluster = self.cluster[xClusterIndex]
            xIndex = xCluster.max

            # update animation text
            curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['change_text', str(curAniCluster.clusters[xClusterIndex].maxAni)]))
            # update animation value
            curAniCluster.maxAni = curAniCluster.clusters[xClusterIndex].maxAni
            step += 1
            # update tree maximum
            self.max = self.value(xClusterIndex, xIndex)

        else:
            # get the location of the value to be deleted
            xClusterIndex = self.clusterIndex(x)
            xCluster = self.cluster.get(xClusterIndex, None)
            xIndex = self.valueIndex(x)
            # if that location does not exist
            if xCluster == None:
                # ensure everything is reset to typical blue color
                curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
                curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
                step += 1
                return

        # delete is required now, make the recursive call
        xCluster.delete(xIndex, curAniCluster.clusters[xClusterIndex])

        # if the delete operation emptied a cluster
        if xCluster.min == None:
            # delete that cluster from the hashmap
            del self.cluster[xClusterIndex]
            # update the summary vector to reflect the deletion
            self.summary.delete(xClusterIndex, curAniCluster.summary)
            # if summary is empty, mark that visibly
            if self.summary.min == None:
                self.summary = None

        # ensure everything is reset to typical blue color
        curAniCluster.min.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
        curAniCluster.max.aniQueue.put(animation.Movement(-1, -1,step, ['lightblue']))
        step += 1


    def __iter__(self):
        """
        Iterator over the elements in the veb-tree.
        
        Returns: int
        """
        value = self.min
        while value != None:
            yield value
            value = self.successor(value)


    def __str__(self):
        """
        Returns a string representing the veb-tree.

        Returns: str
        """
        return str(tuple(value for value in self))


    def __repr__(self):
        """
        Represents the veb-tree for printing.

        Returns: str
        """
        return str(self)


def startVEBtree(aniQueue, orginx, orginy, screen_width, screen_height, commandQueue):
    """
    Start the animation for the entire tree, runs interactively
    Arguments:
    ----------
    aniQueue : queue
        Queue of animation operations that are being processed
    originx : int
        Origin point for x axis on screen
    originy : int
        Origin point for y axis on screen
    screen_width : int
        Width of screen to assist with readable formatting
    screen_height : int 
        Height of screen to assist with readable formatting
    commandQueue : list
        Commands being inserted externally for processing with the specific VEB tree
    
    """
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

    # keep loop running while waiting on command
    while 1:
        step = 0
        command = commandQueue.get()
        # break condition when animator ends
        if command[0] == 'break':
            break
        # call insertion command
        elif command[0] == 'insert':
            VEBtree.insert(int(command[1]), VEBtreeAni, int(command[1]))
        # call deletion command
        elif command[0] == 'delete':
            VEBtree.delete(int(command[1]), VEBtreeAni)
        # call search command
        elif command[0] == 'search':
            VEBtree.contains(int(command[1]), VEBtreeAni)
