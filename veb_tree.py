from math import floor
import animation

# Global step count value
step_count = 0

class VEB():
    """
    Constructor for the VEB class. This will create the enitre VEB tree based
    on the size of the universe.
    Parameters:
    -----------
    u : int
        The size of the universe for the VEB tree.
    Returns:
    --------
    VEB
        The top layer VEB object that all other operations will start at.
    """
    def __init__(self, u, aniList, x_origin, y_origin, width, height, size, animate):
        self.minimum = None
        self.maximum = None
        self.universe = u
        self.aniList = aniList
        self.size = size
        # Create Universe animation objects
        self.universeLabelAniObject = animation.Object(-1)
        self.universeAniObject = animation.Object(-1)
        self.aniList.append(self.universeLabelAniObject)
        self.aniList.append(self.universeAniObject)
        # Create minimum animation objects
        self.minLabelAniObject = animation.Object(-1)
        self.minAniObject = animation.Object(-1)
        self.aniList.append(self.minLabelAniObject)
        self.aniList.append(self.minAniObject)
        # Create maximum animation objects
        self.maxLabelAniObject = animation.Object(-1)
        self.maxAniObject = animation.Object(-1)
        self.aniList.append(self.maxLabelAniObject)
        self.aniList.append(self.maxAniObject)
        if animate:
            # Draw all of this VEB boxed to the screen
            if self.universe == 16:
                self.universeLabelAniObject.x = x_origin - (3*size)
                self.universeLabelAniObject.y = y_origin
                self.draw_box(self.universeLabelAniObject, 'lightblue', "U", False)
                self.universeAniObject.x = x_origin - (2*size)
                self.universeAniObject.y = y_origin
                self.draw_box(self.universeAniObject, 'lightblue', str(self.universe), False)
                self.minLabelAniObject.x = x_origin - (1*size)
                self.minLabelAniObject.y = y_origin
                self.draw_box(self.minLabelAniObject, 'lightblue', "Min", False)
                self.minAniObject.x = x_origin
                self.minAniObject.y = y_origin
                self.draw_box(self.minAniObject, 'lightblue', "None", False)
                self.maxLabelAniObject.x = x_origin + (1*size)
                self.maxLabelAniObject.y = y_origin
                self.draw_box(self.maxLabelAniObject, 'lightblue', "Max", False)
                self.maxAniObject.x = x_origin + (2*size)
                self.maxAniObject.y = y_origin
                self.draw_box(self.maxAniObject, 'lightblue', "None", False)
            else:
                self.universeLabelAniObject.x = x_origin
                self.universeLabelAniObject.y = y_origin
                self.draw_box(self.universeLabelAniObject, 'lightblue', "U", False)
                self.universeAniObject.x = x_origin + size
                self.universeAniObject.y = y_origin
                self.draw_box(self.universeAniObject, 'lightblue', str(self.universe), False)
                self.minLabelAniObject.x = x_origin + (2*size)
                self.minLabelAniObject.y = y_origin
                self.draw_box(self.minLabelAniObject, 'lightblue', "Min", False)
                self.minAniObject.x = x_origin + (3*size)
                self.minAniObject.y = y_origin
                self.draw_box(self.minAniObject, 'lightblue', "None", False)
                self.maxLabelAniObject.x = x_origin + (4*size)
                self.maxLabelAniObject.y = y_origin
                self.draw_box(self.maxLabelAniObject, 'lightblue', "Max", False)
                self.maxAniObject.x = x_origin + (5*size)
                self.maxAniObject.y = y_origin
                self.draw_box(self.maxAniObject, 'lightblue', "None", False)
        # If the universe is greater than 2, we need to recursively create all
        # of the sub VEB and summary vectors.
        if self.universe > 2:
            self.n_galaxies = int(u**.5)
            if self.universe == 16:
                self.summary = VEB(self.n_galaxies, aniList, x_origin, y_origin, width, height, size, False)
                self.galaxies = \
                [
                    VEB(self.n_galaxies, aniList, x_origin - (27*size), y_origin + 50, width, height, size, animate),
                    VEB(self.n_galaxies, aniList, x_origin - (11*size), y_origin + 50, width, height, size, animate),
                    VEB(self.n_galaxies, aniList, x_origin + (5*size), y_origin + 50, width, height, size, animate),
                    VEB(self.n_galaxies, aniList, x_origin + (21*size), y_origin + 50, width, height, size, animate)
                ]
            elif self.universe == 4:
                self.summary = VEB(self.n_galaxies, aniList, x_origin, y_origin, width, height, size, False)
                self.galaxies = \
                [
                    VEB(self.n_galaxies, aniList, x_origin - (4*size), y_origin + 50, width, height, size, animate),
                    VEB(self.n_galaxies, aniList, x_origin + (4*size), y_origin + 50, width, height, size, animate),
                ]
        # We have reached the bottom of the VEB tree, we don't need to create
        # the summary vector or the sub galaxies.
        else:
            self.n_galaxies = 0
            self.summary = None
            self.galaxies = None
        return

    """
    Inserts an integer within the universe into the tree.
    Parameters:
    -----------
    V : VEB
        A van Emde Boas tree object.
    x : int
        The key that we want to insert into the data structure.
    """
    def insert(self, V, x):
        # If minumum is none, we now there are no elements anywhere below this
        # point, so we can directly add it as the min/max of the VEB
        if V.minimum is None:
            self.color_box(V.minAniObject, 'green', False)
            self.color_box(V.maxAniObject, 'green', True)
            self.change_text(V.minAniObject, str(x), True)
            self.change_text(V.maxAniObject, str(x), True)
            V.minimum = x
            V.maximum = x
            self.color_box(V.minAniObject, 'lightblue', False)
            self.color_box(V.maxAniObject, 'lightblue', False)
        # If we have a new minimum for this VEB, swap the values with the old
        # one and continue down the tree to find the new location for it.
        elif x < V.minimum:
            self.color_box(V.minAniObject, 'green', True)
            self.change_text(V.minAniObject, str(x), True)
            x, V.minimum = V.minimum, x
            self.color_box(V.minAniObject, 'lightblue', True)
        # If we have not reached the bottom of the tree
        if V.universe > 2:
            if V.galaxies[self.high(V, x)].minimum is None:
                self.insert(V.summary, self.high(V, x))
            self.insert(V.galaxies[self.high(V, x)], self.low(V, x))
        if x > V.maximum:
            self.color_box(V.maxAniObject, 'green', True)
            self.change_text(V.maxAniObject, str(x), True)
            V.maximum = x
            self.color_box(V.maxAniObject, 'lightblue', True)

    """
    Deletes an integer within the universe from the tree.
    Parameters:
    -----------
    V : VEB
        A van Emde Boas tree object.
    x : int
        The key that we want to delete from the data structure.
    """
    def delete(self, V, x):
        # If there is only one element in the VEB, we know that no sub elements
        # exist, so we can just set them both to None and exit
        if V.minimum == V.maximum:
            self.color_box(V.minAniObject, 'red', False)
            self.color_box(V.maxAniObject, 'red', True)
            self.change_text(V.minAniObject, '0', True)
            self.change_text(V.maxAniObject, '0', True)
            V.minimum = None
            V.maximum = None
            self.color_box(V.minAniObject, 'lightblue', False)
            self.color_box(V.maxAniObject, 'lightblue', False)
        # If we are at the bottom layer of the tree, the element we are going to
        # delete will either be this min or max value.
        elif V.universe == 2:
            # If x is the minimum, only the maximum will be left
            self.color_box(V.maxAniObject, 'red', False)
            if x == 0:
                self.change_text(V.maxAniObject, '1', True)
                V.minimum = 1
            # If x is the maximum, only the minimum will be left
            else:
                self.change_text(V.maxAniObject, '0', True)
                V.minimum = 0
            self.color_box(V.maxAniObject, 'red', True)
            self.change_text(V.maxAniObject, str(V.minimum), True)
            V.maximum = V.minimum
            self.color_box(V.maxAniObject, 'lightblue', False)
            self.color_box(V.minAniObject, 'lightblue', False)
        # We must go down the tree, and update the summary VEB's along the way
        else:
            if x == V.minimum:
                first_galaxy = V.summary.minimum
                x = self.index(V, first_galaxy, V.galaxies[first_galaxy].minimum)
                self.color_box(V.minAniObject, 'red', True)
                self.change_text(V.minAniObject, str(x), True)
                V.minimum = x
                self.color_box(V.minAniObject, 'lightblue', False)

            self.delete(V.galaxies[self.high(V, x)], self.low(V, x))
            if V.galaxies[self.high(V, x)].minimum == None:
                self.delete(V.summary, self.high(V, x))
                if x == V.maximum:
                    summary_max = V.summary.maximum
                    self.color_box(V.maxAniObject, 'red', True)
                    if summary_max == None:
                        self.change_text(V.maxAniObject, str(V.minimum), True)
                        V.maximum = V.minimum
                    else:
                        new_max = self.index(V, summary_max, V.galaxies[summary_max].maximum)
                        self.change_text(V.maxAniObject, str(new_max), True)
                        V.maximum = new_max
                    self.color_box(V.maxAniObject, 'lightblue', True)

            elif x == V.maximum:
                self.color_box(V.maxAniObject, 'red', True)
                new_max = self.index(V, self.high(V, x), V.galaxies[self.high(V, x)].maximum)
                self.change_text(V.maxAniObject, str(new_max), True)
                V.maximum = new_max
                self.color_box(V.maxAniObject, 'lightblue', True)
    """
    Searches for the given object in the VEB tree.
    Parameters:
    -----------
    V : VEB
        The VEB object that we are currently checking.
    x : int
        The value that we are currently searching for in the tree.
    Returns:
    --------
    bool
        Whether or not the value is in the tree.
    """
    def search(self, V, x):
        self.color_box(V.maxAniObject, 'orange', False)
        self.color_box(V.maxAniObject, 'orange', True)
        if x == V.minimum or x == V.maximum:
            if x == V.minimum:
                self.color_box(V.minAniObject, 'green', True)
            else:
                self.color_box(V.maxAniObject, 'green', True)

            self.color_box(V.minAniObject, 'lightblue', False)
            self.color_box(V.maxAniObject, 'lightblue', True)
            return True
        if V.universe == 2:
            self.color_box(V.minAniObject, 'red', False)
            self.color_box(V.maxAniObject, 'red', True)
            self.color_box(V.minAniObject, 'lightblue', False)
            self.color_box(V.maxAniObject, 'lightblue', True)
            return False
        self.color_box(V.minAniObject, 'lightblue', False)
        self.color_box(V.maxAniObject, 'lightblue', True)
        return self.search(V.galaxies[self.high(V, x)], self.low(V, x))

    """
    """
    def high(self, V, x):
        return x // floor(V.universe**0.5)

    """
    """
    def low(self, V, x):
        return x % floor(V.universe**0.5)

    """
    """
    def index(self, V, x, y):
        return x * floor(V.universe) + y

    """
    Function that will draw a box onto the screen.
    Parameters:
    -----------
    animation_object : Object
        The animation object that needs to be drawn. This object's aniQueue, x,
        y, and userNum variables must already be set.
    color : str
        The color that the new node should be.
    text : str
        The text string that we want written in the box.
    increment_step : bool
        Determines whether of not the step count will be incremented after the line
        is drawn.
    """
    def draw_box(self, animation_object, color, text, increment_step):
        global step_count
        animation_object.aniQueue.put(animation.Movement(-1, -1, step_count, [], [],
        ['rectangle', animation_object.x, animation_object.y, self.size, text, color]))
        if increment_step:
            step_count += 1
        return

    """
    Function that will color a box drawn on the screen.
    Parameters:
    -----------
    aniObject : Object
        The animation object that needs to be recolored.
    color : str
        The color that the box should be changed to.
    increment_step : bool
        Determines whether or not the step count will be incremented after the
        line is drawn.
    """
    def color_box(self, aniObject, color, increment_step):
        global step_count
        aniObject.aniQueue.put(animation.Movement(-1, -1, step_count, [color]))
        if increment_step:
            step_count += 1
        return

    """
    Function that will change the text of a box drawn on the screen.
    Parameters:
    -----------
    aniObject : Object
        The animation object that needs to be recolored.
    text : str
        The text that should be displayed in the box
    """
    def change_text(self, aniObject, text, increment_step):
        global step_count
        aniObject.aniQueue.put(animation.Movement(-1, -1, step_count, ['change_text', text]))
        if increment_step:
            step_count += 1
        return

"""
The function that should be called when initializing a VEB tree animation.
NOTE: This function will block and wait for more input.
Parameters:
-----------
aniList : list
    The data structure that the Movement objects should be appended to. Append
    is the only permissable action for this list.
x_origin : int
    The x origin that will be used to position the animation. For this case,
    it should always be 0.
y_origin : int
    The y origin that will be used to position the animation.
width : int
    The total width of the animation window we are allowed to use.
height : int
    The total height of the animation window we are allowed to use.
"""
def start_veb(aniList, x_origin, y_origin, width, height):
    # Initialize the VEB tree object
    V = VEB(16, aniList, x_origin + (width / 2), y_origin + (height // 15), width, height, 25, True)
    # Loop and wait for more elements to insert, delete, and search for
    while True:
        # for i in [1,2,7,8,12]:
        for i in range(16):
            V.insert(V, i)
        for i in range(16):
            print(V.search(V, i))
        for i in range(16):
            V.delete(V, i)
        for i in range(16):
            print(V.search(V, i))
        break
