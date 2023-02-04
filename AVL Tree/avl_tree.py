import sys
import animation
import time
from queue import Queue

elements_to_insert = Queue()

# A class to represent a node in an AVL tree
class AVLTreeNode():
    def __init__(self, object, parent):
        self.object           = object
        self.parent           = parent
        self.left_child_node  = None
        self.right_child_node = None
        self.height           = 1
        self.level            = 0

# A class to represent an AVL Tree
#
# Insertion: O(log(N))
# Deletion: O(log(N))
# Search: O(log(N))
class AVLTreeAnimation():

    # Initialize the global tree variables
    def __init__(self, size, xorigin, width, height, aniList, y_distance):
        self.step = 0 # Step of the animation the tree is currently on
        self.size = size # Size of each node in the tree
        self.tree_height = 0 # Num of levels in the tree
        self.xorigin = xorigin # xorigin of screen section
        self.width = width # Width of screen section
        self.height = height # Height of screen section
        self.root = None # The topmost node of the tree
        self.aniList = aniList # List of animations to be made (only append)
        self.y_distance = y_distance # Distance between the levels of the tree

    # Function that users should call to insert a value to the AVL tree
    def insert(self, key):
        self.root = self.insert_helper(key, self.root, None)
        if self.tree_height > self.get_height(self.root) + 1:
            self.resize_tree(self.get_height(self.root))

    # Function that will insert the specified key into the tree using recursion
    def insert_helper(self, key, current_node, parent):
        if current_node is None: # Reached the bottom of the tree
            # Create new node which includes the animation object
            new_object = animation.Object(key)
            self.aniList.append(new_object)
            new_node = AVLTreeNode(new_object, parent)
            if parent is None: # Adding the root node
                new_object.x = self.xorigin + (self.width / 2) - (self.size / 2)
                new_object.y = self.height / 15
                self.tree_height = 1
                self.draw_node(new_object.aniQueue, new_object.x, new_object.y, new_object.userNum, 'lightblue', True)
            else: # New leaf is being added
                new_node.level = self.get_depth(new_node)
                if new_node.level > self.tree_height: # Adding a level -> Resize tree
                    self.resize_tree(new_node.level)
                    self.tree_height += 1
                # Calculate the nodes x and y coordinates
                seperator = 2**(self.tree_height - 2)
                # print(self.tree_height)
                level_seperators = [0]
                for idx in range(1, self.tree_height):
                    level_seperators.append(seperator)
                    seperator = seperator / 2
                if new_object.userNum > parent.object.userNum:
                    new_object.x = parent.object.x + (self.size * level_seperators[self.get_depth(new_node) - 1])
                    new_object.y = parent.object.y + self.y_distance
                else:
                    new_object.x = parent.object.x - (self.size * level_seperators[self.get_depth(new_node) - 1])
                    new_object.y = parent.object.y + self.y_distance
                # Draw the new node onto the screen
                self.draw_node(new_object.aniQueue, new_object.x, new_object.y, new_object.userNum, 'lightblue', False)
                # Create line to the parent node
                self.draw_line(new_node, True)
                # Reset the parent node's color
                self.color_node(parent, 'lightblue', True)
            return new_node
        elif key <= current_node.object.userNum: # New node is to the left of the current one
            if parent is not None:
                self.color_node(parent, 'lightblue', False)
            self.color_node(current_node, 'gold', True)
            current_node.left_child_node = self.insert_helper(key, current_node.left_child_node, current_node)
        else: # New node is to the right of the current one
            if parent is not None:
                self.color_node(parent, 'lightblue', False)
            self.color_node(current_node, 'gold', True)
            current_node.right_child_node = self.insert_helper(key, current_node.right_child_node, current_node)

        # The node's new height will be the maximum child's heigth plus one.
        # Used when we are climbing back up the tree and rotating as necessary.
        current_node.height = 1 + max(self.get_height(current_node.left_child_node),
                                      self.get_height(current_node.right_child_node))

        # Get the new balance factor for the current node
        balance_factor = self.get_balance(current_node)
        if balance_factor > 1 and key < current_node.left_child_node.object.userNum:
            node = self.right_rotate(current_node)
            self.fix_tree(node, True)
            return node
        if balance_factor < -1 and key > current_node.right_child_node.object.userNum:
            node = self.left_rotate(current_node)
            self.fix_tree(node, True)
            return node
        if balance_factor > 1 and key > current_node.left_child_node.object.userNum:
            node = self.left_rotate(current_node.left_child_node)
            self.fix_tree(node, True)
            current_node.left_child_node = node
            node = self.right_rotate(node)
            self.fix_tree(node, True)
            return node
        if balance_factor < -1 and key < current_node.right_child_node.object.userNum:
            node = self.right_rotate(current_node.right_child_node)
            self.fix_tree(node, True)
            self.root.right_child_node = node
            node = self.left_rotate(current_node)
            self.fix_tree(node, True)
            return node
        # Subtree is balanced
        return current_node

    # Function that will delete the node with the specified key
    def delete_node(self, root, key):
        # Perform standard BST delete
        if root is None:
            return root
        elif key < root.value: # Node to be deleted is to the left
            root.left_child_node = self.delete_node(root.left_child_node, key)
        elif key > root.value: # Node to be deleted is to the right
            root.right_child_node = self.delete_node(root.right_child_node, key)
        else: # This is the node that needs to be deleted
            if root.left_child_node is None:
                # No left children, so right child will simply move up
                temp = root.right_child_node
                root = None
                return temp
            elif root.right_child_node is None:
                # No right children, so left child will simply move up
                temp = root.left_child_node
                root = None
                return temp
            # Node to be deleted has both children so use the minimum value of the
            # right hand side as a replacement
            temp = self.get_successor(root.right_child_node)
            root.value = temp.value
            root.right_child_node = self.delete_node(root.right_child_node, temp.value)

        # If the tree is empty, no balancing needs to be done
        if root is None:
            return root

        # Calculate the new height of the node
        root.height = 1 + max(self.get_height(root.left_child_node),
                              self.get_height(root.right_child_node))

        # Get the new balance factor for the current node
        balance_factor = self.get_balance(root)
        # If the node is now unbalanced to the left
        if balance_factor > 1 and self.get_balance(root.left_child_node) >= 0:
            return self.right_rotate(root)

        if balance_factor < -1 and self.get_balance(root.right_child_node) <= 0:
            self.left_rotate(root)
            self.fix_tree(self.root)
            # TODO Decrease the size of the tree if necessary
            return self.left_rotate(root)

        # If the root is unbalance to the right
        if balance_factor < -1 and self.get_balance(root.left_child_node) < 0:
            root.left_child_node = self.left_rotate(root.left_child_node)
            return self.right_rotate(root)

        #abc
        if balance_factor < -1 and self.get_balance(root.right_child_node) > 0:
                root.right_child_node = self.right_rotate(root.right_child_node)
                return self.left_rotate(root)

        # Return the new balanced root of the tree
        return root

    """
    Function that will search for the desired key.
    NOTE: If the key is not found, then None will be returned
    """
    def search(self, key):
        node = self.search_helper(key, self.root)
        self.color_node(node, 'lightblue', True)
        return node

    """
    Recursive helper function for search.
    """
    def search_helper(self, key, node):
        found_node = None
        if node is not None:
            self.color_node(node, 'gold', True)
            if key == node.object.userNum:
                self.color_node(node, 'green', True)
                return node
            elif key < node.object.userNum:
                self.color_node(node, 'lightblue', True)
                found_node = self.search_helper(key, node.left_child_node)
                return found_node
            else:
                self.color_node(node, 'lightblue', True)
                found_node = self.search_helper(key, node.right_child_node)
                return found_node
        else:
            return found_node
    """
    Function that will perform a left rotation using the parent node
          z           y
           \         / \
            y   ->  z   x
           / \       \
         T2   x       T2
    """
    def left_rotate(self, z):
        self.color_node(z, 'gold', True)
        y = z.right_child_node
        self.color_node(y, 'gold', True)
        T2 = y.left_child_node
        z.right_child_node = T2

        if T2 is not None:
            T2.parent = z
            self.color_node(T2, 'gold', True)

        y.parent = z.parent
        y.left_child_node = z
        z.parent = y

        # Calculate the new heights for the nodes
        z.height = 1 + max(self.get_height(z.left_child_node),
                           self.get_height(z.right_child_node))
        y.height = 1 + max(self.get_height(y.left_child_node),
                           self.get_height(y.right_child_node))
        return y

    """
    Function that will perform a right rotation using the parent node
          z           y
         /           / \
        y     ->    x   z
       / \             /
      x   T3         T3
    """
    def right_rotate(self, z):
        # Perform the right rotation
        self.color_node(z, 'gold', True)
        y = z.left_child_node
        self.color_node(y, 'gold', True)
        T3 = y.right_child_node
        y.right_child_node = z
        z.left_child_node = T3

        if T3 is not None:
            self.color_node(T3, 'gold', True)
            T3.parent = z

        y.parent = z.parent
        y.right_child_node = z
        z.parent = y

        # Calculate the new heights for the nodes
        z.height = 1 + max(self.get_height(z.left_child_node),
                           self.get_height(z.right_child_node))
        y.height = 1 + max(self.get_height(y.left_child_node),
                           self.get_height(y.right_child_node))

        # Return the new top level node
        return y

    # Return the height of the tree starting at the given node
    def get_height(self, root):
        # If the tree is empty the height will be 0
        if root is None:
            return 0
        return root.height

    # Gets the depth of the node (Inverse of get height)
    def get_depth(self, node):
        depth = 0
        current_node = node
        while current_node is not None:
            depth += 1
            current_node = current_node.parent
        return depth

    # Get the balance of the given node
    def get_balance(self, root):
        if root is None:
            # The tree is empty
            return 0
        # Calculate the balance by determing whether the left or right side of
        # the tree has more nodes.
        return self.get_height(root.left_child_node) - \
               self.get_height(root.right_child_node)

    # Get the smallest value in the tree
    def get_successor(self, root):
        # If return either the root or the farthest value to the left
        if root is None or root.left_child_node is None:
            return root
        return self.get_successor(root.left_child_node)

    """
    Implements a preorder traversal that will move the nodes to fit the new tree height

    Calculation:
    When expanding the tree every node's distance from the root node should double.
    Ex:
    In when going from a height 3 -> height 4 tree, the root's child nodes will go from being
        root.x (+ of -) 2*size --> root.x (+ or -) 4*size
    This  principle holds for all nodes in the tree
    """
    def preorder_resize(self, current_node):
        if current_node is not None:
            if current_node.object.userNum <= self.root.object.userNum: # Node will be to the left of it's parent
                self.delete_line(current_node, False)
                self.move_node(self.root.object.x - ((self.root.object.x - current_node.object.x) * 2), current_node.object.y, current_node, False)
            else: # Node will be to the right of it's parent
                self.delete_line(current_node, False)
                self.move_node(self.root.object.x + ((current_node.object.x - self.root.object.x) * 2), current_node.object.y, current_node, False)
            self.preorder_resize(current_node.left_child_node)
            self.preorder_resize(current_node.right_child_node)

    """
    Function that will first resize the tree and then readd the parent-child lines.
    """
    def resize_tree(self, height):
        # Resize the entire tree (deletes all lines)
        self.preorder_resize(self.root)
        self.step += 1
        # Go through and re-add all of the lines
        self.add_lines_helper(self.root)
        self.step += 1
        return

    """
    Function that will fix a tree that has been balanced
    """
    def fix_tree(self, subtree_root, increment_step):
        seperator = 2**(self.tree_height - 2)
        level_seperators = [0]
        for idx in range(1, self.tree_height):
            level_seperators.append(seperator)
            seperator = seperator / 2
        self.fix_tree_helper(subtree_root, subtree_root, level_seperators, increment_step)
        self.reset_color(subtree_root)
        if increment_step:
            self.step += 1
        return

    """
    Recursive helper function for the tree
    """
    def fix_tree_helper(self, subtree_root, current_node, level_seperators, increment_step):
        if current_node is not None:
            if current_node.parent is not None:
                if current_node.object.userNum <= current_node.parent.object.userNum:
                    self.delete_line(current_node, increment_step)
                    self.move_node(current_node.parent.object.x - (self.size * level_seperators[self.get_depth(current_node) - 1]), current_node.parent.object.y + 50, current_node, increment_step)
                    self.draw_line(current_node, increment_step)
                else:
                    self.delete_line(current_node, increment_step)
                    self.move_node(current_node.parent.object.x + (self.size * level_seperators[self.get_depth(current_node) - 1]), current_node.parent.object.y + self.y_distance, current_node, increment_step)
                    self.draw_line(current_node, increment_step)
            else:
                self.delete_line(current_node, True)
                self.move_node(self.xorigin + (self.width / 2) - (self.size / 2), self.xorigin + (self.width / 2) - (self.size / 2), current_node, increment_step)

            self.fix_tree_helper(subtree_root, current_node.left_child_node, level_seperators, increment_step)
            self.fix_tree_helper(subtree_root, current_node.right_child_node, level_seperators, increment_step)
            return

    """
    Recursive Function that will reset all of the nodes colors in the subtree
    """
    def reset_color(self, current_node):
        if current_node is not None:
            self.color_node(current_node, 'lightblue', False)
            self.reset_color(current_node.left_child_node)
            self.reset_color(current_node.right_child_node)

    """
    Recursive helper to add lines to the tree
    """
    def add_lines_helper(self, current_node):
        if current_node is not None:
            if current_node.parent is not None:
                # Draw a line to the parent
                current_node.object.aniQueue.put(animation.Movement(-1,-1,self.step,[],
                    [current_node.parent.object.x + (self.size / 2), current_node.parent.object.y + self.size,
                     current_node.object.x + (self.size / 2), current_node.object.y]))
            self.add_lines_helper(current_node.left_child_node)
            self.add_lines_helper(current_node.right_child_node)
        return

    """
    Draws a new node at the given x y coordinates.
    """
    def draw_node(self, queue, x, y, key, color, increment_step):
        queue.put(animation.Movement(-1, -1, self.step, [], [], ['oval', x, y, self.size, str(key), color]))
        if increment_step:
            self.step += 1
        return

    """
    Draws a line to the node's parent.
    NOTE: The given node must have a parent (can't be the root)
    """
    def draw_line(self, node, increment_step):
        node.object.aniQueue.put(animation.Movement(-1, -1, self.step, [], [node.parent.object.x + (self.size / 2), node.parent.object.y + self.size, node.object.x + (self.size / 2), node.object.y]))
        if increment_step:
            self.step += 1
        return

    """
    Deletes the line connecting the node to its parent.
    """
    def delete_line(self, node, increment_step):
        node.object.aniQueue.put(animation.Movement(node.object.x, node.object.y, self.step, ['delete_line']))
        if increment_step:
            self.step += 1
        return

    """
    Updates the given node's coordinates to the x and y values and adds the
    movement to the animation queue.
    """
    def move_node(self, x, y, node, increment_step):
        node.object.x = x
        node.object.y = y
        node.object.aniQueue.put(animation.Movement(node.object.x,  node.object.y))
        if increment_step:
            self.step += 1
        return

    """
    Recolors the given node.
    """
    def color_node(self, node, color, increment_step):
        node.object.aniQueue.put(animation.Movement(-1, -1, self.step, [color]))
        if increment_step:
            self.step += 1
        return

# Function that will start the avl tree algorithm
def start_avl_tree(aniList, x_origin, y_origin, width, height):
    # Initialize the AVL tree object
    tree = AVLTreeAnimation(30, x_origin, width, height, aniList, 50)
    # Loop and wait for more elements to insert, delete, and search for
    while True:
        tree.insert(1)
        tree.insert(2)
        tree.insert(0)
        tree.insert(-1)
        tree.insert(5)
        tree.insert(1.5)
        tree.insert(0.5)
        tree.insert(6)
        tree.insert(7)
        tree.insert(8)
        tree.insert(6.5)
        tree.insert(-1.5)
        tree.insert(-2)
        tree.insert(0.75)
        tree.insert(0.8)
        tree.search(8)
        break
