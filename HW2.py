from tkinter import *
from queue import Queue
from threading import Thread, Lock
from turtle import Screen
from animation import *
from avl_tree import start_avl_tree
from rbtreeA import *
from veb_tree import start_veb
import time

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
def settingOrginExample(aniList, x=0, y=0):
    orginx = x
    orginy = y

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
    myList[3].aniQueue.put(Movement(-1,-1,step,[],[myList[3].x + size/2, myList[3].y, myList[1].x + size/2, myList[1].y + size],['trueRectangle',orginx+125,orginy+300,size,str(myList[3].userNum),'lightblue']))

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
    myList[0].aniQueue.put(Movement(-1,-1,step,['change_text','test']))

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
def startAnimation(step=0, delay=100, movePreformed=1, stepFlag=1):
    #Makes sure all objects have made their moves before the next step starts
    allMovesDone = True

    #Iterate through all the objects an check .aniQueue and .moveQueue for Movements
    for aniList in mainAnimationList:
        if stepFlag:
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
        if stepVar.get():
            stepFlag = 0
            #Waits for StepOnce button - spins otherwise
            if not stepQueue.empty():
                stepFlag = stepQueue.get()
                step+=1
                if movePreformed >= 5:
                    movePreformed = -1
                else:
                    movePreformed += 1
        else:
            step+=1
            if movePreformed >= 5:
                movePreformed = -1
            else:
                movePreformed += 1
    else:
        movePreformed = 1


    #This method recursivley calls this start method passing the current step as an argument
    if movePreformed != -1:
        tk.after(1, startAnimation, step, delay, movePreformed, stepFlag)

def startThreads():
    canvas.delete('all')
    mainAnimationList.clear()

    #Create a List for the objects to be animated
    #Start algorithm thread with created list as argument
    mainAnimationList.append([])
    mainAnimationList.append([])

    if AVL1.get():
        t1 = Thread(target = lambda: start_avl_tree(mainAnimationList[0], 0, 0, screen_width, screen_height/7, commandQueue1))
    elif VEB1.get():
        #TODO add VEB Tree
        t1 = Thread(target = settingOrginExample, args =(mainAnimationList[0], ))
    elif RBT1.get():
        #TODO add RB Tree
        t1 = Thread(target = lambda: RBTree.rbTree(mainAnimationList[0], screen_width/2, 10, commandQueue1))
    else:
        t1 = Thread(target = settingOrginExample, args =(mainAnimationList[0], ))

    if AVL2.get():
        t2 = Thread(target = lambda: start_avl_tree(mainAnimationList[1], 0, screen_height/2, screen_width, screen_height/7, commandQueue2))
    elif VEB2.get():
        #TODO add VEB Tree
        t2 = Thread(target = settingOrginExample, args =(mainAnimationList[1], screen_height/2, screen_height/3))
    elif RBT2.get():
        #TODO add RB Tree
        t2 = Thread(target = lambda: RBTree.rbTree(mainAnimationList[0], screen_width/2, screen_height/2, commandQueue2))
    else:
        t2 = Thread(target = settingOrginExample, args =(mainAnimationList[1], 0, screen_height/3))

    t1.start()
    t2.start()

    tk.after(1000, startAnimation, 0, delayScale.get())

def settingsWindow():
    window = Toplevel()
    window.geometry('500x300')

    newlabel = Label(window, text = "Settings Window")
    newlabel.pack(padx=5, pady=5)


    label1 = Label(window,text = "Tree 1")
    label1.pack(pady=10)

    ChkBttn = Checkbutton(window, width = 15, text='AVL                       ', variable = AVL1)
    ChkBttn.pack()

    ChkBttn2 = Checkbutton(window, width = 15, text='VAN_EMDE_BOAS', variable = VEB1)
    ChkBttn2.pack()

    ChkBttn3 = Checkbutton(window, width = 15, text='RED_BLACK           ', variable = RBT1)
    ChkBttn3.pack()


    label2 = Label(window,text = "Tree 2")
    label2.pack(pady=10)

    ChkBttn4 = Checkbutton(window, width = 15, text='AVL                       ', variable = AVL2)
    ChkBttn4.pack()

    ChkBttn5 = Checkbutton(window, width = 15, text='VAN_EMDE_BOAS', variable = VEB2)
    ChkBttn5.pack()

    ChkBttn6 = Checkbutton(window, width = 15, text='RED_BLACK           ', variable = RBT2)
    ChkBttn6.pack()

def stepOnce():
    stepQueue.put(1)

#Command methods start step back at 0
def insertCommand():
    commandQueue1.put(['insert',insertEntry.get()])
    commandQueue2.put(['insert',insertEntry.get()])
    startAnimation(0, delayScale.get())

def deleteCommand():
    commandQueue1.put(['delete',deleteEntry.get()])
    commandQueue2.put(['delete',deleteEntry.get()])
    startAnimation(0, delayScale.get())

def searchCommand():
    commandQueue1.put(['search',searchEntry.get()])
    commandQueue2.put(['search',searchEntry.get()])
    startAnimation(0, delayScale.get())

############################################################################################## Program starts here
tk = Tk()
screen_width = tk.winfo_screenwidth()
screen_height = tk.winfo_screenheight()
canvas = Canvas(tk,width=screen_width * 0.98,height=screen_height * 0.85)
canvas.grid(row=0, column=0, columnspan=51)

mainAnimationList = []
commandQueue1 = Queue()
commandQueue2 = Queue()

AVL1 = IntVar()
VEB1 = IntVar()
RBT1 = IntVar()
AVL2 = IntVar()
VEB2 = IntVar()
RBT2 = IntVar()
stepVar = IntVar()

#settingsWindow
settingsButton = Button(tk, text='Settings', width=10, command=settingsWindow)
settingsButton.grid(row=1, column=0)

#Start method contains Animation Loop
startButton = Button(tk, text='Start', width=10, command=startThreads)
startButton.grid(row=1, column=6)

#stepMode
stepQueue = Queue()
stepBttn = Checkbutton(tk, width = 8, text='StepMode', variable = stepVar)
stepBttn.grid(row=1, column=7)
stepButton = Button(tk, text='StepOnce', width=10, command=stepOnce)
stepButton.grid(row=1, column=8)

#Insert Command
insertButton = Button(tk, text='Insert', width=10, command=insertCommand)
insertButton.grid(row=1, column=14)
insertEntry = Entry(tk, width = 5)
insertEntry.grid(row=1, column=15)

#Delete Command
deleteButton = Button(tk, text='Delete', width=10, command=deleteCommand)
deleteButton.grid(row=1, column=21)
deleteEntry = Entry(tk, width = 5)
deleteEntry.grid(row=1, column=22)

#Insert Command
searchButton = Button(tk, text='Search', width=10, command=searchCommand)
searchButton.grid(row=1, column=28)
searchEntry = Entry(tk, width = 5)
searchEntry.grid(row=1, column=29)

#Dealy Scale
delayScale = Scale(tk, from_=1, to=5000, orient=HORIZONTAL)
delayScale.grid(row=1, column=50)
delayLabel = Label(tk, text='Delay:')
delayLabel.grid(row=1, column=49)


#Runs the animation in the background
tk.mainloop()
