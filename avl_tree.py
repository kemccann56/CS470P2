"""
AVL Tree Animation Implementation

Group 3: Andrew Hankins, Alex Reese, Manjiri Gunaji, Kyle McCann, Nicholas Callahan
Luke Lindsay, and Shelby Deerman

References:
-----------
https://www.geeksforgeeks.org/introduction-to-avl-tree/
https://www.programiz.com/dsa/avl-tree
"""
import animation
from queue import Queue

"""
A class to represent a node in an AVL tree
"""
class AVLTreeNode():
    def __init__(self, object, parent):
        self.object           = object
        self.parent           = parent
        self.left_child_node  = None
        self.right_child_node = None
        self.height           = 1
        self.level            = 0

"""
A class to represent an AVL Tree

Insertion: O(log(N))
Deletion: O(log(N))
Search: O(log(N))
"""
class AVLTreeAnimation():

    """
    Initialize the global tree variables
    Parameters:
    -----------
    step : int
        The current step of the animation that we are on.
    size : int
        The width of the nodes in the tree.
    xorigin : int
        The x origin that will be used to position the animation.
    width : int
        The width of the screen section we are allowed to use.
    height : int
        The height of the screen section we are allowed to use.
    aniList : list
        List of animation objects that we should append to.
    y_distance : int
        The distance between each level of the tree.
    """
    def __init__(self, size, xorigin, yorigin, width, height, aniList, y_distance):
        self.step = 0 # Step of the animation the tree is currently on
        self.size = size # Size of each node in the tree
        self.tree_height = 0 # Num of levels in the tree
        self.xorigin = xorigin # xorigin of screen section
        self.y_origin = yorigin # y origin of screen section
        self.width = width # Width of screen section
        self.height = height # Height of screen section
        self.root = None # The topmost node of the tree
        self.aniList = aniList # List of animations to be made (only append)
        self.y_distance = y_distance # Distance between the levels of the tree

    """
    Function that users should call to insert a key to the AVL tree.
    Parameters:
    -----------
    key : int
        The key to be inserted into the tree.
    """
    def insert(self, key):
        # Perform a standard binary tree insert then rotate any unbalanced subtrees
        self.root = self.insert_helper(key, self.root, None)
        # If the currently stored tree height is off by more than one, resize
        # the tree to match it. This is included to prevent any unnecessary
        # resizing.
        if self.tree_height > self.get_height(self.root) + 1:
            self.resize_tree(self.get_height(self.root))

    """
    Function that will recursively search for the location of where the new node
    should be inserted. After this, the tree will be balanced as we go up the
    tree.
    Parameters:
    -----------
    key : int
        The key of the node that we want to delete.
    current_node : AVLTreeNode
        The node that we are currently looking at.
    parent : AVLTreeNode
        The parent of the node we are currently looking at. This will be used
        when initializing a new node object that is being inserted.
    Returns:
    --------
    AVLTreeNode
        The root of each balanced subtree.
    """
    def insert_helper(self, key, current_node, parent):
        # Reached the bottom of the tree
        if current_node is None:
            # Create new node which includes the animation object
            new_object = animation.Object(key)
            self.aniList.append(new_object)
            new_node = AVLTreeNode(new_object, parent)
            # Adding the root node
            if parent is None:
                new_object.x = self.xorigin + (self.width / 2) - (self.size / 2)
                new_object.y = self.y_origin + (self.height / 15)
                self.tree_height = 1
                self.draw_node(new_object, 'lightblue', True)
            # New leaf is being added
            else:
                new_node.level = self.get_depth(new_node)
                # Adding a level -> Resize tree
                if new_node.level > self.tree_height:
                    self.increase_size(new_node.level)
                    self.tree_height += 1
                # Calculate the nodes x and y coordinates. The distance between
                # a parent node and the child can be computed based off of the
                # level in the tree.
                seperator = 2**(self.tree_height - 2)
                level_seperators = [0]
                for idx in range(1, self.tree_height):
                    level_seperators.append(seperator)
                    seperator = seperator / 2
                # If we are adding the node to the right of the parent, add the calculated value
                if new_object.userNum > parent.object.userNum:
                    new_object.x = parent.object.x + (self.size * level_seperators[self.get_depth(new_node) - 1])
                    new_object.y = parent.object.y + self.y_distance
                # If we are adding the node to the left of the parent, subtract the calculated value
                else:
                    new_object.x = parent.object.x - (self.size * level_seperators[self.get_depth(new_node) - 1])
                    new_object.y = parent.object.y + self.y_distance
                # Draw the new node onto the screen
                self.draw_node(new_object, 'lightblue', False)
                # Create line to the parent node
                self.draw_line(new_node, True)
                # Reset the parent node's color
                self.color_node(parent, 'lightblue', True)
            return new_node
        # New node is to the left of the current one
        elif key <= current_node.object.userNum:
            # Moving on from current node
            if parent is not None:
                self.color_node(parent, 'lightblue', False)
            self.color_node(current_node, 'gold', True)
            current_node.left_child_node = self.insert_helper(key, current_node.left_child_node, current_node)
        # New node is to the right of the current one
        else:
            # Moving on from current node
            if parent is not None:
                self.color_node(parent, 'lightblue', False)
            self.color_node(current_node, 'gold', True)
            current_node.right_child_node = self.insert_helper(key, current_node.right_child_node, current_node)

        # The node's new height will be the maximum child's heigth plus itself.
        # Used when we are climbing back up the tree and rotating as necessary.
        current_node.height = 1 + max(self.get_height(current_node.left_child_node),
                                      self.get_height(current_node.right_child_node))

        # Get the new balance factor for the current node
        balance_factor = self.get_balance(current_node)
        # Right Rotation
        if balance_factor > 1 and key < current_node.left_child_node.object.userNum:
            node = self.right_rotate(current_node)
            self.fix_tree(node, False)
            return node
        # Left Rotation
        if balance_factor < -1 and key > current_node.right_child_node.object.userNum:
            node = self.left_rotate(current_node)
            self.fix_tree(node, False)
            return node
        # Left-Right Rotation
        if balance_factor > 1 and key > current_node.left_child_node.object.userNum:
            node = self.left_rotate(current_node.left_child_node)
            self.fix_tree(node, False)
            current_node.left_child_node = node
            node = self.right_rotate(node)
            self.fix_tree(node, False)
            return node
        # Right-Left Rotation
        if balance_factor < -1 and key < current_node.right_child_node.object.userNum:
            node = self.right_rotate(current_node.right_child_node)
            self.fix_tree(node, False)
            current_node.right_child_node = node
            node = self.left_rotate(current_node)
            self.fix_tree(node, False)
            return node
        # Subtree is balanced
        return current_node

    """
    Function that users should call to delete a node from the tree.
    Parameters:
    -----------
    key : int
        The key to be deleted from the tree.
    """
    def delete(self, key):
        # Perform a standard binary tree using the deleted nodes sucessor. Then
        # rotate any unbalanced subtrees
        self.root = self.delete_node_helper(self.root, key)
        # If the currently stored tree height is off by more than one, resize
        # the tree to match it. This is included to prevent any unnecessary
        # resizing.
        if self.tree_height > self.get_height(self.root) + 1:
            self.decrease_size(self.get_height(self.root))

    """
    Function that will recursively search for the node to delete, and perform
    a standard binary search delete. After this, the tree will be balanced as
    we go up the tree.
    Parameters:
    -----------
    node : AVLTreeNode
        The node that should be checked.
    key : int
        The key of the node that we want to delete.
    Returns:
    --------
    AVLTreeNode
        The root of each balanced subtree.
    """
    def delete_node_helper(self, node, key):
        # Reached the bottom of the tree
        if node is None:
            return node
        # Node to be deleted is to the left
        elif key < node.object.userNum:
            if node.parent is not None:
                self.color_node(node.parent, 'lightblue', False)
            self.color_node(node, 'gold', True)
            node.left_child_node = self.delete_node_helper(node.left_child_node, key)
        # Node to be deleted is to the right
        elif key > node.object.userNum:
            if node.parent is not None:
                self.color_node(node.parent, 'lightblue', False)
            self.color_node(node, 'gold', True)
            node.right_child_node = self.delete_node_helper(node.right_child_node, key)
        # This is the node that needs to be deleted
        else:
            # Indicate we have found the node to delete in the animation
            if node.parent is not None:
                self.color_node(node.parent, 'lightblue', False)
            self.color_node(node, 'green', True)
            # No children
            if node.left_child_node is None and node.right_child_node is None:
                self.delete_node_from_animation(node, True)
                if node.parent is not None:
                    if node.object.userNum <= node.parent.object.userNum:
                        node.parent.left_child_node = None
                    else:
                        node.parent.right_child_node = None
                return None
            # Right child only
            elif node.left_child_node is None:
                temp = node.right_child_node
                self.color_node(temp, 'red1', True)
                temp.parent = node.parent
                if temp.object.userNum <= temp.parent.object.userNum:
                    temp.parent.left_child_node = temp
                else:
                    temp.parent.right_child_node = temp
                self.delete_node_from_animation(node, True)
                self.fix_tree(temp, False)
                node = None
                return temp
            # Left child only
            elif node.right_child_node is None:
                temp = node.left_child_node
                self.color_node(temp, 'red1', True)
                temp.parent = node.parent
                if temp.object.userNum <= temp.parent.object.userNum:
                    temp.parent.left_child_node = temp
                else:
                    temp.parent.right_child_node = temp
                self.delete_node_from_animation(node, True)
                self.fix_tree(temp, False)
                node = None
                return temp
            # Node to be deleted has both children so use successor as a replacement
            temp = self.get_successor(node.right_child_node)
            node.object.userNum = temp.object.userNum
            node.object.aniQueue.put(animation.Movement(-1,-1,self.step,['change_text',str(temp.object.userNum)]))
            self.step += 1
            node.right_child_node = self.delete_node_helper(node.right_child_node, temp.object.userNum)

        # If the tree is empty, no balancing needs to be done
        if node is None:
            return node

        # Calculate the new height of the node
        node.height = 1 + max(self.get_height(node.left_child_node),
                              self.get_height(node.right_child_node))
        # Get the new balance factor for the current node
        balance_factor = self.get_balance(node)
        # Right Rotate
        if balance_factor > 1 and self.get_balance(node.left_child_node) >= 0:
            new_node = self.right_rotate(node)
            self.fix_tree(new_node, False)
            return new_node
        # Left Rotate
        if balance_factor < -1 and self.get_balance(node.right_child_node) <= 0:
            new_node = self.left_rotate(node)
            self.fix_tree(new_node, False)
            return new_node
        # Left-Right Rotate
        if balance_factor > 1 and self.get_balance(node.left_child_node) < 0:
            new_node = self.left_rotate(node.left_child_node)
            self.fix_tree(new_node, False)
            node.left_child_node = new_node
            new_node = self.right_rotate(new_node)
            self.fix_tree(new_node, False)
            return new_node
        # Right-Left Rotate
        if balance_factor < -1 and self.get_balance(node.right_child_node) > 0:
            new_node = self.right_rotate(node.right_child_node)
            self.fix_tree(new_node, False)
            node.right_child_node = new_node
            new_node = self.left_rotate(node)
            self.fix_tree(new_node, False)
            return new_node
        # Subtree is balanced
        return node

    """
    Function that will search for the desired key.
    Parameters:
    -----------
    key : int
        The key of the node that we are searching for.
    Returns:
    --------
    AVLTreeNode
        The found node.
        NOTE: If no node is found, then None is returned.
    """
    def search(self, key):
        node = self.search_helper(key, self.root)
        self.color_node(node, 'lightblue', True)
        return node

    """
    Recursive helper function for search.
    Parameters:
    -----------
    key : int
        The key of the node that we are searching for.
    node : AVLTreeNode
        The node that we are currently at in the tree.
    Returns:
    --------
    AVLTreeNode
        The found node.
        NOTE: If no node is found, then None is returned.
    """
    def search_helper(self, key, node):
        found_node = None
        if node is not None:
            self.color_node(node, 'gold', True)
            if key == node.object.userNum:
                self.color_node(node, 'green', True)
                return node
            elif key < node.object.userNum:
                self.color_node(node, 'lightblue', False)
                found_node = self.search_helper(key, node.left_child_node)
                return found_node
            else:
                self.color_node(node, 'lightblue', False)
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
    Parameters:
    -----------
    z : AVLTreeNode
        The original top level node of the section that will be rotated.
    Returns:
    --------
    AVLTreeNode:
        The new top level node of the section that was rotated.
    """
    def left_rotate(self, z):
        # Get the nodes that will be rotated
        y = z.right_child_node
        T2 = y.left_child_node
        # Color all of the nodes that will be moved
        self.color_node(z, 'red1', False)
        self.color_node(y, 'red1', False)
        if T2 is not None:
            T2.parent = z # Set T2's parent if necessary
            self.color_node(T2, 'red1', False)
        if y.right_child_node is not None:
            self.color_node(y.right_child_node, 'red1', True)
        # Rotate the nodes
        z.right_child_node = T2
        y.parent = z.parent
        y.left_child_node = z
        z.parent = y
        # Update the root if necessary
        if z == self.root:
            self.root = y
        # Calculate the new heights for rotated nodes
        z.height = 1 + max(self.get_height(z.left_child_node),
                           self.get_height(z.right_child_node))
        y.height = 1 + max(self.get_height(y.left_child_node),
                           self.get_height(y.right_child_node))
        # Return the new parent node
        return y

    """
    Function that will perform a right rotation using the parent node
          z           y
         /           / \
        y     ->    x   z
       / \             /
      x   T3         T3
    Parameters:
    -----------
    z : AVLTreeNode
        The original top level node of the section that will be rotated.
    Returns:
    --------
    AVLTreeNode:
        The new top level node of the section that was rotated.
    """
    def right_rotate(self, z):
        # Get the nodes that will be rotated
        y = z.left_child_node
        T3 = y.right_child_node
        y.right_child_node = z
        # Color all of the nodes that will be moved
        self.color_node(z, 'red1', False)
        self.color_node(y, 'red1', False)
        if T3 is not None:
            self.color_node(T3, 'red1', False)
            T3.parent = z # Set T3's parent if necessary
        if y.left_child_node is not None:
            self.color_node(y.left_child_node, 'red1', True)
        # Rotate the nodes
        z.left_child_node = T3
        y.parent = z.parent
        y.right_child_node = z
        z.parent = y
        # Calculate the new heights for the nodes
        z.height = 1 + max(self.get_height(z.left_child_node),
                           self.get_height(z.right_child_node))
        y.height = 1 + max(self.get_height(y.left_child_node),
                           self.get_height(y.right_child_node))
        # Return the new parent node
        return y

    """
    Return the height of the node.
    Parameters:
    -----------
    node : AVLTreeNode
        The node whose height we want.
    """
    def get_height(self, node):
        if node is None:
            return 0
        return node.height

    """
    Gets the level that the node is currently at in the tree.
    Parameters:
    -----------
    node : AVLTreeNode
        The node whose level in the tree we want.
    Returns:
    --------
    int
        The level that the node is on.
    """
    def get_depth(self, node):
        depth = 0
        while node is not None:
            depth += 1
            node = node.parent
        return depth

    """
    Get the balance of the given node.
    Parameters:
    -----------
    node : AVLTreeNode
        The node whose balance we want.
    Returns:
    --------
    int
        An integer representing the node's balance. If the node is unbalanced to
        the left, the returned value will be positive. If the node is unbalanced
        to the right, a negative value will be returned.
    """
    def get_balance(self, node):
        if node is None:
            return 0
        return self.get_height(node.left_child_node) - \
               self.get_height(node.right_child_node)

    """
    Gets the successor to the given node.
    Parameters:
    -----------
    node : AVLTreeNode
        The node that we are currently on. If this is set to None, we know that
        the prevous node was the sucessor.
    Returns:
    --------
    AVLTreeNode
        The successor to the given node
    """
    def get_successor(self, node):
        if node.parent is not None:
            self.color_node(node.parent, 'gold', False)
        self.color_node(node, 'gold', True)
        # The node farthest to the left in the subtree will be the successor
        if node is None:
            self.color_node(node.parent, 'green', True)
            return node
        elif node.left_child_node is None:
            self.color_node(node, 'green', True)
            return node
        return self.get_successor(node.left_child_node)


    """
    Function that should be called when the tree size can be decreased.
    Parameters:
    height : int
        The current height of the tree. This height will be decreased by one.
    """
    def decrease_size(self, height):
        # Resize the entire tree (deletes all lines)
        self.decrease_size_helper(self.root)
        self.step += 1
        # Go through and re-add all of the lines
        self.add_lines_helper(self.root)
        self.step += 1
        self.tree_height -= 1
        return

    """
    Implements a preorder traversal that will move the nodes to fit the new tree
    height.

    Calculation:
    ------------
    When decreasing the tree size, every node's distance from the root should be
    cut in half.
    Ex:
    When going from a height 4 -> height 3 tree, the root's child nodes will go
    from being
        root.x (+ or -) 4*size --> root.x (+ or -) 2*size.
    This principle holds for all nodes in the tree.

    Parameters:
    -----------
    current_node : AVLTreeNode
        The node that we are currently moving.
        NOTE: The first node passed in should always be the root of the tree.
    """
    def decrease_size_helper(self, current_node):
        if current_node is not None:
            # Node is to the left of its parent
            if current_node.object.userNum <= self.root.object.userNum:
                self.delete_line(current_node, False)
                self.move_node(self.root.object.x - ((self.root.object.x - current_node.object.x) / 2),
                               current_node.object.y, current_node, False)
            # Node is to the right of its parent
            else:
                self.delete_line(current_node, False)
                self.move_node(self.root.object.x + ((current_node.object.x - self.root.object.x) / 2),
                               current_node.object.y, current_node, False)
            self.decrease_size_helper(current_node.left_child_node)
            self.decrease_size_helper(current_node.right_child_node)


    """
    Function that should be called when the tree needs to be resized:
    Parameters:
    -----------
    height : int
        The height of the tree that the resize should be based on.
    """
    def increase_size(self, height):
        # Resize the entire tree (deletes all lines)
        self.increase_size_helper(self.root)
        self.step += 1
        # Go through and re-add all of the lines
        self.add_lines_helper(self.root)
        self.step += 1
        return


    """
    Implements a preorder traversal that will move the nodes to fit the new tree height

    Calculation:
    ------------
    When expanding the tree every node's distance from the root node should double.
    Ex:
    In when going from a height 3 -> height 4 tree, the root's child nodes will go from being
        root.x (+ of -) 2*size --> root.x (+ or -) 4*size
    This  principle holds for all nodes in the tree

    Parameters:
    -----------
    current_node : AVLTreeNode
        The node that we are currently moving.
        NOTE: The first node should always be the root of the tree.
    """
    def increase_size_helper(self, current_node):
        if current_node is not None:
            # Node is to the left of its parent
            if current_node.object.userNum <= self.root.object.userNum:
                self.delete_line(current_node, False)
                self.move_node(self.root.object.x - ((self.root.object.x - current_node.object.x) * 2), current_node.object.y, current_node, False)
            # Node is to the right of its parent
            else:
                self.delete_line(current_node, False)
                self.move_node(self.root.object.x + ((current_node.object.x - self.root.object.x) * 2), current_node.object.y, current_node, False)
            self.increase_size_helper(current_node.left_child_node)
            self.increase_size_helper(current_node.right_child_node)

    """
    Function that should be called when part of the tree needs to be updated
    on the screen.
    Parameters:
    -----------
    subtree_root : AVLTreeNode
        The root of the subtree that needs to be updated.
    increment_step : bool
        Determines whether or not a the step count will be incremented when
        updating the tree animation.
        NOTE: This value will be used for all animation updates, so setting as
              True significantly increases the time it takes to update the tree.
    """
    def fix_tree(self, subtree_root, increment_step):
        # See fix_tree_helper documentation for more infor about the level seperators
        seperator = 2**(self.tree_height - 2)
        level_seperators = [0]
        for idx in range(1, self.tree_height):
            level_seperators.append(seperator)
            seperator = seperator / 2
        self.delete_lines_helper(subtree_root)
        self.fix_tree_helper(subtree_root, subtree_root, level_seperators, increment_step)
        # Make sure tree is fixed resetting the nodes' color
        self.step += 1
        self.reset_color(subtree_root)
        return

    """
    Recursive helper function for the updating the tree on the screen. This
    works by repositioning the nodes in the subtree based on their level, and the
    position of the subtree's root.
    Parameters:
    -----------
    subtree_root : AVLTreeNode
        The root of the subtree whose node's need to be updated on the screen.
        NOTE: This node must be in the right position.
    current_node : AVLTreeNode
        The node in the subtree that we are currently updating.
    level_seperators : list
        A list of integers that indicates the x distance a node should be from
        their parent. For example the list [0, 4, 2, 1] indicates that for a height
        4 tree, nodes at level 2 should be (4 * size) away from their parent.
    increment_step : bool
        Determines whether or not the step count should be incrementing when
        updating the animation.
    """
    def fix_tree_helper(self, subtree_root, current_node, level_seperators, increment_step):
        if current_node is not None:
            if current_node.parent is not None: # If we are not at the root node
                if current_node.object.userNum <= current_node.parent.object.userNum:
                    if current_node.object.x != current_node.parent.object.x - (self.size * level_seperators[self.get_depth(current_node) - 1]):
                        self.delete_line(current_node, increment_step)
                        self.move_node(current_node.parent.object.x - (self.size * level_seperators[self.get_depth(current_node) - 1]),
                                       current_node.parent.object.y + self.y_distance,
                                       current_node,
                                       increment_step)
                        self.draw_line(current_node, increment_step)
                else:
                    if current_node.object.x != current_node.parent.object.x + (self.size * level_seperators[self.get_depth(current_node) - 1]):
                        self.delete_line(current_node, increment_step)
                        self.move_node(current_node.parent.object.x + (self.size * level_seperators[self.get_depth(current_node) - 1]),
                                       current_node.parent.object.y + self.y_distance,
                                       current_node,
                                       increment_step)
                        self.draw_line(current_node, increment_step)
            else: # Node is the root so remove any line that was attatched to it
                self.delete_line(current_node, increment_step)
                self.move_node(self.xorigin + (self.width / 2) - (self.size / 2), self.y_origin + (self.height / 15), current_node, increment_step)

            self.fix_tree_helper(subtree_root, current_node.left_child_node, level_seperators, increment_step)
            self.fix_tree_helper(subtree_root, current_node.right_child_node, level_seperators, increment_step)
            return

    """
    Recursive Function that will reset all of the nodes colors in the subtree
    using a preorder traversal.
    Parameters:
    -----------
    current_node : AVLTreeNode
        The node that the traversal will start at.
    """
    def reset_color(self, current_node):
        if current_node is not None:
            self.color_node(current_node, 'lightblue', False)
            self.reset_color(current_node.left_child_node)
            self.reset_color(current_node.right_child_node)

    """
    Recursive helper to add lines to a subtree using a preorder traversal.
    Parameters:
    -----------
    current_node : AVLTreeNode
        The node that the traversal will start at.
    """
    def add_lines_helper(self, current_node):
        if current_node is not None:
            if current_node.parent is not None:
                self.draw_line(current_node, False)
            self.add_lines_helper(current_node.left_child_node)
            self.add_lines_helper(current_node.right_child_node)
        return

    """
    Recursive helper to delete all the lines of a subtree using a preorder
    traversal.
    Parameters:
    -----------
        current_node : AVLTreeNode
            The node that the traversal will start at.
    """
    def delete_lines_helper(self, current_node):
        if current_node is not None:
            if current_node.parent is not None:
                self.delete_line(current_node, False)
            self.delete_lines_helper(current_node.left_child_node)
            self.delete_lines_helper(current_node.right_child_node)
        return

    """
    Draws a new node onto the screen.
    Parameters:
    -----------
    animation_object : Object
        The animation object that needs to be drawn. This object's aniQueue, x, y,
        and userNum variables must be already set.
    color : str
        The color that the new node should be.
    increment_step : bool
        Determines whether of not the step count will be incremented after the
        line is drawn.
    """
    def draw_node(self, animation_object, color, increment_step):
        animation_object.aniQueue.put(animation.Movement(-1, -1, self.step, [], [],
            ['oval', animation_object.x, animation_object.y, self.size,
            str(animation_object.userNum), color]))
        if increment_step:
            self.step += 1
        return

    """
    Draws a line to the node's parent.
    NOTE: The given node must have a parent (can't be the root)
    Parameters:
    -----------
    node : AVLTreeNode
        The child node that needs to have a line drawn to it's parent.
    increment_step : bool
        Determines whether or not the step count will be incremented after the
        line is drawn.
    """
    def draw_line(self, node, increment_step):
        node.object.aniQueue.put(animation.Movement(-1, -1, self.step, [],
            [node.parent.object.x + (self.size / 2), node.parent.object.y + self.size,
             node.object.x + (self.size / 2), node.object.y]))
        if increment_step:
            self.step += 1
        return

    """
    Deletes the line connecting the node to its parent.
    Parameters:
    -----------
    node : AVLTreeNode
        The child node that is currently connected to it's parent.
    increment_step : bool
        Determines whether of not the step count will be incremented after the
        line deletion.
    """
    def delete_line(self, node, increment_step):
        node.object.aniQueue.put(animation.Movement(node.object.x, node.object.y, self.step, ['delete_line']))
        if increment_step:
            self.step += 1
        return

    """
    Updates the given node's coordinates to the x and y values and adds the
    movement to the animation queue.
    Parameters:
    -----------
    x : int
        The x value that the node should move to.
    y : int
        The y value that the node should move to.
    node : AVLTreeNode
        The node needs to be moved.
    increment_step : bool
        Determines wheter or not the step count will be incremented after the
        recoloring.
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
    Parameters:
    -----------
    node : AVLTreeNode
        The node that will be recolored
    color : str
        The color that the node should be changed to.
    increment_step : bool
        Determines whether of not the step count will be incremented after the
        recoloring.
    """
    def color_node(self, node, color, increment_step):
        node.object.aniQueue.put(animation.Movement(-1, -1, self.step, [color]))
        if increment_step:
            self.step += 1
        return

    """
    Deletes a node from the animation.
    Parameters:
    -----------
    node : AVLTreeNode
        The node to be removed from the animation.
    increment_step : bool
        Determines whether or not the step count will be incremented after the
        deletion.
    """
    def delete_node_from_animation(self, node, increment_step):
        node.object.aniQueue.put(animation.Movement(-1, -1, self.step, ['delete_shape']))
        if increment_step:
            self.step += 1
        return

    """
    Prints out the desired value from each node based on a preorder traversal of
    the tree. Mainly used for debugging purposes.
    Parameters:
    -----------
    root : AVLTreeNode
        The root node of the tree tree where the preorder traversal should start.
    """
    def preorder(self, root):
        #if root is None return
        if root==None:
            return
        #traverse root
        print("Node: " + str(root.object.userNum) + " Height: " + str(root.height))
        #traverse left subtree
        self.preorder(root.left_child_node)
        #traverse right subtree
        self.preorder(root.right_child_node)


"""
The function that should be called when initializing an AVL tree animation.
NOTE: This function will block and wait for more input.
Parameters:
-----------
aniList : list
    The data structure that the Movement objects should be appended to. Append
    is the only permissable action for this list.
x_origin: int
    The x origin that will be used to position the animation. For this case,
    it should always be 0.
y_origin : int
    The y origin that will be used to position the animation.
width : int
    The total width of the animation window we are allowed to use.
height : int
    The total heigth of the animation window we are allowed to use.
"""
def start_avl_tree(aniList, x_origin, y_origin, width, height):
    # Initialize the AVL tree object
    tree = AVLTreeAnimation(35, x_origin, y_origin, width, height, aniList, 50)
    # Loop and wait for more elements to insert, delete, and search for
    while True:
        tree.insert(1)
        tree.insert(2)
        tree.insert(3)
        tree.insert(4)
        tree.insert(5)
        tree.delete(2)
        break
