from tkinter import *
from queue import Queue
from threading import Thread, Lock
from animation import *
import avl_tree

###############################################################################################
# A thread that produces data
#Takes a list from mainAnimationList as an argument
def example(aniList):
    #You will need to keep thrack of what step you are on for animations
    step = 0

    #Create your data structure #AVLtree, RBtree, etc
    myList = []

    dataFile = open('smalldataset.txt', 'r')
    for line in dataFile:
        if(not line.isspace() and len(line) > 0):
            #Only time you use aniList is to append Objects
            #Do not remove or move or anything else
            aniList.append(Object(int(line)))

            #Everything in python is a pointer so populate your data structure with the aniList objects
            myList.append(aniList[-1])
    dataFile.close()

    #Once you know the size of your data set you can do the math to determine object (x,y) coordinates
    #hard Coding for example
    size = 50

    myList[0].aniQueue.put(Movement(-1,-1,step,[],[],['oval',300,50,size,str(myList[0].userNum),'lightblue']))
    myList[0].x = 300
    myList[0].y = 50

    myList[1].aniQueue.put(Movement(-1,-1,step,[],[],['oval',150,200,size,str(myList[1].userNum),'lightblue']))
    myList[1].x = 150
    myList[1].y = 200
    #Create line to parent node
    myList[1].aniQueue.put(Movement(-1,-1,step,[],[myList[1].x + size, myList[1].y, myList[0].x, myList[0].y + size]))

    myList[2].aniQueue.put(Movement(-1,-1,step,[],[],['oval',450,200,size,str(myList[2].userNum),'lightblue']))
    myList[2].x = 450
    myList[2].y = 200
    #Create line to parent node
    myList[2].aniQueue.put(Movement(-1,-1,step,[],[myList[2].x, myList[2].y, myList[0].x + size, myList[0].y + size]))

    step += 1

    myList[3].aniQueue.put(Movement(-1,-1,step,[],[],['rectangle',125,300,size,str(myList[3].userNum),'lightblue']))
    myList[3].x = 125
    myList[3].y = 300
    #Create line to parent node
    myList[3].aniQueue.put(Movement(-1,-1,step,[],[myList[3].x + size/2, myList[3].y, myList[1].x + size/2, myList[1].y + size]))

    step += 1

    myList[4].aniQueue.put(Movement(-1,-1,step,[],[],['rectangle',175,300,size,str(myList[3].userNum),'lightblue']))
    myList[4].x = 175
    myList[4].y = 300
    #Create line to parent node
    myList[4].aniQueue.put(Movement(-1,-1,step,[],[myList[4].x + size/2, myList[4].y, myList[1].x + size/2, myList[1].y + size]))

    step += 1

    #Swap exapmle
    myList[0], myList[1] = myList[1], myList[0]

    myList[0].x, myList[1].x = myList[1].x, myList[0].x
    myList[0].y, myList[1].y = myList[1].y, myList[0].y

    myList[0].aniQueue.put(Movement(myList[0].x, myList[0].y,step, ['delete_line']))
    myList[1].aniQueue.put(Movement(myList[1].x, myList[1].y,step,[], [myList[1].x + size, myList[1].y, myList[0].x, myList[0].y + size]))

    step += 1

    #Remove example
    myList[2].aniQueue.put(Movement(-1,-1, step,['delete_shape']))
    myList.pop(2) #Do not remove it from aniList

    step += 1

    print("Finished")

# A thread that produces data
#Everyone should code like this so we can move animations where we want easily
def settingOrginExample(aniList):
    orginx = 600
    orginy = 0

    #You will need to keep thrack of what step you are on for animations
    step = 0

    #Create your data structure #AVLtree, RBtree, etc
    myList = []

    dataFile = open('smalldataset.txt', 'r')
    for line in dataFile:
        if(not line.isspace() and len(line) > 0):
            #Only time you use aniList is to append Objects
            #Do not remove or move or anything else
            aniList.append(Object(int(line)))

            #Everything in python is a pointer so populate your data structure with the aniList objects
            myList.append(aniList[-1])
    dataFile.close()

    #Once you know the size of your data set you can do the math to determine object (x,y) coordinates
    #hard Coding for example
    size = 50

    myList[0].x = orginx+300
    myList[0].y = orginy+50
    myList[0].aniQueue.put(Movement(-1,-1,step,[],[],['oval',orginx+300,orginy+50,size,str(myList[0].userNum),'lightblue']))

    step += 1

    myList[1].x = orginx+150
    myList[1].y = orginy+200
    myList[1].aniQueue.put(Movement(-1,-1,step,[],[myList[1].x + size, myList[1].y, myList[0].x, myList[0].y + size],['oval',orginx+150,orginy+200,size,str(myList[1].userNum),'lightblue']))

    step += 1

    myList[2].x = orginx+450
    myList[2].y = orginy+200
    myList[2].aniQueue.put(Movement(-1,-1,step,[],[myList[2].x, myList[2].y, myList[0].x + size, myList[0].y + size],['oval',orginx+450,orginy+200,size,str(myList[2].userNum),'lightblue']))

    step += 1

    myList[3].x = orginx+125
    myList[3].y = orginy+300
    myList[3].aniQueue.put(Movement(-1,-1,step,[],[myList[3].x + size/2, myList[3].y, myList[1].x + size/2, myList[1].y + size],['rectangle',orginx+125,orginy+300,size,str(myList[3].userNum),'lightblue']))

    step += 1

    myList[4].x = orginx+175
    myList[4].y = orginy+300
    myList[4].aniQueue.put(Movement(-1,-1,step,[],[myList[4].x + size/2, myList[4].y, myList[1].x + size/2, myList[1].y + size],['rectangle',orginx+175,orginy+300,size,str(myList[3].userNum),'lightblue']))

    step += 1

    #Swap exapmle with color change
    myList[0].aniQueue.put(Movement(-1, -1,step, ['red']))
    myList[1].aniQueue.put(Movement(-1, -1,step, ['red']))
    step += 1

    myList[0], myList[1] = myList[1], myList[0]

    myList[0].x, myList[1].x = myList[1].x, myList[0].x
    myList[0].y, myList[1].y = myList[1].y, myList[0].y

    myList[0].aniQueue.put(Movement(myList[0].x, myList[0].y,step, ['delete_line']))
    myList[1].aniQueue.put(Movement(myList[1].x, myList[1].y,step,[], [myList[1].x + size, myList[1].y, myList[0].x, myList[0].y + size]))

    myList[0].aniQueue.put(Movement(-1, -1,step, ['lightblue']))
    myList[1].aniQueue.put(Movement(-1, -1,step, ['lightblue']))

    step += 1

    #Remove example
    myList[2].aniQueue.put(Movement(-1,-1, step,['delete_shape']))
    myList.pop(2) #Do not remove it from aniList

    step += 1

    print("Finished")

############################################################################################################
#Animation Loop
def start(step=0):
    #Makes sure all objects have made their moves before the next step starts
    allMovesDone = True

    #Iterate through all the objects an check .aniQueue and .moveQueue for Movements
    for aniList in mainAnimationList:
        for aniObject in aniList:
            #Preforms canvas moves after they have been dvided by the delay in the previous loop iteration
            #Also checks for newLines and creates them
            if not aniObject.moveQueue.empty():
                allMovesDone = False
                newCoords = aniObject.moveQueue.get()
                if newCoords.newLine:
                    aniObject.lineToParent = canvas.create_line(newCoords.newLine[0], newCoords.newLine[1], newCoords.newLine[2], newCoords.newLine[3])
                elif newCoords.newObject:
                    if newCoords.newObject[0] == 'oval':
                        aniObject.shape = canvas.create_oval(newCoords.newObject[1],newCoords.newObject[2],newCoords.newObject[1] + newCoords.newObject[3],newCoords.newObject[2] + newCoords.newObject[3],fill=newCoords.newObject[5])
                    elif newCoords.newObject[0] == 'rectangle':
                        aniObject.shape = canvas.create_rectangle(newCoords.newObject[1],newCoords.newObject[2],newCoords.newObject[1] + newCoords.newObject[3],newCoords.newObject[2] + newCoords.newObject[3],fill=newCoords.newObject[5])
                    aniObject.text = canvas.create_text(newCoords.newObject[1]+(newCoords.newObject[3]/2),newCoords.newObject[2]+(newCoords.newObject[3]/2),text=newCoords.newObject[4],font=('Helvetica ' + str(newCoords.newObject[3]//len(newCoords.newObject[4])) + ' bold'))
                elif newCoords.x != -1:
                    canvas.move(aniObject.shape, newCoords.x, newCoords.y)
                    canvas.move(aniObject.text, newCoords.x, newCoords.y)

            #This is the Queue that the algorithm threads add Movment objects too
            elif not aniObject.aniQueue.empty():
                #Only remove from the Queue if on the right step
                if aniObject.aniQueue.queue[0].step <= step:
                    allMovesDone = False
                    newCoords = aniObject.aniQueue.get()

                    #Make sure object has a shape
                    if aniObject.shape:
                        oldCoords = canvas.coords(aniObject.shape)

                    #Check for delete commands in args list
                    #Else then it must me a color change
                    for arg in newCoords.args:
                        if arg == 'delete_line':
                            canvas.delete(aniObject.lineToParent)
                        elif arg == 'delete_shape':
                            canvas.delete(aniObject.shape)
                            canvas.delete(aniObject.text)
                            canvas.delete(aniObject.lineToParent)
                            for i in range(delay-1):
                                    aniObject.moveQueue.put(Movement(-1,-1))
                        else:
                            canvas.itemconfig(aniObject.shape, fill=arg)
                            for i in range(delay-1):
                                    aniObject.moveQueue.put(Movement(-1,-1))

                    #Movement objects on the aniQueue get divided by the delay and added to the moveQueue
                    #-1 in the x value will skip the movement
                    if newCoords.x != -1:
                        movex = newCoords.x - oldCoords[0]
                        movey = newCoords.y - oldCoords[1]
                        movexx = movex / delay
                        moveyy = movey / delay
                        for i in range(delay):
                            aniObject.moveQueue.put(Movement(movexx, moveyy))
                        if movexx * delay != movex:
                            aniObject.moveQueue.put(Movement(movex - (movexx * delay), movey - (moveyy * delay)))

                    #If the newLine list is not empty then add it to the .moveQueue
                    if newCoords.newLine:
                        aniObject.moveQueue.put(Movement(-1,-1,step,[],newCoords.newLine))

                    #If the newQbject list is not empty then generate shape on moveQueue
                    if newCoords.newObject:
                        aniObject.moveQueue.put(Movement(-1,-1,step,[],[],newCoords.newObject))
                        for i in range(delay-1):
                            aniObject.moveQueue.put(Movement(-1,-1))

    #After all objects have been looped through then check to see if any moves were made
    #TODO need functionality to signal when all animations are done and wait instead of spining
    if allMovesDone:
        step+=1

    #This method recursivley calls this start method passing the current step as an argument
    tk.after(1, start, step)
############################################################################################## Program starts here
W, H = 1200, 750
delay = 500
tk = Tk()
canvas = Canvas(tk,width=W,height=H)

canvas.pack()
mainAnimationList = []

#Create a List for the objects to be animated
#Start algorithm thread with created list as argument
mainAnimationList.append([])
mainAnimationList.append([])
t1 = Thread(target = lambda: avl_tree.start_avl_tree(mainAnimationList[0], 0, 0, W, H))
t1.start()

#TODO add more widgets
#Start method contains Animation Loop
startButton = Button(tk, text='Start', width=10, command=start)
startButton.pack()

#Runs the animation in the background
tk.mainloop()

