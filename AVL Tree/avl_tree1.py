import sys
import movement


# A class to represent a node in an AVL tree
class TreeNode():
    def __init__(self, value):
        self.value            = value
        self.left_child_node  = None
        self.right_child_node = None
        self.height           = 1

# A class to represent an AVL Tree
#
# Insertion: O(log(N))
# Deletion: O(log(N))
# Search: O(log(N))
class AVLTree():
    # Function that will insert the specified key into the tree using recursion
    def insert(self, root, key):
        if root is None:
            # If the tree is empty, then create the root node
            return TreeNode(key)
        elif key <= root.value:
            # If the new key is less than or equal to the current node's,
            # go to the left child node
            root.left_child_node = self.insert(root.left_child_node, key)
        else:
            # If the new key is greater than the current node's,
            # go the the right child node
            root.right_child_node = self.insert(root.right_child_node, key)

        # The node's new height will be the maximum child's heigth plus one
        root.height = 1 + max(self.get_height(root.left_child_node),
                              self.get_height(root.right_child_node))

        # Get the new balance factor for the current node
        balance_factor = self.get_balance(root)

        if balance_factor > 1 and key < root.left_child_node:
            return self.right_rotate(root)

        if balance_factor < -1 and key > root.right_child_node.value:
            return self.left_rotate(root)

        if balance_factor > 1 and key > root.left_child_node.value:
            root.left_child_node = self.left_rotate(root.left_child_node)
            return self.right_rotate(root)

        if balance_factor < -1 and key < root.right_child_node.value:
            self.root.right_child_node = self.right_rotate(root.right_child_node)
            return self.left_rotate(root)

        # Return the new balanced root of the tree
        return root

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
        y.left_child_node = z

        # Calculate the new heights for the nodes
        z.height = 1 + max(self.get_height(z.left_child_node),
                           self.get_height(z.right_child_node))
        y.height = 1 + max(self.get_height(y.left_child_node),
                           self.get_height(y.right_child_node))

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

    # Print out the current tree
    def printHelper(self, currPtr, indent, last):
        if currPtr != None:
            sys.stdout.write(indent)
            if last:
                sys.stdout.write("R----")
                indent += "     "
            else:
                sys.stdout.write("L----")
                indent += "|    "
            print(currPtr.value)
            self.printHelper(currPtr.left_child_node, indent, False)
            self.printHelper(currPtr.right_child_node, indent, True)

# Function that will start the avl tree algorithm
def start_avl_tree(aniList, x_origin, y_origin, width, height):
    # Animation step that we are on
    step = 0
    # Initialize the AVL tree object
    tree = AVLTree()
    # Tree is initially empty
    root = None

    # Maximum size of the data structure
    max_size = 50

    # Loop and wait for more elements to insert, delete, and search for

    while True:
        break

# Start the algorithm
# start_avl_tree()
