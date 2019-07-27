import numpy as np
import random
import time


class Game():
    # Creates the game and initializes necessary values
    def __init__(self, width, height, display = True, stateRows = 4):
        self.width = width
        self.height = height
        self.gameOver = False
        self.score = 0
        self.reward = 0
        self.blocked = False
        self.stateRows = stateRows
        self.showGame = display
        self.totalLines = 0 
        
        # Numbers to represent what piece occupies the spot
        self.emptyVal = 0
        self.lineBlock = 1
        self.blueLBlock = 2
        self.orangeLBlock = 3
        self.squareBlock = 4
        self.greenZBlock = 5
        self.redZBlock = 6
        self.TBlock = 7
        
        # Creating the board and spawning the first piece
        self.board = np.zeros([height+4,width],dtype=int)
        self.piece = dict()
        self.spawnPiece()
        
    
    # Spawns a new piece randomly.
    # Depending on the piece that spawns, it will generate the spawning spots
    # and check if any of these spots are occupied
    def spawnPiece(self):
        pieceToSpawn = random.randint(self.lineBlock,self.TBlock)
        
        if(pieceToSpawn == self.lineBlock):
            spawnSpots = [(1,int(self.width/2-2)),(1,int(self.width/2-1)),(1,int(self.width/2)),(1,int(self.width/2+1))]
                
        elif(pieceToSpawn == self.blueLBlock):
            spawnSpots = [(0,int(self.width/2-1)),
                          (1,int(self.width/2-1)),(1,int(self.width/2)),(1,int(self.width/2+1))]
            
        elif(pieceToSpawn == self.orangeLBlock):
            spawnSpots =                                                [(0,int(self.width/2+1)),
                          (1,int(self.width/2-1)),(1,int(self.width/2)),(1,int(self.width/2+1))]
            
        elif(pieceToSpawn == self.squareBlock):
            spawnSpots = [(0,int(self.width/2-1)),(0,int(self.width/2)),
                            (1,int(self.width/2-1)),(1,int(self.width/2))]
            
        elif(pieceToSpawn == self.greenZBlock):
            spawnSpots =                         [(0,int(self.width/2)),(0,int(self.width/2+1)),
                          (1,int(self.width/2-1)),(1,int(self.width/2))]
            
        elif(pieceToSpawn == self.redZBlock):
            spawnSpots = [(0,int(self.width/2-1)),(0,int(self.width/2)),
                                                  (1,int(self.width/2)),(1,int(self.width/2+1))]       
            
        elif(pieceToSpawn == self.TBlock):
            spawnSpots =                           [(0,int(self.width/2)),
                            (1,int(self.width/2-1)),(1,int(self.width/2)),(1,int(self.width/2+1))]
            
        self.writeSpots(spawnSpots,pieceToSpawn)
        self.piece["type"] = pieceToSpawn
        self.piece["spots"] = spawnSpots
        self.piece["rotation"] = 0
        

    # Helper function that writes the given piece to the given spots    
    def writeSpots(self,spots,piece):
        for spot in spots:
            self.board[spot[0],spot[1]] = piece
        
        
    # Displays the game (for console version)
    def display(self):
        if self.showGame:
            time.sleep(0.05)
            for i in range(self.width+2):
                print('-', end='')
            for i in range(4):
                print('\n|', end='')
                for j in range(self.width):
                    if self.board[i,j] == self.emptyVal:
                        print(' ', end='')
                    else:
                        print(self.board[i,j],end='')
                print('|', end='')
            print()
            for i in range(self.width+2):
                print('-', end='')
            for i in range(self.height):
                print('\n|', end='')
                for j in range(self.width):
                    if self.board[i+4,j] == self.emptyVal:
                        print(' ', end='')
                    else:
                        print(self.board[i+4,j],end='')
                print('|', end='')
            print()
            for i in range(self.width+2):
                print('-', end='')
            print("\n")
        
    
    # Helper function to increment the rotation
    def nextRotation(self):
        if self.piece["rotation"] < 3:
            self.piece["rotation"] += 1
        else:
            self.piece["rotation"] = 0
    
    
    # Rotates the piece
    def rotatePiece(self):
        self.writeSpots(self.piece["spots"],0)
        newSpots = self.getRotationSpots()
        # If any of the new spots are off of the board, don't perform the rotation
        for spot in newSpots:
            if spot[0] >= self.height or spot[0] < 0 or spot[1] >= self.width or spot[1] < 0:
                self.writeSpots(self.piece["spots"],self.piece["type"])
                return
        # If any of the new spots are occupied, don't perform the rotation
        for spot in newSpots:
            if self.board[spot[0],spot[1]] != 0:
                self.writeSpots(self.piece["spots"],self.piece["type"])
                return
        # If everything is good
        self.writeSpots(newSpots, self.piece["type"])
        self.piece["spots"] = newSpots
        self.nextRotation()
    
    # Helper function that gets the rotation spots and returns them
    def getRotationSpots(self):
        # Rotation for the line block
        if self.piece["type"] == self.lineBlock:
            if self.piece["rotation"] == 0:
                rotationSpots = [(self.piece["spots"][0][0]-1,self.piece["spots"][0][1]+2),
                                 (self.piece["spots"][1][0],self.piece["spots"][1][1]+1),
                                 (self.piece["spots"][2][0]+1,self.piece["spots"][2][1]),
                                 (self.piece["spots"][3][0]+2,self.piece["spots"][3][1]-1)]
            elif self.piece["rotation"] == 1:
                rotationSpots = [(self.piece["spots"][0][0]+2,self.piece["spots"][0][1]+1),
                                 (self.piece["spots"][1][0]+1,self.piece["spots"][1][1]),
                                 (self.piece["spots"][2][0],self.piece["spots"][2][1]-1),
                                 (self.piece["spots"][3][0]-1,self.piece["spots"][3][1]-2)]
            elif self.piece["rotation"] == 2:
                rotationSpots = [(self.piece["spots"][0][0]+1,self.piece["spots"][0][1]-2),
                                 (self.piece["spots"][1][0],self.piece["spots"][1][1]-1),
                                 (self.piece["spots"][2][0]-1,self.piece["spots"][2][1]),
                                 (self.piece["spots"][3][0]-2,self.piece["spots"][3][1]+1)]
            elif self.piece["rotation"] == 3:
                rotationSpots = [(self.piece["spots"][0][0]-2,self.piece["spots"][0][1]-1),
                                 (self.piece["spots"][1][0]-1,self.piece["spots"][1][1]),
                                 (self.piece["spots"][2][0],self.piece["spots"][2][1]+1),
                                 (self.piece["spots"][3][0]+1,self.piece["spots"][3][1]+2)]
        # Rotation for the blue L block     
        elif self.piece["type"] == self.blueLBlock:
            if self.piece["rotation"] == 0:
                rotationSpots = [(self.piece["spots"][0][0],self.piece["spots"][0][1]+2),
                                 (self.piece["spots"][1][0]-1,self.piece["spots"][1][1]+1),
                                 (self.piece["spots"][2][0],self.piece["spots"][2][1]),
                                 (self.piece["spots"][3][0]+1,self.piece["spots"][3][1]-1)]
            elif self.piece["rotation"] == 1:
                rotationSpots = [(self.piece["spots"][0][0]+2,self.piece["spots"][0][1]),
                                 (self.piece["spots"][1][0]+1,self.piece["spots"][1][1]+1),
                                 (self.piece["spots"][2][0],self.piece["spots"][2][1]),
                                 (self.piece["spots"][3][0]-1,self.piece["spots"][3][1]-1)]
            elif self.piece["rotation"] == 2:
                rotationSpots = [(self.piece["spots"][0][0],self.piece["spots"][0][1]-2),
                                 (self.piece["spots"][1][0]+1,self.piece["spots"][1][1]-1),
                                 (self.piece["spots"][2][0],self.piece["spots"][2][1]),
                                 (self.piece["spots"][3][0]-1,self.piece["spots"][3][1]+1)]
            elif self.piece["rotation"] == 3:
                rotationSpots = [(self.piece["spots"][0][0]-2,self.piece["spots"][0][1]),
                                 (self.piece["spots"][1][0]-1,self.piece["spots"][1][1]-1),
                                 (self.piece["spots"][2][0],self.piece["spots"][2][1]),
                                 (self.piece["spots"][3][0]+1,self.piece["spots"][3][1]+1)]
        # Rotation for the the orange L block
        elif self.piece["type"] == self.orangeLBlock:
            if self.piece["rotation"] == 0:
                rotationSpots = [(self.piece["spots"][0][0]+2,self.piece["spots"][0][1]),
                                 (self.piece["spots"][1][0]-1,self.piece["spots"][1][1]+1),
                                 (self.piece["spots"][2][0],self.piece["spots"][2][1]),
                                 (self.piece["spots"][3][0]+1,self.piece["spots"][3][1]-1)]
            elif self.piece["rotation"] == 1:
                rotationSpots = [(self.piece["spots"][0][0],self.piece["spots"][0][1]-2),
                                 (self.piece["spots"][1][0]+1,self.piece["spots"][1][1]+1),
                                 (self.piece["spots"][2][0],self.piece["spots"][2][1]),
                                 (self.piece["spots"][3][0]-1,self.piece["spots"][3][1]-1)]
            elif self.piece["rotation"] == 2:
                rotationSpots = [(self.piece["spots"][0][0]-2,self.piece["spots"][0][1]),
                                 (self.piece["spots"][1][0]+1,self.piece["spots"][1][1]-1),
                                 (self.piece["spots"][2][0],self.piece["spots"][2][1]),
                                 (self.piece["spots"][3][0]-1,self.piece["spots"][3][1]+1)]
            elif self.piece["rotation"] == 3:
                rotationSpots = [(self.piece["spots"][0][0],self.piece["spots"][0][1]+2),
                                 (self.piece["spots"][1][0]-1,self.piece["spots"][1][1]-1),
                                 (self.piece["spots"][2][0],self.piece["spots"][2][1]),
                                 (self.piece["spots"][3][0]+1,self.piece["spots"][3][1]+1)]
        # Rotation for the square block
        elif self.piece["type"] == self.squareBlock:
            rotationSpots = self.piece["spots"]
        # Rotation for the green Z block
        elif self.piece["type"] == self.greenZBlock:
            if self.piece["rotation"] == 0:
                rotationSpots = [(self.piece["spots"][0][0]+1,self.piece["spots"][0][1]+1),
                                 (self.piece["spots"][1][0]+2,self.piece["spots"][1][1]),
                                 (self.piece["spots"][2][0]-1,self.piece["spots"][2][1]+1),
                                 (self.piece["spots"][3][0],self.piece["spots"][3][1])]
            elif self.piece["rotation"] == 1:
                rotationSpots = [(self.piece["spots"][0][0]+1,self.piece["spots"][0][1]-1),
                                 (self.piece["spots"][1][0],self.piece["spots"][1][1]-2),
                                 (self.piece["spots"][2][0]+1,self.piece["spots"][2][1]+1),
                                 (self.piece["spots"][3][0],self.piece["spots"][3][1])]
            elif self.piece["rotation"] == 2:
                rotationSpots = [(self.piece["spots"][0][0]-1,self.piece["spots"][0][1]-1),
                                 (self.piece["spots"][1][0]-2,self.piece["spots"][1][1]),
                                 (self.piece["spots"][2][0]+1,self.piece["spots"][2][1]-1),
                                 (self.piece["spots"][3][0],self.piece["spots"][3][1])]
            elif self.piece["rotation"] == 3:
                rotationSpots = [(self.piece["spots"][0][0]-1,self.piece["spots"][0][1]+1),
                                 (self.piece["spots"][1][0],self.piece["spots"][1][1]+2),
                                 (self.piece["spots"][2][0]-1,self.piece["spots"][2][1]-1),
                                 (self.piece["spots"][3][0],self.piece["spots"][3][1])]
        # Rotation for the red Z block
        elif self.piece["type"] == self.redZBlock:
            if self.piece["rotation"] == 0:
                rotationSpots = [(self.piece["spots"][0][0],self.piece["spots"][0][1]+2),
                                 (self.piece["spots"][1][0]+1,self.piece["spots"][1][1]+1),
                                 (self.piece["spots"][2][0],self.piece["spots"][2][1]),
                                 (self.piece["spots"][3][0]+1,self.piece["spots"][3][1]-1)]
            elif self.piece["rotation"] == 1:
                rotationSpots = [(self.piece["spots"][0][0]+2,self.piece["spots"][0][1]),
                                 (self.piece["spots"][1][0]+1,self.piece["spots"][1][1]-1),
                                 (self.piece["spots"][2][0],self.piece["spots"][2][1]),
                                 (self.piece["spots"][3][0]-1,self.piece["spots"][3][1]-1)]
            elif self.piece["rotation"] == 2:
                rotationSpots = [(self.piece["spots"][0][0],self.piece["spots"][0][1]-2),
                                 (self.piece["spots"][1][0]-1,self.piece["spots"][1][1]-1),
                                 (self.piece["spots"][2][0],self.piece["spots"][2][1]),
                                 (self.piece["spots"][3][0]-1,self.piece["spots"][3][1]+1)]
            elif self.piece["rotation"] == 3:
                rotationSpots = [(self.piece["spots"][0][0]-2,self.piece["spots"][0][1]),
                                 (self.piece["spots"][1][0]-1,self.piece["spots"][1][1]+1),
                                 (self.piece["spots"][2][0],self.piece["spots"][2][1]),
                                 (self.piece["spots"][3][0]+1,self.piece["spots"][3][1]+1)]                         
        # Rotation for the T block
        elif self.piece["type"] == self.TBlock:
            if self.piece["rotation"] == 0:
                rotationSpots = [(self.piece["spots"][0][0]+1,self.piece["spots"][0][1]+1),
                                 (self.piece["spots"][1][0]-1,self.piece["spots"][1][1]+1),
                                 (self.piece["spots"][2][0],self.piece["spots"][2][1]),
                                 (self.piece["spots"][3][0]+1,self.piece["spots"][3][1]-1)]
            elif self.piece["rotation"] == 1:
                rotationSpots = [(self.piece["spots"][0][0]+1,self.piece["spots"][0][1]-1),
                                 (self.piece["spots"][1][0]+1,self.piece["spots"][1][1]+1),
                                 (self.piece["spots"][2][0],self.piece["spots"][2][1]),
                                 (self.piece["spots"][3][0]-1,self.piece["spots"][3][1]-1)]
            elif self.piece["rotation"] == 2:
                rotationSpots = [(self.piece["spots"][0][0]-1,self.piece["spots"][0][1]-1),
                                 (self.piece["spots"][1][0]+1,self.piece["spots"][1][1]-1),
                                 (self.piece["spots"][2][0],self.piece["spots"][2][1]),
                                 (self.piece["spots"][3][0]-1,self.piece["spots"][3][1]+1)]
            elif self.piece["rotation"] == 3:
                rotationSpots = [(self.piece["spots"][0][0]-1,self.piece["spots"][0][1]+1),
                                 (self.piece["spots"][1][0]-1,self.piece["spots"][1][1]-1),
                                 (self.piece["spots"][2][0],self.piece["spots"][2][1]),
                                 (self.piece["spots"][3][0]+1,self.piece["spots"][3][1]+1)]
        return rotationSpots
        
            
    # Moves the piece left or right, depending on the input direction (+/- 1)
    def moveSideways(self, direction):
        # Checking that it is not all the way to the left or right already
        for spot in self.piece["spots"]:
            if direction == -1:
                if spot[1] == 0:
                    return
            elif direction == 1:
                if spot[1] == self.width-1:
                    return
        # Setting old spots to empty
        self.writeSpots(self.piece["spots"],0)
        # Moving piece
        for i,spot in enumerate(self.piece["spots"]):
            self.piece["spots"][i] = (spot[0],spot[1]+direction)
            self.board[spot[0],spot[1]+direction] = self.piece["type"]
        
    
    # Drops the piece as far as it can go and locks it into place, 
    # then breaks rows and spawns a new piece
    def dropPiece(self):
        # Lowers the piece one row at a time until it can't be lowered further
        while True:
            shouldBreak = False
            self.writeSpots(self.piece["spots"],0)
            # Checking to ensure the piece isn't all the way at the bottom
            for spot in self.piece["spots"]:
                if spot[0] == self.height+3:
                    # Put the piece value back into the old spots
                    self.writeSpots(self.piece["spots"],self.piece["type"])
                    shouldBreak = True
                    break
            if shouldBreak:
                break
            # Checking to ensure that there is not another piece blocking the piece from dropping
            for spot in self.piece["spots"]:
                if self.board[spot[0]+1,spot[1]] != 0:
                    # Put the piece value back into the old spots
                    self.writeSpots(self.piece["spots"],self.piece["type"])
                    shouldBreak = True
                    break
            if shouldBreak:
                break
            # Moves the piece down a row
            else:
                for i,spot in enumerate(self.piece["spots"]):
                    self.piece["spots"][i] = (spot[0]+1,spot[1])
                    self.board[spot[0]+1,spot[1]] = self.piece["type"]
                self.display()                    
        for spot in self.piece["spots"]:
            if spot[0] < 4:
                self.gameOver = True
                return
        
        # Breaks rows and updates score
        self.breakRows()
        if self.rowsBroken == 1:
            self.score += 40
        elif self.rowsBroken == 2:
            self.score += 100
        elif self.rowsBroken == 3:
            self.score += 300
        elif self.rowsBroken == 4:
            self.score += 1200
        # Checks if the drop blocked a spot
        self.blocked = self.didBlock()
        # Calculating reward
        self.calcReward()
        # Spawns a new piece after the piece has dropped all the way 
        self.spawnPiece()
        
    
    # Checks whether the drop blocked or not.
    # Block is considered if there is an empty space beneath where the block dropped.
    def didBlock(self):
        for spot in self.piece["spots"]:
            if spot[0] != self.height+3:
                if self.board[spot[0]+1,spot[1]] == 0:
                    return True
        return False
    
    
    # Checks if rows can be broken after a piece is dropped,
    # and breaks them if it is required
    def breakRows(self):
        breakRow = True
        self.rowsBroken = 0
        # Can break a maximum of 4 rows at a time
        for iteration in range(4):
            # Iterate through every row starting at the bottom
            for row in range(self.height+3,3,-1):
                breakRow = True
                # Iterate through every column. If any spots are empty, don't break the row
                for column in range(self.width):
                    if self.board[row,column] == 0:
                        breakRow = False
                        break
                # Breaks the row if it is full
                if breakRow:
                    self.totalLines += 1
                    self.rowsBroken += 1
                    # Sets every column in the row
                    for column in range(self.width):
                        # If it's the top row, sets to empty
                        if row == 4:
                            self.board[row,column] = 0
                        # Otherwise, sets to the row above it
                        else:
                            self.board[row,column] = self.board[row-1,column]
                    # For every row above the current row
                    for rowAbove in range(row-1,3,-1):
                        for column in range(self.width):
                            # Sets the row to empty if it is the top row
                            if rowAbove == 4:
                                self.board[rowAbove,column] = 0    
                            # Otherwise, sets the row to the row above it
                            else:
                                self.board[rowAbove,column] = self.board[rowAbove-1,column]
                    # Resets breakRow and breaks from the loop
                    breakRow = True
                    break
    
    
    # Created for use in Q Learning
    # action is maximum 4*width - 1
    # 0 to width - 1 -> default rotation
    # width to 2*width - 1 -> 1 rotation, etc
    # Remainder after rotating is how many times it should move right from the left edge
    def makeMove(self, action):
        # Rotating and reducing action
        while action > self.width - 1:
            self.rotatePiece()
            action -= self.width
        # Moving the piece all the way to the left
        for i in range(self.width):
            self.moveSideways(-1)
        # Moving the piece the indicated number of times to the right
        while action > 0:
            self.moveSideways(1)
            action -= 1
        # Dropping piece  
        self.dropPiece()
        
    
    # Calculates the reward of an action
    def calcReward(self):
        self.reward = 0
        if self.rowsBroken == 1:
            self.reward = 1000
        elif self.rowsBroken == 2:
            self.reward = 2000
        elif self.rowsBroken == 3:
            self.reward = 3000
        elif self.rowsBroken == 4:
            self.reward = 4000
        if self.blocked:
            self.reward -= 10
        else:
            self.reward += 10
        # Higher reward for putting pieces in lower spots
        for i in range(4):
            self.reward += self.piece["spots"][i][0] * 5
        if self.gameOver:
            self.reward = -10000  

        
             
    
if __name__ == "__main__":
    game = Game(10, 20)
    game.display()
    while True:
        direction = input("Enter command (w,a,s,d or q to quit): ")
        if direction == 'w':
            game.rotatePiece()
        elif direction == 'a':
            game.moveSideways(-1)
        elif direction == 's':
            game.dropPiece()
        elif direction == 'd':
            game.moveSideways(1)
        elif direction == 'q':
            break
        if game.gameOver:
            print("Game Over, Score:", game.score)
            break
        else:
            game.display()
            print("Score:", game.score)
    
    
    
    
    
    
    
    
    
    
    
    
    