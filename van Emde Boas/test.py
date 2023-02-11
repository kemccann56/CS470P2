from dataclasses import dataclass

@dataclass
class MinMax():
    minimum=None
    maximum=None

class VEB():
    def __init__(self, u):
        self.minimum = None
        self.maximum = None
        self.universe = u
        if self.universe > 2:
            self.n_galaxies = int(u**.5)
            self.summary = VEB(self.n_galaxies)
            self.galaxies = [VEB(self.n_galaxies) for _ in range(self.n_galaxies)]
        else:
            self.summary = None
            self.galaxies = None
        return

"""
Returns the result of x divided by the VEB's number of galaxies using integer
division.
Parameters:
-----------
V : VEB
    The current van Embde Boas Tree we are looking at.
x : int
    The integer that we need the index for.
"""
def high(V, x):
    high = x // V.n_galaxies
    return high

"""
Returns the result of x modulo n_galaxies for the vEB tree. This will be used to
find the number that we should now be looking for.
"""
def low(V, x):
    low = x % V.n_galaxies
    return low

def index(V, i, j):
    index = i * V.n_galaxies + j
    return index

"""
Finds the successor the the given value in the vEB tree.
"""
def successor(V, x):
    if V.universe == 2:
        if x == 0 and V.maximum == 1:
            return 1
        else:
            #print("1")
            return
    i = high(V, x)
    if low(V, x) < V.galaxies[i].maximum:
        j = successor(V.galaxies[i], low(V, x))
        #print("2")
    else:
        i = successor(V.summary, high(V, x))
        #print("3")
        j = V.galaxies[i].minimum
    return index(V, i, j)

def insert(V, x):
    #print(x)
    # If the key is already the minimum or maximum value we know that it is
    # already in the tree.
    if x == V.minimum or x == V.maximum:
        return
    # If minimum is None, we know that this is the only key in the VEB, so it
    # will be both the minumum and the maximum.
    if V.minimum is None:
        V.minimum = x
        V.maximum = x
        return
    # If minimum == maximum, we know that there is only one element in the tree
    # so we just need to insert the new min/max value into the VEB.
    if V.minimum == V.maximum:
        if x < V.minimum:
            temp = x
            x = V.minimum
            V.minimum = temp
        elif x > V.maximum:
            temp = x
            x = V.maximum
            V.maximum = temp
    # If we are at the bottom of the tree then any changes do not need to be
    # propagated down.
    if V.universe == 2:
        return
    # Propogate the change down the tree.
    # NOTE: Removed if statement
    insert(V.galaxies[high(V, x)], low(V, x))
    insert(V.summary, high(V, x))
    return

"""
Searches for the key, by looking at each vEB's min and max before traveling
down the tree.
"""
def search(V, key):
    # If the key is greater than the universe size, it can not be represented
    # in the tree so return immediantely.
    if V.universe < key:
        return False
    # If the key is currently the VEB objects minumum or maximum, we know that
    # it exists, so we can stop here
    if V.minimum == key or V.maximum == key:
        return True
    # If the universe is less than or equal to 2, we know that we have reached
    # the bottom of the tree.
    elif V.universe <= 2:
        return False
    # If we have made it this far, then we move on to the next level of the tree.
    return search(V.galaxies[high(V, key)], low(V, key))

V = VEB(16)
# for i in [1,2,7,8,12]:
for i in range(16):
    insert(V, i)
found_val = True
for i in range(16):
    if not search(V, i):
        found_val = False
if found_val:
    print("Found all values!")
else:
    print("Did not find all values")
print(successor(V, 1))
