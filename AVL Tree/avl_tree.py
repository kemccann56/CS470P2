import sys
import movement
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
    def __init__(self, size, xorigin, width, height, aniList):
        self.step = 0 # Step of the animation the tree is currently on
        self.size = size # Size of each node in the tree
        self.tree_height = 0 # Num of levels in the tree
        self.xorigin = xorigin # xorigin of screen section
        self.width = width # Width of screen section
        self.height = height # Height of screen section
        self.root = None # The topmost node of the tree
        self.aniList = aniList # List of animations to be made (only append)

    # Function that users should call to insert a value to the AVL tree
    def insert(self, key):
        self.root = self.insert_helper(key, self.root, None)
        """
        # Reset the tree height since rotation might have been done
        self.tree_height = self.get_height(self.root)
        # Resize the tree based off of any rotations that occured
        self.fix_tree(self.root)
        """

    # Function that will insert the specified key into the tree using recursion
    def insert_helper(self, key, current_node, parent):
        if current_node is None:
            # If the tree is empty, then create the root node
            new_object = movement.Object(key)
            self.aniList.append(new_object)
            new_node = AVLTreeNode(new_object, parent)

            # Set the new objects x and y value
            if parent is None:
                # Root node, so set the coordinates for the start of the tree
                new_object.x = self.xorigin + (self.width / 2) - (self.size / 2)
                new_object.y = self.height / 15
                self.tree_height = 1
            else:
                # Check the height of the tree using the newly inserted leaf
                height = self.get_depth(new_node)
                new_node.level = height
                # print(str(height) + " " + str(self.tree_height))
                # If the new height is greater than the tree height we must resize
                # the tree before adding the new node in the animation
                if height > self.tree_height:
                    self.resize_tree(height)
                    self.tree_height += 1
                    self.step += 1

                # Set x and y values based on which side of the parent they are on
                if new_object.userNum > parent.object.userNum:
                    new_object.x = parent.object.x + self.size
                    new_object.y = parent.object.y + 50
                    new_object.aniQueue.put(movement.Movement(-1,-1,self.step,[],
                    [parent.object.x + (self.size / 2), parent.object.y + self.size, new_object.x + (self.size / 2), new_object.y]))
                else:
                    new_object.x = parent.object.x - self.size
                    new_object.y = parent.object.y + 50
                    new_object.aniQueue.put(movement.Movement(-1,-1,self.step,[],
                    [parent.object.x + (self.size / 2), parent.object.y + self.size, new_object.x + (self.size / 2), new_object.y]))


            # Add the newly created object to the animation queue to be drawn
            new_object.aniQueue.put(movement.Movement(-1, -1, self.step, [], [],
                                    ['oval',new_object.x,new_object.y,self.size,str(new_object.userNum),'lightblue']))
            # Indicate that we have moved on to the next step
            self.step += 1

            return new_node
        elif key <= current_node.object.userNum:
            # If the new key is less than or equal to the current node's,
            # go to the left child node
            current_node.left_child_node = self.insert_helper(key, current_node.left_child_node, current_node)
        else:
            # If the new key is greater than the current node's,
            # go the the right child node
            current_node.right_child_node = self.insert_helper(key, current_node.right_child_node, current_node)

        # The node's new height will be the maximum child's heigth plus one
        current_node.height = 1 + max(self.get_height(current_node.left_child_node),
                                      self.get_height(current_node.right_child_node))

        # Get the new balance factor for the current node
        balance_factor = self.get_balance(current_node)

        # Left side of the tree is to heavy, so rotate to the right
        if balance_factor > 1 and key < current_node.left_child_node.object.userNum:
            return self.right_rotate(current_node)

        # Right side of the tree is to heavy, so rotate to the left
        if balance_factor < -1 and key > current_node.right_child_node.object.userNum:
            return self.left_rotate(current_node)

        if balance_factor > 1 and key > current_node.left_child_node.object.userNum:
            current_node.left_child_node = self.left_rotate(current_node.left_child_node)
            return self.right_rotate(current_node)

        if balance_factor < -1 and key < current_node.right_child_node.object.userNum:
            self.root.right_child_node = self.right_rotate(current_node.right_child_node)
            return self.left_rotate(current_node)

        # Return the new balanced root of the tree
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

    # Function that will fix a tree that has been balanced
    def fix_tree(self, subtree_root):
        seperator = 2**(self.get_height(self.root) - 2)
        level_seperators = [0]
        for idx in range(1, self.tree_height):
            level_seperators.append(seperator)
            # print(seperator)
            seperator = seperator / 2
        self.fix_tree_helper(subtree_root, subtree_root, level_seperators)
        return

    # Recursive helper function for the tree
    def fix_tree_helper(self, subtree_root, current_node, level_seperators):
        if current_node is not None:
            if current_node.parent is not None:
                if current_node.object.userNum <= current_node.parent.object.userNum:
                    current_node.object.aniQueue.put(movement.Movement(current_node.object.x, current_node.object.y, self.step, ['delete_line']))
                    current_node.object.aniQueue.put(movement.Movement(current_node.parent.object.x - (self.size * level_seperators[self.get_depth(current_node) - 1]), current_node.parent.object.y + 50, self.step))
                    current_node.object.x = current_node.parent.object.x - (self.size * level_seperators[self.get_depth(current_node) - 1])
                    current_node.object.y = current_node.parent.object.y + 50
                else:
                    current_node.object.aniQueue.put(movement.Movement(current_node.object.x, current_node.object.y, self.step, ['delete_line']))
                    current_node.object.aniQueue.put(movement.Movement(current_node.parent.object.x + (self.size * level_seperators[self.get_depth(current_node) - 1]), current_node.parent.object.y + 50, self.step))
                    current_node.object.x = current_node.parent.object.x + (self.size * level_seperators[self.get_depth(current_node) - 1])
                    current_node.object.y = current_node.parent.object.y + 50

                # Create the new line
                if current_node.parent is not None:
                    current_node.object.aniQueue.put(movement.Movement(-1,-1,self.step,[],
                    [current_node.parent.object.x + (self.size / 2), current_node.parent.object.y + self.size,
                     current_node.object.x + (self.size / 2), current_node.object.y]))
            else:
                current_node.object.aniQueue.put(movement.Movement(current_node.object.x, current_node.object.y, self.step, ['delete_line']))
                current_node.object.aniQueue.put(movement.Movement(self.xorigin + (self.width / 2) - (self.size / 2), self.height / 15, self.step))
                current_node.object.x = self.xorigin + (self.width / 2) - (self.size / 2)
                current_node.object.y = self.height / 15

            self.fix_tree_helper(subtree_root, current_node.left_child_node, level_seperators)
            self.fix_tree_helper(subtree_root, current_node.right_child_node, level_seperators)
            return


    # Function that will perform a left rotation using the parent node
    #       z           y
    #        \         / \
    #         y   ->  z   x
    #        / \       \
    #      T2   x       T2
    def left_rotate(self, z):
        # Perform the left rotation
        y = z.right_child_node
        T2 = y.left_child_node
        z.right_child_node = T2

        if T2 is not None:
            T2.parent = z

        y.parent = z.parent
        y.left_child_node = z
        z.parent = y

        # Calculate the new heights for the nodes
        z.height = 1 + max(self.get_height(z.left_child_node),
                           self.get_height(z.right_child_node))
        y.height = 1 + max(self.get_height(y.left_child_node),
                           self.get_height(y.right_child_node))
        self.fix_tree(y)
        # Return the new top level node
        return y

    # Function that will perform a right rotation using the parent node
    #       z           y
    #      /           / \
    #     y     ->    x   z
    #    / \             /
    #   x   T3         T3
    def right_rotate(self, z):
        # Perform the right rotation
        y = z.left_child_node
        T3 = y.right_child_node
        y.right_child_node = z
        z.left_child_node = T3

        if T3 is not None:
            T3.parent = z

        y.parent = z.parent
        y.right_child_node = z
        z.parent = y

        self.fix_tree(y)

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

    # Implements a preorder traversal that will move the nodes to fit the new tree height
    def preorder_resize(self, current_node):
        # Root node will never have to be moved
        if current_node is not None:
            if current_node.object.userNum <= self.root.object.userNum:
                # Move the node to its new location, based on its old location
                current_node.object.aniQueue.put(movement.Movement(current_node.object.x, current_node.object.y,
                                                                   self.step, ['delete_line']))
                current_node.object.aniQueue.put(movement.Movement(self.root.object.x - ((self.root.object.x - current_node.object.x) * 2),
                                                                   current_node.object.y))
                current_node.object.x = self.root.object.x - ((self.root.object.x - current_node.object.x) * 2)
            else:
                # Move the node to its new location, based on its old location
                current_node.object.aniQueue.put(movement.Movement(current_node.object.x, current_node.object.y,
                                                                   self.step, ['delete_line']))
                current_node.object.aniQueue.put(movement.Movement(self.root.object.x + ((current_node.object.x - self.root.object.x) * 2),
                                                                   current_node.object.y))
                current_node.object.x = self.root.object.x + ((current_node.object.x - self.root.object.x) * 2)
            # Create the new line
            if current_node.parent is not None:
                current_node.object.aniQueue.put(movement.Movement(-1,-1,self.step,[],
                [current_node.parent.object.x + (self.size / 2), current_node.parent.object.y + self.size,
                 current_node.object.x + (self.size / 2), current_node.object.y]))

            self.preorder_resize(current_node.left_child_node)
            self.preorder_resize(current_node.right_child_node)

    # Function that will initiate the resize of the tree
    def resize_tree(self, height):
        self.preorder_resize(self.root)
        return

# Function that will start the avl tree algorithm
def start_avl_tree(aniList, x_origin, y_origin, width, height):
    # Initialize the AVL tree object
    tree = AVLTreeAnimation(30, x_origin, width, height, aniList)

    # Loop and wait for more elements to insert, delete, and search for
    while True:
        tree.insert(1)
        time.sleep(5)
        tree.insert(2)
        time.sleep(5)
        tree.insert(0)
        time.sleep(5)
        tree.insert(6)
        """
        time.sleep(5)
        tree.insert(-1)
        time.sleep(5)
        tree.insert(-0.5)
        time.sleep(5)
        tree.insert(1.5)
        """

        break
