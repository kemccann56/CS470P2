from tkinter import *
from queue import Queue
from threading import Thread, Lock
from animation import *

def create(aniList, length, width):
    orginx = width//2
    orginy = 0

    size1 = 50
    size2 = 30

    step = 0

    #Create your data structure #AVLtree, RBtree, etc
    myList = []

    aniList.append(Object(0))
    myList.append(aniList[-1])

    #first layer
    myList[0].aniQueue.put(Movement(-1,-1,step,[],[],['trueRectangle',orginx-size2,orginy+50, size2,str(myList[0].userNum),'lightblue']))
    myList[0].aniQueue.put(Movement(-1,-1,step,[],[],['trueRectangle',orginx-size2,orginy+50, size2,str(myList[0].userNum),'lightblue']))


    #second layer

    #third layer




    print("Finished")
    
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
                    elif newCoords.newObject[0] == 'trueRectangle':
                        aniObject.shape = canvas.create_rectangle(newCoords.newObject[1],newCoords.newObject[2],newCoords.newObject[1] + newCoords.newObject[3]/2,newCoords.newObject[2] + newCoords.newObject[3],fill=newCoords.newObject[5])
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
                    textChange = 0
                    for arg in newCoords.args:
                        if textChange:
                            canvas.itemconfig(aniObject.text, text=arg)
                            textChange = 0
                        elif arg == 'delete_line':
                            canvas.delete(aniObject.lineToParent)
                        elif arg == 'delete_shape':
                            canvas.delete(aniObject.shape)
                            canvas.delete(aniObject.text)
                            canvas.delete(aniObject.lineToParent)
                            for i in range(delay-1):
                                    aniObject.moveQueue.put(Movement(-1,-1))
                        elif arg == 'change_text':
                            textChange = 1
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

W, H = 1200, 500
delay = 500
tk = Tk()
canvas = Canvas(tk,width=W,height=H)
canvas.pack()
mainAnimationList = []

#Create a List for the objects to be animated
#Start algorithm thread with created list as argument
mainAnimationList.append([])
mainAnimationList.append([])

t1 = Thread(target = lambda: create(mainAnimationList[0], H, W))
t1.start()

#TODO add more widgets
#Start method contains Animation Loop
startButton = Button(tk, text='Start', width=10, command=start)
startButton.pack()

#Runs the animation in the background
tk.mainloop()