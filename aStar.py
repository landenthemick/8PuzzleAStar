# Landen Mick 1/19/23
# Program utilizes the A* algorithm to solve 8 puzzle challenge
# Example Start Matrix:
# 8 3 2
# 4 7 1
# 0 5 6
# End Goal Matrix:
# 1 2 3
# 4 5 6
# 7 8 0
from copy import deepcopy


# identifies class for node
class Node:

    # construct node with required attributes
    def __init__(self, board, g, member, parent, move):
        self.board = board
        self.g = g # (g)
        self.calcManhattan()  # (h)
        self.member = member
        self.calculateCost()
        self.parent = parent
        self.move = move

    # function for calculation of Manhattan Distance (h)
    def calcManhattan(self):
        total = 0
        # loop through board
        for counter in range(len(self.board) ** 2):
            for i in range(0, len(self.board)):
                for j in range(0, len(self.board)):
                    if (self.board[i][j] == counter):
                        # calculate x and y distance from each square to goal state
                        dist = abs(counter % 3 - j) + abs(counter // 3 - i)
                        #calculates hueristic value (cost to move from current to final cell)
                        total = total + dist
        self.h = total

    # function for calculation of cost value (f)
    def calculateCost(self):
        # defines cost as h + g
        self.cost = self.h + self.g

    def generateNodes(self):
        # create two lists for expansion
        openList = []
        closedList = []
        # loop through puzzle
        for i in range(0, len(self.board)):
            for j in range(0, len(self.board)):
                # find blank spaces
                if self.board[i][j] == 0:
                    blankRow = i
                    blankColumn = j
        # identifies moves based on location of blank space
        blankPos = [[blankRow - 1, blankColumn, "Up"],
                    [blankRow + 1, blankColumn, "Down"],
                    [blankRow, blankColumn - 1, "Left"],
                    [blankRow, blankColumn + 1, "Right"]]
        for i in range(0, len(blankPos)):
            for j in range(0, len(blankPos[i]) - 1):
                # cross-reference with bounds
                if (blankPos[i][j] > len(self.board) - 1) or (blankPos[i][j] < 0):
                    closedList.append(i)
        closedList.reverse()
        for i in closedList:
            # delete blank positions from closedList
            del blankPos[i]
        # expanding all possible nodes to find the lowest manhattan distance
        for i in range(0, len(blankPos)):
            #using deepcopy to copy node and keep addresses
            expandNodes = deepcopy(self.board)
            tempVar = expandNodes[blankPos[i][0]][blankPos[i][1]]
            expandNodes[blankPos[i][0]][blankPos[i][1]] = 0
            expandNodes[blankRow][blankColumn] = tempVar
            move = blankPos[i][2]
            openList.append(Node(expandNodes, self.g + 1, None, self, move))
        # return openList
        return openList


# check if goal state is met for completion
def checkGoal(pos):
    complete = True
    # loops through matrix to confirm goal state is met
    counter = 0
    for i in range(0, len(pos)):
        for j in range(0, len(pos)):
            # if goal state not met
            if pos[i][j] != counter:
                # set complete to false
                complete = False
            counter += 1
    return complete


# function to check resolvability
def isSolvable(state):
    even = False
    if len(state) % 2 == 0:
        even = True
    oneDArray = []
    # if odd
    if even == False:
        # construct 1D array
        for row in range(len(state)):
            for column in range(len(state[0])):
                # update 1DArray with row and col positions
                oneDArray.append(state[row][column])
        counter = 0
        increment = 0
        # counting inversions
        for index in oneDArray:
            if index != 0:
                for j in range(increment):
                    # compares to goal state
                    if oneDArray[j] > index:
                        counter += 1
            increment += 1
        # checks divisibility, if yes, return solvable
        solvable = (counter % 2 == 0)
        return solvable
    # if even
    else:
        # construct 1D array
        for row in range(len(state)):
            for column in range(len(state[0])):
                oneDArray.append(state[row][column])
                if puzzle[row][column] == 0:
                    # located row pos of blank space in matrix
                    blank = row
        counter = 0
        increment = 0
        # counting inversions
        for index in oneDArray:
            if index != 0:
                for j in range(increment):
                    # compares to goal state
                    if oneDArray[j] > index:
                        counter += 1
            increment += 1
        # adds blank row in inversion count
        counter = counter + blank
        # checks divisibility, if yes, return solvable
        solvable = (counter % 2 == 0)
        return solvable


# A* method
def solve(pos):
    # checks if solvable using isSolvable method
    if isSolvable(pos) == True:
        # construct node
        start = Node(pos, 0, None, None, None)
        # begins calculation of Manhattan Distance
        start.calcManhattan()
        # begins calculation of path cost
        start.calculateCost()
        # initialize open and closed lists
        openList = [start]
        closedList = []
        # while openList != empty
        while len(openList) != 0:
            # uses lambda function to define autonomous function (sort)
            openList.sort(key=lambda node: node.cost, reverse=False)
            # if openList matches with board
            if checkGoal(openList[0].board) == True:
                # user prompt
                print("***********************")
                print("Reached the goal state!")
                print("***********************")
                # calls on move counter
                moves = str(openList[0].g)
                # print # of moves
                print("Number of moves: " + moves)
                # identifying expanding node and assigning it to node
                node = openList[0]
                path = []
                # while expanding node has a parent
                while node.parent != None:
                    # records move
                    path.append(node.move)
                    # moving up the tree
                    node = node.parent
                # reverse path to print in correct order
                path.reverse()
                # print path list
                print(*path, sep=", ")
                break
            # if open list doesn't match with board, generate more nodes
            childNodes = openList[0].generateNodes()
            for member in childNodes:
                best = True
                # checks list for more efficient members
                for item in openList:
                    if item.board == member.board and item.cost == member.cost:
                        best = False
                for item in closedList:
                    if item.board == member.board and item.cost == member.cost:
                        best = False
                # if there are none, append list
                if best == True:
                    openList.append(member)
            del openList[0]
            closedList.append(openList[0])

    else:
        # print not solvable
        print("This is not solvable")


# method for user initial state
def initialState():
    # test data provided
    puzzle = [[8, 3, 2], [4, 7, 1], [0, 5, 6]]
    # loop through all positions in matrix
    for row in range(3):
        for column in range(3):
            # user input for each position
            puzzle[row][column] = int(input("Enter Tile " + str(row) + " " +
                                            str(column) + ": "))
    # returns user inputted initial state
    print("Initial State")
    # print user matrix visual
    for number in range(3):
        print(str(puzzle[number][0]) + "  " + str(puzzle[number][1]) + "  " +
              str(puzzle[number][2]))
    return puzzle


# main method
def main():
    # test data provided
    startPos = [[8, 3, 2], [4, 7, 1], [0, 5, 6]]
    # calls for user input
    puzzle = initialState()
    # run algorithm on inputted inital state
    solve(startPos)


# run main method
main()
