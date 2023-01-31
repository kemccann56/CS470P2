# AVL Tree

## Description

Self-balancing binary search tree that is balanced based off of the
height of each node's children. This value is called the balancing factor
and is generally either a value of -1, 0, +1.

```
Balance Factor = (Height of Left Subtree - Height of Right Subtree) or
                 (Height of Right Subtree - Height of Left Subtree)
```

## Runtime

Insertion: O(log(N))
Deletion: O(log(N))
Search: O(log(N))

## Algorithm

In order to keep the tree balanced, right and left rotations are used.

### Left Rotation

In left rotation, we take a nodes right child and move it up to take
its parent's position.

```
 z           y
  \         / \
   y   ->  z   x
  / \       \
T2   x       T2
```

#### Pseudocode
```
if x
```


### Right Rotation

In rigth rotation, we take a node's left child and move it up to take
its parent's position.

```
    z           y
   /           / \
  y     ->    x   z
 / \             /
x   T3         T3
```

