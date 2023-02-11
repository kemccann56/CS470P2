import math

class VEB():
    def __init__(self, u):
        self.minimum = None
        self.maximum = None
        self.u = u
        self.n_galaxies = math.ceil(u**.5)
        if u > 2:
            self.summary = VEB(self.n_galaxies)
            self.galaxy = [VEB(self.n_galaxies) for _ in range(self.n_galaxies)]
        return
        
def high(V, x):
    high = math.floor(x / V.n_galaxies)
    return high

def low(V, x):
    low = x % V.n_galaxies
    return low

def index(V, i, j):
    assert isinstance(i, int)
    assert isinstance(V.n_galaxies, int)
    assert isinstance(j, int)
    index = i * V.n_galaxies + j
    return index
        
def successor(V, x):
    if V.u == 2:
        if x == 0 and V.maximum == 1:
            return 1
        else:
            return
        
    if V.minimum is not None and x < V.minimum:
        return self.minimum
        
    i = high(V, x)
    max_low = V.galaxy[i].maximum
    if max_low is not None and low(V, x) < max_low:
        j = successor(V.galaxy[i], low(V, x))
    else:
#         i = V.summary.successor(high(V, x))
        i = successor(V.summary, high(V,x))
        if i is None:
            return None
        j = V.galaxy[i].minimum
    return index(V, i, j)

# max_low = self.cluster[self.high(x)].max
# if max_low is not None and self.low(x) < max_low:
#     offset = self.cluster[self.high(x)].successor(self.low(x))
#     return self.index(self.high(x), offset)
# else:
#     succ_cluster = self.summary.successor(self.high(x))
#     if succ_cluster is None:
#         return None
#     else:
#         offset = self.cluster[succ_cluster].min
#         return self.index(succ_cluster, offset)

def insert(V, x):
    if x == V.minimum or x == V.maximum:
        return

    if V.minimum is None:
        V.minimum = x
        V.maximum = x
        return
    
    if x < V.minimum:
        x, V.minimum = V.minimum, x
    if x > V.maximum:
        x, V.maximum = V.maximum, x
    
    if V.u == 2:
        return
        
    insert(V.galaxy[high(V, x)], low(V, x) )
    if V.galaxy[high(V, x)].minimum is None:
        insert(V.summary, high(V, x))
    return

def delete(V, x):
    if V.minimum is None or x < V.minimum or x > V.maximum:
        return

    if V.minimum == V.maximum:
        V.minimum = V.maximum = None
        return
    
    if V.u == 2:
        if x == 0:
            self.minimum = 1
        else:
            self.maximum = 0
        return
    
    if x == V.minimum:
        i = V.summary.minimum
        if i is None:
            V.minimum = None
            V.maximum = None
            return
        else:
            V.minimum = index(i, V.galaxy[i].minimum)

    delete(V.galaxy[high(V, x)], low(V, x))
    if V.galaxy[high(V, x)].minimum is None:
        delete(V.summary, high(V, x))
    if x == V.maximum:
        V.summary.maximum = None
    else:
        i = V.summary.maximum
        V.maximum = index(i, V.galaxy[i].maximum)
    return
    
V = VEB(64)
# for i in [1,2,7,8,12]:
for i in range(64):
    insert(V, i)
for i in [0,1,3,7,8]:
    print(successor(V, i))