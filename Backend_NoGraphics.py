from random import random
from math import *
import numpy as np
from LoadLevel import *
import Graphic_Classes as gc

#bounds of array (in pixels, relative to the ball)
#currently, creates a window from 100 pix below and to the left
#to 300 pix above and to the right of the ball
screenMaxX = 300
screenMaxY = 350
screenMinX = -100
screenMinY = -50

#speed at which the map moves
#currently set at 5 pix/frame
#for reference, each square on the map is 20 pix
#negative is to the left
v_screen = -5

#speed at which the ball jumps vertically (in pix/frame)
#upward is positive
v_jump = 10

#acceleration of ball in midair (in pix/frame^2)
#positive is downward
accel = 1

kept = 5                #number of top trials to pass to next generation

jumps = []              #the list of locations for jumps

#this will store a list of 'jumps' and their corresponding final positions
jumpsList = []
for i in range(kept):
    jumpsList.append([jumps.copy(),0])
    
#retrieves the level
#list_blocks stores a list of block-coordinates as [x-coordinate, y=coordinate]
#list_spikes and list_orbs do the same for spikes and orbs, respectively
#length stores the pixel length 
list_blocks,list_spikes,list_orbs,length = getLevel()

#stores whether the level has been beaten yet
win = False

#stores the final distance (in pix) the ball reaches in each trial
finalPosition = 0

#This class is the object for the ball (the player), including how to 
#initialize it and how to move it on the screen
class Ball():
    
    #initializes the ball at an input position (pix) on the screen
    #and speed (pix/frame). For the code to work correctly, dx should be 0
    def __init__(self,x_init,y_init,dx,dy):
        self.goto(x_init,y_init)            #places ball's turtle at input coordinates
        self.dx = dx                        #x-velocity (pix/frame), should be 0
        self.dy = dy                        #y-velocity (pix/frame)
        self.onfloor = True                 #stores whether the ball is on a block
        self.position = 0                   #stores how far the ball has traveled
    
    #places ball's turtle at coordinates (x,y) on the screen
    def goto(self,x,y):
        self.x = x
        self.y = y

    #updates the ball's position based off of its velocity,
    #and changes its y-velocity based on acceleration
    def move(self):
        newx = self.x + self.dx
        newy = self.y + self.dy
        
        #makes sure ball doesnt go into floor
        if self.onfloor:
            self.dy = 0
        else:
            self.dy -= accel

        self.goto(newx,newy)

#This class encodes map objects (blocks, spikes, and orbs)
class Object():
    #initializes object at input coordinates and x-velocity (should be v_screen)
    #y-velocity will be 0
    def __init__(self,x_init,y_init,dx):
        self.dx = dx
        self.goto(x_init,y_init)
        
    def goto(self,x,y):
        self.x = x
        self.y = y
        
    #moves (to the left) without acceleration
    def move(self):
        newx = self.x + self.dx
        newy = self.y

        self.goto(newx,newy)
    
#These objects encode the spikes, blocks, and orbs.
#Currently, they are identical to object, so the pass keyword is inserted
class Spike(Object):
    pass 
        
class Block(Object):
    pass
        
class Orb(Object):
    pass

#This class will run the actual game.
class JumpingBallApplication():
    
    def __init__(self,list_blocks,list_spikes,list_orbs):
        self.done = False               #true if has won/died
        self.position = 0               #x-distance of ball
        global jumps
        #will store the locations in jumps that ball actually jumps at
        self.usedJumps = []             
        #brings in list of coordinates of obstacles as attributes
        self.list_blocks = list_blocks
        self.list_spikes = list_spikes
        self.list_orbs = list_orbs
        self.buildWindow()              #begins the program
    
    #marks the class as done
    def over(self):
        self.done = True

    def buildWindow(self):
        
        #creates ball at the origin and at rest
        x_init = 0
        y_init = 0
        dx = 0
        dy = 0
        ball = Ball(x_init,y_init,dx,dy)
        
        #stores list of Block objects
        blockList = []
        for coord in list_blocks:
            block = Block(coord[0],coord[1],v_screen)
            blockList.append(block)
        
        #stores list of Spike objects
        spikeList = []
        for coord in list_spikes:
            spike = Spike(coord[0],coord[1],v_screen)
            spikeList.append(spike)
        
        #stores list of Orb objects
        orbList = []
        for coord in list_orbs:
            orb = Orb(coord[0],coord[1],v_screen)
            orbList.append(orb)
        
        #stores a final block which will be where the map ends
        lastblock = Block(length,0,v_screen)


        #if the game has been won, quits the game
        def winHandler():
            if (lastblock.x < 10):
                global win
                win = True
                quitHandler();
        
        #if the game has been lost, quits the game
        def deathHandler():
            global win
            #determines if ball has run into a spike
            spike_box = 15                          #spike hitbox
            for spike in spikeList:
                cond = abs(spike.x-ball.x) < spike_box \
                and abs(spike.y-ball.y) < spike_box
                if cond:
                    win = False
                    quitHandler()
            #determines if ball has run into a block
            block_box = 20                          #block hitbox
            for block in blockList:
                cond = abs(block.x-ball.x) < block_box \
                and abs(block.y-ball.y) < block_box
                if cond:
                    win = False
                    quitHandler()
    
        #quits the program and sets finalPosition to the ball's last position
        def quitHandler():
            self.over()
            global finalPosition
            finalPosition = ball.position
        
        #if the ball is not moving up and is close to a block, 
        #snaps ball location to top of block so that the ball 
        #doesn't go into the block. Then identifies the ball as
        #on the block (so that it can jump)
        def landHandler():
            block_box = 20                          #block hitbox
            ball.onfloor = False
            if (ball.dy <= 0):
                for block in blockList:
                    if abs(block.x-ball.x) < block_box:
                        dely = ball.y-block.y
                        if dely <= block_box - ball.dy and dely >= block_box:
                            ball.dy = block.y-ball.y+block_box
                            ball.onfloor = True
                            break
        
        #If the ball is supposed to jump and can jump (is on top 
        #of a block or on an orb), then jumps by setting y-velocity
        #to v_jump. Then marks ball as not on floor if jumped off 
        #of a block.
        def jumpHandler():
            if (ball.position in jumps):
                orb_box = 20                #orb hitbox
                lol = False                 #stores whether the ball can jump
                if ball.onfloor:
                    lol = True
                    ball.onfloor = False
                    ball.dy = v_jump;
                for orb in orbList:
                    if (abs(orb.x-ball.x) < orb_box \
                        and abs(orb.y-ball.y) < orb_box):
                        lol = True
                        ball.dy = v_jump
                        break
                if lol:
                    self.usedJumps.append(ball.position)
                    
        #animates the actions recursively by moving the ball,
        #checking checking for win or death, then moving the
        #map.
        def animate():
            if not self.done:
                ball.position -= v_screen
                landHandler()
                jumpHandler()
                ball.move()
                winHandler()
                if not win:
                    deathHandler()
                for spike in spikeList:
                    spike.move()
                for block in blockList:
                    block.move()
                for orb in orbList:
                    orb.move()
                lastblock.move()
                animate()
    
        #initiates the animation loop
        animate()

maxPosition = 0                 #maximum position a run as reached
prevJumps = jumps.copy()        #will store a pre-mutation jumps copy

gen = 0                         #number of generations that have been run

#)th generation: seeds jumpsList with the null scenario with no jumps
print("Null case")
jumpingBallApp = JumpingBallApplication(list_blocks,list_spikes,list_orbs)
jumpsList[0][1] = finalPosition

gensList = []                   #will store the jumpsLists of each generation

#runs a new generation when the current generation fails to beat the level
while (not win):
    newJumpsList = jumpsList.copy()         #will store top trials in gen
    #iterates through jumps in jumpsLists and runs mutated trials
    for item in jumpsList:
        #This block determines how far back mutations can go compared to
        #prior maximum position reached. Default is at 300 pix.
        var_area = 300
        if (len(item[0]) > 0):
            #if last jump was far enough, increases var_area accordingly
            var_area = max(var_area,1.3*(item[1]-item[0][-1]))
        
        trials = 15                         #trials per parent per generation
        prevJumps = item[0].copy()          #makes copy of parent to be mutated
        for i in range(trials):
            jumps = prevJumps.copy()          #sets jumps to the parent
            
            #Mutation block: Picks a random spot within var_area in front of 
            #final position of parent trial. To add a jump
            if (item[1] > var_area):
                x = item[1] - v_screen*int(var_area/v_screen*random())
            else:
                x = v_screen*int(item[1]/v_screen*random())
            #replacement: has a 21% chance of replacing the last jump
            #in the parent's jumps with the new jump location, and a 
            #9% chance of replacing the last two jumps.
            chance = 0.3
            if (len(item[0]) > 1):
                if (random() < chance):
                    del jumps[-1]
                    if (len(item[0]) > 2):
                        if (random() < chance):
                            del jumps[-1] 
            jumps.append(x)
            
            #If the child jumps being considered is in the parent generation's
            #jumpsList or the current jumpsList, then don't run.
            cont = True                 #whether the trial should be run
            for thing in jumpsList:
                if thing[0] == jumps:
                    cont = False
                    break
            for thing in newJumpsList:
                if thing[0] == jumps:
                    cont = False
                    break
            #if the trial shouldn't be run, then skips to end of code in loop
            if not cont:
                continue
            
            #runs the trial (with the mutated jumps)
            #finalPosition is set to the max distance the ball reaches
            jumpingBallApp = JumpingBallApplication(list_blocks,list_spikes,list_orbs)
            
            #sets jumps to the values that were actually used to avoid
            #long, redundant jump lists.
            jumps = jumpingBallApp.usedJumps.copy()
            
            #updates newJumpsList with trials that traveled further
            #than other trials in jumpsList (favors previous item if 
            #distance is equal)
            for i in range(kept):
                cond = True         #if no other trial has traveled same distance
                for k in range(i):
                    if finalPosition == newJumpsList[k][1]:
                        cond = False
                #if trial has traveled further than old trial
                cond2 = finalPosition > newJumpsList[i][1]
                #replacement trial bumps down lower trials
                if cond2 and cond:
                    for j in range(kept-1,i,-1):
                        newJumpsList[j] = newJumpsList[j-1].copy()
                    newJumpsList[i][0] = jumps.copy()
                    newJumpsList[i][1] = finalPosition
                    break
                
            if win:
                break
    
    #prints the top trials of each generation
    jumpsList = newJumpsList.copy()
    gen += 1
    print("Here's are the",kept,"best trials in generation", gen, ": ")
    for i in range(kept):
        print((i+1),":",jumpsList[i][1],"pix,",jumpsList[i][1]*100/length,"%")
        print(jumpsList[i][0])
    
    if win:
        continue
    
    #Handles premature convergence for memory sections.
    #Has a 40% chance of deleting the last jump of the nth place trial 
    #if it matches the previous generation's nth place trial in distance
    for i in range(kept):
        #if 1 gen back had the same jumps, delete last jump
        if random() < 0.4:
            for n in range(1,0,-1):
                if gen >= 2*n and len(jumpsList[i][0]) >= n:
                    #checks if the final distance matches with previous generation's
                    cond = jumpsList[i][1] == gensList[gen-2*n][i][1]
                    if cond:
                        #removes last jump
                        for k in range(n):
                            del jumpsList[i][0][-1]
                        #Reruns trial to find its corresponding final position
                        jumps = jumpsList[i][0].copy()
                        jumpingBallApp = JumpingBallApplication(list_blocks,list_spikes,list_orbs)
                        jumpsList[i][1] = finalPosition
                        break
         
    #Runs the best trial (with graphics) every {frequency} generations
    frequency = 10
    if (gen % frequency == 0):
        gc.jumps = jumpsList[0][0]
        root = gc.tkinter.Tk()
        showApp = gc.JumpingBallApplication(root)
        showApp.mainloop()
    
    #store current jumpsList as the final value of this generation     
    gensList.append(jumpsList.copy())

#pauses the program until user input, and then prints the jumpsList and
#ends the program        
value = input("Press enter to show the winning trial: ")
print("Here's the winning trial: ")
print(jumpsList[0][0])

print("Training Completed.")
