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
#``
# NOTES:        - MyAI inherits from the abstract AI class in AI.py.
#
#               - DO NOT MAKE CHANGES TO THIS FILE.
# ==============================CS-199==================================


#The way the array palces things -> [ row, column ]
#The way traditional coordinates work ---> [ row, column ]  (5th row, 2nd column)
# The way their startX --> corresonds to column 
#Start Y corresponds to row 
 
from http.client import FOUND
from re import A
from socket import if_indextoname

from AI import AI
from Action import Action
import numpy as np
import random
import time
 
 
class MyAI( AI ):
  #startX -> 
  #X-> corresponds to the column
  #Y needs to be row 
    def __init__(self, rowDimension, colDimension, totalMines, startX, startY):
        #print('start')
        
        #column, row 
        #print("Intial Coordinates:",startY," ", startX)

        self.initalCoords = [startY, startX]
        self.row = rowDimension
        self.col = colDimension
        self.numOfMines = totalMines
        self.numOfFlag = 0 #should be one by the end
        self.numUncoveredtiles = 1
        self.debugMoves = []
        #self.unTiles = []
        #self.flag = []
 
        ### New Attempt
        # there are 3 type of tiles
 
        ## 1. Uncovered tile
        ## 2. flagged tile
        ## 3. untouched tile

        
        self.label = np.full((rowDimension, colDimension), -1)
        self.elabel = np.full((rowDimension, colDimension), -1)
        self.refLabel = np.full((rowDimension, colDimension), '') # this creates a reference board, an empty string indicates the tile has not been touched yet
        #print("Row:",colDimension," Column:",rowDimension)
        # we can label each tile as a flagged and uncovered
    
        #print('doing an action')
        #Actual board -> row, column 
        self.amove = Action(AI.Action.UNCOVER, startX, startY) #uncovers the first move tile

    
        #print('first ref label')
        #print("Coords:",startY," ",startX)
        self.refLabel[startY, startX] = 'U'
        
        self.moves = [] # list all actions to do
        self.frontier_covered = [] # list of all covered frontiers
        self.actionMoves = []


        self.actionMoves.append([1, startY, startX])
        self.frontier_covered.append((startY, startX)) # list of values that can have adjacent nodes to be explored
        self.frontier_uncovered = set() # set of values that should not be explored
        self.solvable = False
        self.p = 0 # probability of a mine 
        self.n = 0
        self.time_elapsed = 0.0

       
 
       
 
       # no prints this time
 
        ########################################################################
        #                           YOUR CODE ENDS                             #
        ########################################################################
 
       
    def getAction(self, number: int):
        #print("New action starting!")
        #Note: The max time I'm putting rn is arbitrary since idk how much time there really is
        MAX_TIME = 1000
        remaining_time = MAX_TIME - self.time_elapsed
 
        if(remaining_time < 3):
            #print('too long guess')
            random_coords = self.chooseRandom()
            #print("hi")
            
        
        else:
            #print("Action start!")
            ts = time.time()
        ########################################################################
        #                           YOUR CODE BEGINS                           #
        ########################################################################
       
            #win condition= uncovered all except one tile
            

            #print('start now')
            self.numTiles()

            
            if (self.row * self.col) - self.numOfMines == self.numUncoveredtiles:
                #print('Done')
                return Action(AI.Action.LEAVE)

            #check which tiles are uncovered relative to the current position
            #uncovered = [] #tiles uncovered relative to start position
           
            if number != -1: # if the number is non negative then we work on the board
                #getX -> row
                #getY -> column 
                #print("Get Coordinates",self.amove.getX(), self.amove.getY())

                #print("Refence board dimensions:",len(self.refLabel),len(self.refLabel[0]))
                #self. refLabel board -> 0-29 
                self.refLabel[ self.amove.getY(), self.amove.getX()] = 'U' # u indicates uncovered

                #print("Ref label is the issue")
                
                self.label[ self.amove.getY(), self.amove.getX()] = number # the number of adjacent bombs
                #print("Label is correct")
                #print(self.refLabel)


            #print('scan')
            self.scan() # find a move

            #print('finish scanning')                                                                                                                                  
            #print('number of uncovered')
            #print(self.numUncoveredtiles)

            #print(self.actionMoves)
            if len(self.actionMoves) == 0:
                #print('find_moves')
                self.find_moves() # get some moves

                #print('out of finding moves')
                if len(self.actionMoves) == 0:   
                    
                    #print('cannot find any')
                    return Action(AI.Action.LEAVE)
                
            if len(self.actionMoves) == 0 and len(self.frontier_uncovered) == 1:
                #print('simple prob')
                self.getSimpleProb()
                t = self.applyOpeningProb
                
                
                    
            
                    
            #print('poppping')
            
            #non_dupes = []
            #[non_dupes.append(x) for x in self.moves if x not in non_dupes]
            #non_dupes_debug = []
            #[non_dupes_debug.append(x) for x in self.debugMoves if x not in non_dupes_debug]
            #next_move = self.moves.pop()
            
            
            test = self.actionMoves.pop()
            
            if test[0] == 1:
                #print("Coordinates",test[1],test[2])
                #UNCOVER -> y, x column, row 
                next_move = Action(AI.Action.UNCOVER, test[2], test[1])
                
            elif test[0] == 0: #flag
                next_move = Action(AI.Action.FLAG, test[2], test[1])
                
            #next_move = self.moves.pop()
            
            #next_move = non_dupes.pop()
            #print(non_dupes_debug)
            #self.debugMoves.pop()
            self.amove = next_move
           # print("uncovered:",self.frontier_uncovered)
           # print("covered:",self.frontier_covered)
            
            return next_move
                
        ########################################################################
        #                           YOUR CODE ENDS                             #
        ########################################################################
    
    def all_equal(self, iterator):
        iterator = iter(iterator)
        try:
            first = next(iterator) 
        except StopIteration:
            return True
        return all(first == x for x in iterator)
        
    def find_min_moves(self):
        
        #print('hi im here')
        coords = []
        
        #print('coords')
        for x in range(self.row):
            for y in range(self.col):
                if self.refLabel[x, y] == '':
                    coords.append((x, y))
    
        #print('get coords')
        #print(coords)
        vals = []
        new_coords = []      
        for i in coords:
            adj = self.getAdjacent(i[0], i[1])

            checker = False
            for j in adj:   
                if self.refLabel[j[0],j[1]] != '':
                    new_coords.append(i)
                    checker = True
                    break
            
            if checker:
                temp = 0
                for j in adj:
                    if self.elabel[j[0], j[1]] >=0 :
                        temp += self.elabel[j[0], j[1]]
                    
                vals.append(temp)
            else:
                continue
        
        t = self.all_equal(vals) 
        
        if t: # if it is true then all the values in he list are the same therefore cannot simply choose one
            
            #print('false')
            return False
        
        #print(new_coords)
        #print(vals)    
        min_val = min(vals)
        
        
        min_index = vals.index(min_val) # once we find the min values it has the less possibility of being a bomb?
            
            
        x = new_coords[min_index]
        #print(x)
            
        self.actionMoves.append([1, x[0], x[1]])
        #self.debugMoves.append([x[0],x[1]])
        self.refLabel[x[0], x[1]] == 'U'
        self.frontier_covered.append((x[0], x[1]))
        return True
            
            
        
                
                
    def find_moves(self):
        #print('hi im here :D')
        
            
        
        #print(self.frontier_covered)
        #print(self.frontier_uncovered)
        while True:
            
            
            #if self.n == 50:
                #return Action(AI.Action.LEAVE)
            
            
            if len(self.actionMoves) != 0: # has stuff to do
                #print('has stuff to do')

                return
            
            self.numTiles()
            if (self.row * self.col) - self.numOfMines == self.numUncoveredtiles: # goal
                
                #print('appending the end')
                self.moves.append(Action(AI.Action.LEAVE))
                return
            
            if len(self.frontier_covered) == 0: # frontier is empty
                
                #print('frontier empty so we scan again')
                
                self.scan() # find a move
                
                if len(self.frontier_covered) == 0 or len(self.actionMoves) == 0: # if still cannot find a move do a random move
                    
                    #print('Find lowest :c')
                    a = self.find_min_moves() ## get the lowest  adjacent number of bombs
                    if a == True:
                        #print('return')
                        return
                    
                    if len(self.actionMoves) == 0 or a == False: 
                    
                        #print('random')
                        self.chooseRandom()
                    
                    return
            
            #print(self.frontier_covered)
            coords = self.frontier_covered.pop()
            
           # if coords in self.frontier_uncovered or self.refLabel[coords[0], coords[1]] == 'U':
            #    continue
            self.ruleOfThumb(coords[0], coords[1])
            
            #self.n += 1
            
                
            
        
    def getSimpleProb(self): # probability of each tile being a bomb without prior knowledge
        n = self.numOfMines
        num = 0
        for x in range(self.row):
            for y in range(self.col):
                if self.refLabel[x, y] == '':
                    num +=1
                    
        self.p = n / num
        
    
    def applyOpeningProb(self):
        num = self.label[self.amove.getY(), self.amove.getX()]
        
        adj = self.getAdjacent(self.amove.getY(), self.amove.getX())
        
        
        if num / len(adj) < self.p: # uncover one of the random spots around the tile
            
            explore = self.getAdjacent( self.amove.getY(), self.amove.getX())
            coords = random.choice(explore)
            #print("Applying opening probability")
            
            self.actionMoves.append([1, coords[0], coords[1]])
            self.debugMoves.append([coords[0],coords[1]])
            self.refLabel[coords[0], coords[1]] = 'U'
            
            return True
        else:
            return False
        
        
    def numTiles(self):
        num = 0
        for x in range(self.row):
            for y in range(self.col):
                if self.refLabel[x, y] == 'U':
                    num += 1
        #print(self.refLabel)
        self.numUncoveredtiles = num
        
        
    #def getFrontier(self, x, y):
        
        
    def scan(self):
        #print('scanning')
        for i in range(self.row):
            for j in range(self.col):
                
                if self.label[i, j] >=0:
                    self.ruleOfThumb(i, j)
                    
                
        
    def ruleOfThumb(self, x, y):
        #print('ROT')
        test = False
        #print(self.amove.getX(), self.amove.getY())
        adj = self.getAdjacent(x, y) # get all the adjacent of the current move
        noFlag = self.countNoFlag(adj) # get all the number of no flags of the current move
        yesFlag = self.countFlag(adj) # get all the number of flags of the current move
        


        #print(x, y)
        
        #print(adj)
        ## effective label
        
        #print(self.frontier_covered)
        self.elabel[x, y] = self.label[x, y] - yesFlag
        
        #print(self.elabel[x, y])
        #print(x, y)
        if self.label[x, y] < 0:
            #print('big oof')
            return
            
        
        if self.elabel[x, y] == 0: # effective label  == 0
            #print('effective == 0')
            for t in adj:
                if self.refLabel[t[0], t[1]] == '': # if untouched
                    
                    #print('undiscovered tile and now inserting',t[0]," ",t[1])
                    #print("uncovered:",self.frontier_uncovered)
                    #print("covered:",self.frontier_covered)
                    #this is where dupes check 
                    
                    # check = [1,t[0],t[1]]
                    check = [1, t[0], t[1]]
                    
                    if check not in self.actionMoves:
                        self.actionMoves.append(check)
                    #self.moves.append(Action(AI.Action.UNCOVER, t[0], t[1]))
                    # check = [1,t[0],t[1]]
                    
                    
                    
                    #if check not in self.moves:
                         # self.moves.append([1,t[0],t[1]])
                    # move = self.moves.pop
                    # if(move[0] == 1):
                    #   (Action.UNCOVER,move[1],move[2])
                    
                    
                    #self.debugMoves.append([t[0],t[1]])
                    #self.refLabel[x[0], x[1]] = 'U'
                    #self.frontier_covered.append(x) # frontier covered around the 
                    #self.numUncoveredtiles += 1
                 
            
            test = True    
        
        
        elif self.elabel[x, y] == noFlag: # effective label == #no flags
            #print('Flag')
            for t in adj:
                if self.refLabel[t[0], t[1]] == '':
                    
                    #print('undiscovered tile and now inserting')
                    check = [0, t[0], t[1]]
                    if check not in self.actionMoves:
                        self.actionMoves.append(check)
                    
                    
                    #self.moves.append(Action(AI.Action.FLAG, t[0], t[1]))
                    #self.debugMoves.append('FLAG',t[0,t[1]])
                    self.refLabel[t[0], t[1]] = 'F'
                    
                temporary = self.getAdjacent(t[0], t[1])
                
                for x1 in temporary:
                    if self.refLabel[x1[0], x1[1]] != '':
                        self.elabel[x1[0], x1[1]] -= 1
            test = False
        
        else:
            #print('not done anything')
            return
        
        
        if test: # if uncovered then get the adjacent
            for a in adj:
                if a in self.frontier_uncovered:
                    continue
                if a not in self.frontier_covered:
                    self.frontier_covered.append(a) # get all the adjacents of the original adjacent as a frontier

                    #if a not in self.frontier_uncovered:
                        #self.frontier_covered.append(a) # get all the adjacents of the original adjacent as a frontier
        
        if noFlag == 0:
            #print('added one with no flag')
            self.frontier_uncovered.add((x, y))
    
    
    def countFlag(self, coords):
        
        yesFlag = 0
        for x in coords:

                
            if self.refLabel[x[0], x[1]] == 'F':
                yesFlag +=1
                
        return yesFlag
    
    def countNoFlag(self, coords):
        noFlag = 0
        for x in coords:

                
            if self.refLabel[x[0], x[1]] == '':
                noFlag +=1
                
        return noFlag
    
        
    def getAdjacent(self, a, b):
        
        coords = [(x + a, y + b)
                  for x in range(-1, 2) for y in range(-1, 2)
                  if (x, y) != (0, 0)] # get all the adjacent

        temp = [pair for pair in coords
                if self.tileinBounds(pair[0], pair[1])] # return the valid adjacents
        
        my_list = list(set(temp))
        
        return temp
 
    #check if tile is in Bounds or not
    def tileinBounds(self, x, y):
        
        return (x >= 0 and x < self.row) and (y >= 0 and y < self.col)
           
        

    def chooseRandom(self):
       
       
 
        explore = []
        for x in range(0, self.row):
            for y in range(0, self.col):
                if self.refLabel[x, y] == '': # if empty string then we explore
                    explore.append((x, y))
                    
        #print(explore)
 
        coords = random.choice(explore)
        self.refLabel[coords[0], coords[1]] == 'U'
        self.frontier_covered.append((coords[0], coords[1]))
        #print("CHOSE RANDOMLY")
        self.actionMoves.append([1, coords[0], coords[1]])
        
        
        #self.numUncoveredtiles += 1
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
 
