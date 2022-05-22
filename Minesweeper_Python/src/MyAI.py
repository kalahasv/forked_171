# ==============================CS-199==================================
# FILE:         MyAI.py
#
# AUTHOR:       Justin Chung# ==============================CS-199==================================
# FILE:         MyAI.py
#
# AUTHOR:       Justin Chung
#
# DESCRIPTION:  This file contains the MyAI class. You will implement your
#               agent in this file. You will write the 'getAction' function,
#               the constructor, and any additional helper functions.
#
# NOTES:        - MyAI inherits from the abstract AI class in AI.py.
#
#               - DO NOT MAKE CHANGES TO THIS FILE.
# ==============================CS-199==================================
 
from http.client import FOUND
from re import A
from socket import if_indextoname

from AI import AI
from Action import Action
import numpy as np
import random
import time
 
 
class MyAI( AI ):
 
    def __init__(self, rowDimension, colDimension, totalMines, startX, startY):
 
        self.initalCoords = [startX,startY]
        self.row = rowDimension
        self.col = colDimension
        self.numOfMines = totalMines
        self.numOfFlag = 0 #should be one by the end
        self.numUncoveredtiles = 1
        #self.unTiles = []
        #self.flag = []
 
        ### New Attempt
        # there are 3 type of tiles
 
        ## 1. Uncovered tile
        ## 2. flagged tile
        ## 3. untouched tile
 
        self.label = np.full((rowDimension, colDimension), -1)
        self.elabel = np.full((rowDimension, colDimension), -1)
        self.refLabel = np.full((rowDimension, colDimension), "") # this creates a reference board, an empty string indicates the tile has not been touched yet
        # we can label each tile as a flagged and uncovered

       
        self.amove = Action(AI.Action.UNCOVER, startX, startY) #uncovers the first move tile
        self.refLabel[startX, startY] = 'U'
        
        self.number0 = [] # get the adjacent tiles that are uncovered and with number zero
        self.numer1 = [] # gett the adjacent tiles that are uncovered and with a number 1
        self.time_elapsed = 0.0
 
       
 
       
 
       # no prints this time
 
        ########################################################################
        #                           YOUR CODE ENDS                             #
        ########################################################################
 
       
    def getAction(self, number: int):
 
        #Note: The max time I'm putting rn is arbitrary since idk how much time there really is
        MAX_TIME = 1000
        remaining_time = MAX_TIME - self.time_elapsed
 
        if(remaining_time < 3):
            random_coords = self.chooseRandom()
            #print("hi")
            return Action(AI.Action.UNCOVER, random_coords[0],random_coords[1])
        else:
            #print("Action start!")
            ts = time.time()
        ########################################################################
        #                           YOUR CODE BEGINS                           #
        ########################################################################
       
            #win condition= uncovered all except one tile
            if (self.row * self.col) - self.numOfMines == self.numUncoveredtiles:
                #print('Done')
                return Action(AI.Action.LEAVE)
 
            #check which tiles are uncovered relative to the current position
            #uncovered = [] #tiles uncovered relative to start position
           
            if number >= 0: # if the number is non negative then we work on the board
 
                self.refLabel[self.amove.getX(), self.amove.getY()] = 'U' # u indicates uncovered
                self.label[self.amove.getX(), self.amove.getY()] = number # the number of adjacent bombs
                
                
                if number == 0: # get the coordinates of those tile with zero bombs
                    self.number0.append((self.amove.getX(), self.amove.getY()))
 
                numFlagged, numNoFlagged = self.markedOrUnmarked(self.amove.getX(), self.amove.getY())
 
                # EffectiveLabel(x) = Label(x) – NumMarkedNeighbors(x)
           
                self.elabel[self.amove.getX(), self.amove.getY()] = self.label[self.amove.getX(), self.amove.getY()] - numFlagged
 
               
                   
 
                if self.elabel[self.amove.getX(), self.amove.getY()] == 0: # uncover all unmarked neighbors
                   
                    #print('Uncover all unmarked neighbors')
                   
                    #print(self.elabel[self.amove.getX(), self.amove.getY()])
 
                    result = self.unCoverAll(self.amove.getX(), self.amove.getY(),ts)
                    
                    if result != None:
                        return result
                
                    
                    
                ## Rule of thumb
                if self.elabel[self.amove.getX(), self.amove.getY()] == numNoFlagged: # mark all unmarked neighbors
                   
                    #print('Mark all neighbors')
                   
                    #print(self.elabel[self.amove.getX(), self.amove.getY()])
 
 
                    self.coverAll(self.amove.getX(), self.amove.getY(),ts)
                     
                     
                ## Get get the adjacent tile with no bombs or less likey to be a bomb
                ref_c = [  self.amove.getX(),self.amove.getY()]
                
                
                if not self.elabel[self.amove.getX(), self.amove.getY()] == 0 and not self.elabel[self.amove.getX(), self.amove.getY()] == numNoFlagged:
                    #print(self.elabel[self.amove.getX(), self.amove.getY()])
                    #print(numNoFlagged)
                    print('special case')
                    
                    d = self.specialUncover()
                    #print("D was found to be false")
                    if d == False:
                        #print('minMaxTest')
                        d = self.minMaxTile()
                        #print("min max didn't work, D is still false")
                        if d == False:
                            #print('random case')
                            coordinates = self.chooseRandom()
                            self.refLabel[coordinates[0], coordinates[1]] = 'U'
                            self.amove = Action(AI.Action.UNCOVER, coordinates[0], coordinates[1])
                        

                            self.numUncoveredtiles +=1


                            return self.amove
                        else:
                            return d
                    
 
                    else:
                       
                        return d
                        
                        
                        
                        
                    
                #print('no case hehe')
 
                ## make a random guess
                
                print("random guess")
                coordinates = self.chooseRandom()
                self.refLabel[coordinates[0], coordinates[1]] = 'U'
                self.amove = Action(AI.Action.UNCOVER, coordinates[0], coordinates[1])

                self.numUncoveredtiles +=1
 
                return self.amove
 
               
           
                #print('c')
                #print(self.numUncoveredtiles)
                #print(self.amove.getX(), self.amove.getY())
                #print(self.elabel[self.amove.getX(), self.amove.getY()])
                #print("oh we're leaving now?")
                return Action(AI.Action.LEAVE)
            #else:
                #print("The number is negative and we don't know what to do! Number: ", number)
 
 
           
 
 
 
 
 
 
       
       
       
        ########################################################################
        #                           YOUR CODE ENDS                             #
        ########################################################################
        
    def minMaxTile(self):

        explore = []
        for x in range(0, self.row):
            for y in range(0, self.col):
                if self.refLabel[x, y] == '': # if empty string then we explore
                    explore.append((x, y))
                    
        max_coords = (-1, -1)
        max_value = 10000000000000000
        
        
        # finds the one with the min value of adjacent bombs near it
        #print(explore)
        for x in explore:
            #print("Coordinates going into special check:",x[0]," ",x[1])
            temp = self.specialCheck(x[0], x[1])
            #print("We got through special check")
           # print("temporary value",temp)
            
            if temp < max_value: 
                max_value = temp
                max_coords = (x[0], x[1])
           # print("Max coords",max_coords)
        #print("we got to the value")
        if max_value != 0:
            
            #print(max_value)
            #print(max_coords)
            
            self.refLabel[max_coords[0], max_coords[1]] = 'U'
            self.amove = Action(AI.Action.UNCOVER, max_coords[0], max_coords[1])
            self.numUncoveredtiles +=1
            #print(max_coords[0], max_coords[1])
            return self.amove
        
        else: 
            #print("returning false")
            return False
            
        
        
    def specialCheck(self, x, y):
        num = 0 
        if self.tileinBounds(x - 1, y) and self.refLabel[x - 1, y] != '': 
            num += self.label[x - 1, y]
       # print("First check done")
        if self.tileinBounds(x - 1, y + 1) and self.refLabel[x - 1, y + 1] != '': 
            #print("in bounds")
            num += self.label[x - 1, y + 1]
       # print("Second Check done")
        if self.tileinBounds(x - 1, y - 1) and self.refLabel[x - 1, y - 1] != '': 
            num += self.label[x - 1, y - 1]
        # right
       # print("Third Check done")
        if self.tileinBounds(x + 1, y) and self.refLabel[x + 1, y] != '': 
            num += self.label[x + 1, y]
        #print("Third Check done")
        if self.tileinBounds(x + 1, y - 1) and self.refLabel[x + 1, y - 1] != '': 
            num += self.label[x + 1, y - 1]
            
        if self.tileinBounds(x + 1, y + 1) and self.refLabel[x + 1, y + 1] != '':
       #     print("in bounds")
            num += self.label[x + 1, y + 1]
 
        #top
        if self.tileinBounds(x, y + 1) and self.refLabel[x, y + 1] != '':
        #    print("in bounds")
            num += self.label[x, y+1] 
 
        #bottom
        if self.tileinBounds(x, y - 1) and self.refLabel[x, y - 1] != '': 
            num += self.label[x, y - 1]

       # print("nothing in bounds")
        return num
    
    def specialUncover(self):
        
        
        explore = []
        for x in range(0, self.row):
            for y in range(0, self.col):
                if self.refLabel[x, y] != '': # if empty string then we explore
                    explore.append((x, y))
                  
                  
     
        
        coords = False
        for x in explore:
            #print(x)
            if self.label[x[0], x[1]] == 0:
                
                coords = self.getUntouchedAdjacent(x[0], x[1])
                
                if coords == False:
                   # print('found none')
                    continue
                    
                
                else:
                    #print('found some')
                    break

        
        if coords == False: #exhausted the amount of tiles with zero bombs near it that are yet to be uncovered
             return False
            
        new_coords = coords[0]
        self.refLabel[new_coords[0], new_coords[1]] = 'U'
        self.amove = Action(AI.Action.UNCOVER, new_coords[0], new_coords[1])
        self.numUncoveredtiles +=1
        
        return self.amove
        
    
    def getUntouchedAdjacent(self, x, y):
        temp = []
        #print('check untouched adjacent')
        if self.tileinBounds(x - 1, y) and self.refLabel[x - 1, y] == '':  
            temp.append((x - 1, y)) 
            return temp
        
        if self.tileinBounds(x - 1, y + 1) and self.refLabel[x - 1, y + 1] == '': 
            temp.append((x - 1, y + 1))
            return temp
        
        if self.tileinBounds(x - 1, y - 1) and self.refLabel[x - 1, y - 1] == '': 
            temp.append((x - 1, y - 1))
            return temp
 
        # right
        if self.tileinBounds(x + 1, y) and self.refLabel[x + 1, y] == '': 
            temp.append((x + 1, y))
            return temp
        
        
        if self.tileinBounds(x + 1, y - 1) and self.refLabel[x + 1, y - 1] == '': 
            
            temp.append((x + 1, y - 1))
            return temp
        
        if self.tileinBounds(x + 1, y + 1) and self.refLabel[x + 1, y + 1] == '': 
            temp.append((x + 1, y + 1))
            return temp
 
        #top
        if self.tileinBounds(x, y + 1) and self.refLabel[x, y + 1] == '': 
            temp.append((x, y + 1))
            return temp
        #bottom
        if self.tileinBounds(x, y - 1) and self.refLabel[x, y - 1] == '': 
            temp.append((x, y - 1))
            return temp
        
    
        #print('no adjacent found')
        return False
      
    def updateELabel(self, x, y):
        #left
        if self.tileinBounds(x - 1, y): self.elabel[x - 1, y] -= 1
        if self.tileinBounds(x - 1, y + 1): self.elabel[x - 1, y + 1] -= 1
        if self.tileinBounds(x - 1, y - 1): self.elabel[x - 1, y - 1] -= 1
 
        # right
        if self.tileinBounds(x + 1, y): self.elabel[x + 1, y] -= 1
        if self.tileinBounds(x + 1, y - 1): self.elabel[x + 1, y - 1] -= 1
        if self.tileinBounds(x + 1, y + 1): self.elabel[x + 1, y + 1] -= 1
 
        #top
        if self.tileinBounds(x, y + 1): self.elabel[x, y + 1] -= 1
 
        #bottom
        if self.tileinBounds(x, y - 1): self.elabel[x, y - 1] -= 1
       
        return
    def coverAll(self, x, y, ts):
        # left side
        ## left
        #print("Hi, we're covering stuff now")
        if self.tileinBounds(x - 1, y) and self.refLabel[x - 1, y] == '':  # if coordinates is valid and it is not touched yet
            self.refLabel[x - 1, y] = 'F'
            #print("hi, welcome to the left!")
            self.amove = Action(AI.Action.FLAG, x - 1, y)
 
            #print('printing elabel before')
            #print(self.elabel[x - 1, y])
            self.updateELabel(x - 1, y)
            #print('fin')
           
 
            #time now
            tE = time.time()
            dt = tE-ts
            self.time_elapsed += dt
 
 
            return self.amove
   
        ## top left
        if self.tileinBounds(x - 1, y + 1) and self.refLabel[x - 1, y + 1] == '':  
           
            #print("Hi welcome to the top left!")
            self.refLabel[x - 1, y + 1] = 'F'
            self.amove = Action(AI.Action.FLAG, x - 1, y + 1)
 
            #print('printing elabel before')
            #print(self.elabel[x - 1, y + 1])
            self.updateELabel(x - 1, y + 1)
            #print('fin')
 
 
            tE = time.time()
            dt = tE-ts
            self.time_elapsed += dt
 
            return self.amove
       
        ## bottom left
        if self.tileinBounds(x - 1, y - 1) and self.refLabel[x - 1, y - 1] == '':
           
            #print("hi welcome to the bottom left")
            self.refLabel[x - 1, y  - 1] = 'F'
            self.amove = Action(AI.Action.FLAG, x - 1, y - 1)
 
 
            #print('printing elabel before')
            #print(self.elabel[x - 1, y - 1])
            self.updateELabel(x - 1, y - 1)
            #print('fin')
 
            tE = time.time()
            dt = tE-ts
            self.time_elapsed += dt
 
            return self.amove
       
 
        # right side
 
 
        ## right
        if self.tileinBounds(x + 1, y) and self.refLabel[x + 1, y] == '':  
           
           
            #print("hi welcome to the right!")
            self.refLabel[x + 1, y] = 'F'
            self.amove = Action(AI.Action.FLAG, x + 1, y)
 
            #print('printing elabel before')
            #print(self.elabel[x + 1, y])
            self.updateELabel(x + 1, y)
            #print('fin')
 
            tE = time.time()
            dt = tE-ts
            self.time_elapsed += dt
 
            return self.amove
       
        ## top right
        if self.tileinBounds(x + 1, y + 1)  and self.refLabel[x + 1, y + 1] == '':  
           
            #print("hi welcome to the top right")
 
            self.refLabel[x + 1, y + 1] = 'F'
            self.amove = Action(AI.Action.FLAG, x + 1, y + 1)
 
            #print('printing elabel before')
            #print(self.elabel[x + 1, y + 1])
            self.updateELabel(x + 1, y + 1)
            #print('fin')
 
            tE = time.time()
            dt = tE-ts
            self.time_elapsed += dt
 
            return self.amove
       
        ## bottom right
        if self.tileinBounds(x + 1, y - 1) and self.refLabel[x + 1, y - 1] == '':
 
            #print("hi welcome to the bottom right")
            self.refLabel[x + 1, y - 1] = 'F'
            self.amove = Action(AI.Action.FLAG, x + 1, y - 1)
 
            #print('printing elabel before')
            #print(self.elabel[x + 1, y - 1])
            self.updateELabel(x + 1, y - 1)
            #print('fin')
 
 
            tE = time.time()
            dt = tE - ts
            self.time_elapsed += dt
 
            return self.amove
       
 
        #top
        if self.tileinBounds(x, y + 1) and self.refLabel[x, y + 1] == '':
           
            #print("hi welcome to top")
            self.refLabel[x, y + 1] = 'F'
            self.amove = Action(AI.Action.FLAG, x, y + 1)
 
            #print('printing elabel before')
            #print(self.elabel[x, y + 1])
            self.updateELabel(x, y + 1)
            #print('fin')
 
            tE = time.time()
            dt = tE-ts
            self.time_elapsed += dt
 
            return self.amove
 
        #bottom
        if self.tileinBounds(x, y - 1) and self.refLabel[x, y - 1] == '':  
           
            #print("hi welcome bottom")
            self.refLabel[x, y - 1] = 'F'
 
            self.amove = Action(AI.Action.FLAG, x, y - 1)
 
 
            #print('printing elabel before')
            #print(self.elabel[x, y - 1])
            self.updateELabel(x, y - 1)
            #print('fin')
 
            tE = time.time()
            dt = tE - ts
            self.time_elapsed += dt
 
            return self.amove
 
    def unCoverAll(self, x, y,ts):
       
        #print('we at uncover now')
        # left side
        ## left
 
        #print("Checking left condition")
        if self.tileinBounds(x - 1, y) and self.refLabel[x - 1, y] == '':  # if coordinates is valid and it is not touched yet
            #print("hi, welcome to the left!")
 
            self.refLabel[x - 1, y] = 'U'
           
 
            self.amove = Action(AI.Action.UNCOVER, x - 1, y)
            self.numUncoveredtiles +=1
           
           
           
 
            #time now
            tE = time.time()
            dt = tE-ts
            self.time_elapsed += dt
 
 
            return self.amove
   
        #print("Checking top left condition")
        ## top left
        if self.tileinBounds(x - 1, y + 1) and self.refLabel[x - 1, y + 1] == '':  
           
            #print("Hi welcome to the top left!")
            self.refLabel[x - 1, y + 1] = 'U'
            self.amove = Action(AI.Action.UNCOVER, x - 1, y + 1)
            self.numUncoveredtiles +=1
 
           
 
 
            tE = time.time()
            dt = tE-ts
            self.time_elapsed += dt
 
            return self.amove
       
        #print("Checking bottom left condition")
        ## bottom left
        if self.tileinBounds(x - 1, y - 1) and self.refLabel[x - 1, y - 1] == '':
           
            #print("hi welcome to the bottom left")
            self.refLabel[x - 1, y  - 1] = 'U'
            self.amove = Action(AI.Action.UNCOVER, x - 1, y - 1)
            self.numUncoveredtiles +=1
 
 
            tE = time.time()
            dt = tE-ts
            self.time_elapsed += dt
 
            return self.amove
       
 
        # right side
 
 
        ## right
        #print("Checking right condition")
        if self.tileinBounds(x + 1, y) and self.refLabel[x + 1, y] == '':  
           
           
            #print("hi welcome to the right!")
            self.refLabel[x + 1, y] = 'U'
            self.amove = Action(AI.Action.UNCOVER, x + 1, y)
            self.numUncoveredtiles +=1
 
           
 
            tE = time.time()
            dt = tE-ts
            self.time_elapsed += dt
 
            return self.amove
       
        ## top right
        #print("Checking top right condition")
        if self.tileinBounds(x + 1, y + 1)  and self.refLabel[x + 1, y + 1] == '':  
           
            #print("hi welcome to the top right")
 
            self.refLabel[x + 1, y + 1] = 'U'
            self.amove = Action(AI.Action.UNCOVER, x + 1, y + 1)
            self.numUncoveredtiles +=1
 
           
 
            tE = time.time()
            dt = tE-ts
            self.time_elapsed += dt
 
            return self.amove
       
        ## bottom right
        #print("Checking bottom right condition")
        if self.tileinBounds(x + 1, y - 1) and self.refLabel[x + 1, y - 1] == '':
 
            #print("hi welcome to the bottom right")
            self.refLabel[x + 1, y - 1] = 'U'
            self.amove = Action(AI.Action.UNCOVER, x + 1, y - 1)
            self.numUncoveredtiles +=1
 
 
 
            tE = time.time()
            dt = tE - ts
            self.time_elapsed += dt
 
            return self.amove
       
 
        #top
        #print("Checking top condition")
        if self.tileinBounds(x, y + 1) and self.refLabel[x, y + 1] == '':
           
            #print("hi welcome to top")
            self.refLabel[x, y + 1] = 'U'
            self.amove = Action(AI.Action.UNCOVER, x, y + 1)
            self.numUncoveredtiles +=1
 
           
 
            tE = time.time()
            dt = tE-ts
            self.time_elapsed += dt
 
            return self.amove
 
        #bottom
        #print("Checking bottom  condition")
        if self.tileinBounds(x, y - 1) and self.refLabel[x, y - 1] == '':  
           
            #print("hi welcome bottom")
            self.refLabel[x, y - 1] = 'U'
 
            self.amove = Action(AI.Action.UNCOVER, x, y - 1)
            self.numUncoveredtiles +=1
 
 
           
 
            tE = time.time()
            dt = tE - ts
            self.time_elapsed += dt
 
            return self.amove
        #print("None of the conditions were satisfied")
    def markedOrUnmarked(self, x, y):
        i = 0 # marked with a flag
        j = 0 # not marked with a flag
        # left side
        ## left
 
 
        if self.tileinBounds(x - 1, y) and self.refLabel[x - 1, y] == 'F': # if valid move and flagged and not touched yet
            i +=1
       
        if self.tileinBounds(x - 1, y) and self.refLabel[x - 1, y] == '': # if valid move and not touched yet
            j +=1
 
 
        ## top left
        if self.tileinBounds(x - 1, y + 1) and self.refLabel[x - 1, y + 1] == 'F':
            i +=1
       
        if self.tileinBounds(x - 1, y + 1) and self.refLabel[x - 1, y + 1] == '':
            j +=1
 
 
        ## bottom left
        if self.tileinBounds(x - 1, y - 1) and self.refLabel[x - 1, y - 1] == 'F':
            i +=1
 
        if self.tileinBounds(x - 1, y - 1) and self.refLabel[x - 1, y - 1] == '':
            j +=1
 
        # right side
 
        ## right
        if self.tileinBounds(x + 1, y) and self.refLabel[x + 1, y] == 'F':
            i +=1
        if self.tileinBounds(x + 1, y) and self.refLabel[x + 1, y] == '':
            j +=1
       
        ## top right
        if self.tileinBounds(x + 1, y + 1) and self.refLabel[x + 1, y + 1] == 'F':
            i +=1
        if self.tileinBounds(x + 1, y + 1) and self.refLabel[x + 1, y + 1] == '':
            j +=1
 
        ## bottom right
        if self.tileinBounds(x + 1, y - 1) and self.refLabel[x + 1, y - 1] == 'F':
            i +=1
        if self.tileinBounds(x + 1, y - 1) and self.refLabel[x + 1, y - 1] == '':
            j +=1
 
 
        #top
        if self.tileinBounds(x, y + 1) and self.refLabel[x, y + 1] == 'F':
            i +=1
 
        if self.tileinBounds(x, y + 1) and self.refLabel[x, y + 1] == '':
            j +=1
 
        #bottom
        if self.tileinBounds(x, y - 1) and self.refLabel[x, y - 1] == 'F':
            i +=1
 
        if self.tileinBounds(x, y - 1) and self.refLabel[x, y - 1] == '':
            j +=1
 
        return i, j
 
    #check if tile is in Bounds or not
    def tileinBounds(self, x, y):
        if (x >= 0 and x < self.row) and (y >= 0 and y < self.col) :
            return True
        else:
            #print("Tile is in bounds")
            return False

    def chooseRandom(self):
       
       
 
        explore = []
        for x in range(0, self.row):
            for y in range(0, self.col):
                if self.refLabel[x, y] == '': # if empty string then we explore
                    explore.append((x, y))
 
        coords = random.choice(explore)
 
       
       
       
       
       
        return coords
        #self.action = Action(AI.Action.UNCOVER, randx, randy)
 
#
# DESCRIPTION:  This file contains the MyAI class. You will implement your
#               agent in this file. You will write the 'getAction' function,
#               the constructor, and any additional helper functions.
#
# NOTES:        - MyAI inherits from the abstract AI class in AI.py.
#
#               - DO NOT MAKE CHANGES TO THIS FILE.
# ==============================CS-199==================================
 
