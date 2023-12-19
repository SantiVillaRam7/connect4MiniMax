import copy # For copying the game board
# Creates a node for the minimax tree
# the player for the AI is 1, the player for the human is 2
class Node:
    def __init__(self, value=0, children=None, player=0, i=0, j=0):
        self.value = value
        if children is None:
            children = []
        self.children = children
        self.player = player
        self.i = i
        self.j = j
    def addchild(self, child): # adds a child node
        self.children.append(child)
    def setplace(self, row,col):
        self.i=row
        self.j=col  
    def setvalue(self, value):
        self.value=value
    def __str__(self):
        return str(self.value)
    def toStr(self, depth=0):
        # Print the current node's value with proper indentation
        print("  " * depth + self.__str__())
        # Recursively print child nodes
        for child in self.children:
            child.toStr(depth + 1)
# Creates a tree for the minimax algorithm







#Simulates a game
class Game:
    def __init__(self):
        self.board = [[0 for _ in range(7)] for _ in range(6)]
        self.last=Node(0, None, 1, 0, 0)
    #To string
    def toStr(self):
        for row in self.board:
            print(row)
    #make a move
    def move(self, col, player):
        if col < 0 or col > 6:
            print("Invalid column. Column must be between 0 and 6.")
            return False

        for i in range(5, -1, -1):  # Start from the bottom row (index 5) and go upwards
            if self.board[i][col] == 0:
                self.board[i][col] = player
                self.board[i][col]  # Update the last move
                print("Move made.")
                if self.finish(player):
                    print("Player " + str(player) + " wins.")
                    return True
                return i
        print("Column is full")
        return False
    #check if the game is over
    def finish(self, player):
        for i in range(6):
            for j in range(7):
                if self.check(player, i, j):
                    return True
        return False
    #check if there are 4 in a row
    def check(self, player, row, col):
        # Check horizontally
        for i in range(4):
            if col + i >= 7:
                break  # Stop if we reach the right edge
            if self.board[row][col + i] != player:
                break
        else:
            return True  # Found four in a row horizontally

        # Check vertically
        for i in range(4):
            if row + i >= 6:
                break  # Stop if we reach the bottom
            if self.board[row + i][col] != player:
                break
        else:
            return True  # Found four in a row vertically
        # Check diagonally (top-left to bottom-right)
        for i in range(4):
            if row + i >= 6 or col + i >= 7:
                break  # Stop if we reach the edge
            if self.board[row + i][col + i] != player:
                break
        else:
            return True  # Found four in a row diagonally

        # Check diagonally (bottom-left to top-right)
        for i in range(4):
            if row - i < 0 or col + i >= 7:
                break  # Stop if we reach the edge
            if self.board[row - i][col + i] != player:
                break
        else:
            return True  # Found four in a row diagonally

        return False  # No four in a row found
    def hplay(self, col):#human play
        row=self.move(col, 2)
        self.last=Node(0, None, 2, row, col)
        self.toStr()
    def aiplay(self):#ai play
        print("AI play")
        print(self.last)
        tree=Tree(self.last, self)
        tree.buildTree()
        #tree.setheuristic()
        best=tree.find_best_move(3) #find the best move, maybe need to change the depth ++++++++++++++++++++++
        self.move(best.j, 1)
        self.toStr()

game=Game()
game.move(0, 2)
game.move(0, 1)
game.move(0, 2)
game.move(0, 2)
game.move(0, 1)
game.move(0, 2)
game.move(0, 1)
game.toStr()