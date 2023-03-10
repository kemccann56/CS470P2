# CS470P2 : AVL & RB Trees

## Group 3:
Andrew Hankins, Alex Reese, Manjiri Gunaji, Kyle McCann, Nicholas Callahan, Luke Lindsay, and Shelby Deerman

## Overview
As part of this project, we implemented three well-known algorithms, Van Emde Boas trees, AVL trees, and Red-Black trees. To better understand the working of these data structures, we used Python to create animations that depict the insertion, deletion, and searching of elements in the tree. For this purpose, we utilized the Tkinter library, a widely-used Python GUI toolkit.

In addition to the code and animations, we created a presentation highlighting the unique features of each algorithm and comparing their performance in terms of time complexity and space efficiency. The presentation also discussed the advantages and disadvantages of each data structure and provided use case scenarios where one data structure might be preferable over the others.

## Prerequisites
The application has been designed to work with Python 3, and as such, the only requirement is to have Python 3 installed on your system. Fortunately, Python 3 already includes the necessary tkinter library, so there's no need to install anything else. It's worth noting that the application has been tested extensively with Python version 3.10.6, so we recommend using this version to ensure compatibility.

## Repository Structure
```
CS470P2/
├── AVLtree.py : Primary implementation of the AVL tree including animations.
├── HW2.py : The main file that will be run in order to start the animation.
├── RBtree.py : Primary implementation of the RB tree including animations.
├── VEBtree.py : Primary implementation of the VEB tree including animations. This version optimizes 
|                the storage space used, and is the version that will be shown in the animation application.
├── VEBtree2.py : Secondary implementation of the VEB tree including animations. This version does not optimize 
|                 the storage of the VEB tree, and is not shown in the animation application.
├── animation.py : Animation utility classes.
├── README.md : File containing information on the project, including how to run code and other relevant details.
├── smalldataset.txt : Initial testing dataset.
├── smallerdataset.txt : Reduced testing dataset
├── Presentation.pptx : Powerpoint Presentation of the data structures.
├── Presentation.pdf : Presentation in pdf form.
```
## Instructions
1. Run `python3 HW2.py` to launch the animation application.
2. Click the `Settings` button in the lower left-hand corner.
3. Select the two data structures to be displayed and exit the settings menu.
4. Click the `Start` button.
5. Enter an integer values into either the `Insert`, `Delete`, or `Search` boxes and then click the corresponding button.

**Additional Info:**
* The speed of the animation can be modified using the scroller at the bottom right corner of the screen. This should only be used when an operation is not currently in progress.
* The keyword `all` may be used to insert 0...15 into the data structures.
* Clicking the start button will reset the page with the selected data structures.

## References
### van Emde Boas
- [johmswk Hashmap vEB](https://github.com/jhomswk/Van_Emde_Boas_Tree)
- [MIT Lecture](https://www.youtube.com/watch?v=hmReJCupbNU)
- [MIT Lecture Notes](https://ocw.mit.edu/courses/6-046j-design-and-analysis-of-algorithms-spring-2015/49c8fa24dffce58052c90d46ac800387_MIT6_046JS15_lec04.pdf)
- [Stanford Lecture Slides](https://web.stanford.edu/class/archive/cs/cs166/cs166.1146/lectures/14/Small14.pdf)

### AVL
- [GeekForGeeks](https://www.geeksforgeeks.org/introduction-to-avl-tree/)
- [Programiz](https://www.programiz.com/dsa/avl-tree)
