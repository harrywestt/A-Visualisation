"""
Project: A* Algorithm Visualisation
Version: 1.2
Author: Harry West
Date: 08/2021
"""

from random import randint
import pygame
import sys
import aStar


class setup:
    def __init__(self, width, height, gridSize):
        # Sets the width, height and grid size for the screen
        self.width, self.height = width, height
        self.gridSize = gridSize

        # Variables for the buttons, self.selected will be used to check which button is in use
        self.selected = "WALL"
        self.playBlocked = True
        self.startFlagBlocked = False
        self.endFlagBlocked = False
        self.wallBlocked = False

        # Colour of the children from the A*, put here so it can be changed. self.down is used to change the direction of the colour change
        self.childColour = [78, 159, 224]
        self.down = False

        # Two lists that store the positions of the walls and the positions of every block
        self.wallLocations = []
        self.positions = []

        # Fills the background of the window to be a gray colour
        window.fill((43, 43, 43))

        # Loads images and scales them to the correct size
        self.startButton = pygame.image.load("assets/playButton.png")
        self.startButton = pygame.transform.scale(self.startButton, (100, 100))
        self.startFlag = pygame.image.load("assets/startFlag.png")
        self.startFlag = pygame.transform.scale(self.startFlag, (100, 100))
        self.endFlag = pygame.image.load("assets/endFlag.png")
        self.endFlag = pygame.transform.scale(self.endFlag, (100, 100))
        self.wall = pygame.image.load("assets/wall.png")
        self.wall = pygame.transform.scale(self.wall, (100, 100))
        self.block = pygame.image.load("assets/block.png")
        self.block = pygame.transform.scale(self.block, (100, 100))

    def drawBottom(self):
        # Method for drawing the button section of the screen, needs to be recalled anytime a button is locked/unlocked
        pygame.draw.rect(window, (43, 43, 43), (0, 750, self.width, self.height))  # Draws background
        pygame.draw.line(window, (190, 145, 23), (0, self.height - 100), (self.width, self.height - 100), 3)
        # Draws orange evenly spaced lines at the bottom of the screen
        for i in range(int(self.width / 4), self.width, int(self.width / 4)):
            pygame.draw.line(window, (190, 145, 23), (i, self.height - 100), (i, self.height), 3)
        pygame.draw.line(window, (190, 145, 23), (1, self.height - 100), (1, self.height), 3)

    def drawGrid(self):
        # Iterates over the width of the screen by the grid size
        for i in range(0, self.width, self.gridSize):
            # Draws the vertical and horizontal lines
            pygame.draw.line(window, (169, 183, 198), (i, 0), (i, self.height - 100))
            pygame.draw.line(window, (169, 183, 198), (0, i), (self.width, i))

        # Draws the final three lines to close the final boxes in the grid
        pygame.draw.line(window, (169, 183, 198), (self.width - 1, 0), (self.width - 1, self.height - 100))
        pygame.draw.line(window, (169, 183, 198), (0, 1), (self.width, 1))

        # Draws the bottom of the screen
        self.drawBottom()

        # Updates the display
        pygame.display.update()

    def drawButtons(self):
        # Draws the bottom of the screen
        self.drawBottom()

        # Checks if the play button can be unlocked
        if self.startFlagBlocked and self.endFlagBlocked and not self.wallBlocked:
            self.playBlocked = False

        # Blits the images to the screen in the correct locations
        window.blit(self.startButton, ((self.width / 8) - 50, self.height - 100))
        window.blit(self.startFlag, ((self.width / 8) * 3 - 50, self.height - 100))
        window.blit(self.endFlag, ((self.width / 8) * 5 - 50, self.height - 100))
        window.blit(self.wall, ((self.width / 8) * 7 - 50, self.height - 100))

        # Checks if the buttons are blocked, if so, will put the block image over top
        if self.playBlocked:
            window.blit(self.block, ((self.width / 8) - 50, self.height - 100))
        if self.startFlagBlocked:
            window.blit(self.block, ((self.width / 8) * 3 - 50, self.height - 100))
        if self.endFlagBlocked:
            window.blit(self.block, ((self.width / 8) * 5 - 50, self.height - 100))
        if self.wallBlocked:
            window.blit(self.block, ((self.width / 8) * 7 - 50, self.height - 100))

        # Updates the display
        pygame.display.update()

    def drawOnBackground(self, x, y):
        # Method for drawing at the location selected

        # Checks the selected item and if the item is already on the screen
        if self.selected == "WALL" and [int(x // self.gridSize), int(y // self.gridSize)] not in self.positions:
            # Adds the new position to the lists
            self.positions.append([int(x // self.gridSize), int(y // self.gridSize)])
            self.wallLocations.append([int(x // self.gridSize), int(y // self.gridSize)])
            # Draws a orange square in the correct location
            pygame.draw.rect(window, (190, 145, 23), (int(x // self.gridSize * 25) + 1, int(y // self.gridSize * 25) + 1, self.gridSize - 1, self.gridSize - 1))
        # Checks the selected item and if the item is already on the screen
        elif self.selected == "START FLAG" and [int(x // self.gridSize), int(y // self.gridSize)] not in self.positions:
            # Adds the new position to the lists
            self.positions.append([int(x // self.gridSize), int(y // self.gridSize)])
            self.startFlagLocation = [int(x // self.gridSize), int(y // self.gridSize)]
            # Draws a green square at the start location
            pygame.draw.rect(window, (73, 156, 84), (int(x // self.gridSize * 25) + 1, int(y // self.gridSize * 25) + 1, self.gridSize - 1, self.gridSize - 1))
            # Locks the start flag button and prevents a second being placed
            self.selected = ""
            self.startFlagBlocked = True
            self.drawButtons()
        # Checks the selected item and if the item is already on the screen
        elif self.selected == "END FLAG" and [int(x // self.gridSize), int(y // self.gridSize)] not in self.positions:
            # Adds the new position to the lists
            self.positions.append([int(x // self.gridSize), int(y // self.gridSize)])
            self.endFlagLocation = [int(x // self.gridSize), int(y // self.gridSize)]
            # Draws a red square at the end point
            pygame.draw.rect(window, (199, 84, 80), (int(x // self.gridSize * 25) + 1, int(y // self.gridSize * 25) + 1, self.gridSize - 1, self.gridSize - 1))
            # Locks the end flag button and prevents a second being placed
            self.selected = ""
            self.endFlagBlocked = True
            self.drawButtons()
        # Updates the screen
        pygame.display.update()

    def drawSolution(self, points, finished):
        # Iterates over all the points
        for point in points:
            # Checks if this point is a child
            if not finished:
                # Checks if the point has never been drawn before
                if point not in self.positions:
                    # Changes the new child colours slightly
                    if self.childColour[1] != 0 and self.childColour[0] != 255 and self.childColour[1] != 255 and self.childColour[0] != 0:
                        if self.down:
                            self.childColour[1] -= 1
                            self.childColour[0] += 1
                        else:
                            self.childColour[1] += 1
                            self.childColour[0] -= 1
                    else:
                        self.down = True
                        if self.childColour[0] == 255 or self.childColour[1] == 0:
                            self.childColour[1] += 1
                            self.childColour[0] -= 1
                        else:
                            self.childColour[1] -= 1
                            self.childColour[0] += 1

                    # Draws the child to the screen
                    pygame.draw.rect(window, tuple(self.childColour), (int(point[0] * 25) + 1, int(point[1] * 25) + 1, self.gridSize - 1, self.gridSize - 1))

            # Check if this is the solution
            else:
                # Draws the solution, as well as the flags again
                pygame.draw.rect(window, (255, 0, 0), (int(point[0] * 25) + 1, int(point[1] * 25) + 1, self.gridSize - 1, self.gridSize - 1))
                pygame.draw.rect(window, (73, 156, 84), (self.startFlagLocation[0] * 25 + 1, self.startFlagLocation[1] * 25 + 1, self.gridSize - 1,self.gridSize - 1))
                pygame.draw.rect(window, (199, 84, 80), (self.endFlagLocation[0] * 25 + 1, self.endFlagLocation[1] * 25 + 1, self.gridSize - 1,self.gridSize - 1))
            # Updates the position list with the new point
            self.positions.append(point)
            # Updates the display
            pygame.display.update()

    def checkClick(self, x, y):
        # For dealing with the grid
        if y <= 750:
            # Draws at the selected location
            self.drawOnBackground(x, y)
        # For dealing with buttons
        else:
            # Will check if inside the correct x coordinate and the button is not locked
            if x <= 185 and not self.playBlocked:
                # If play is clicked, the player cannot press anymore buttons and cannot draw
                self.selected = ""
                self.startFlagBlocked = True
                self.playBlocked = True
                self.endFlagBlocked = True
                self.wallBlocked = True
                self.drawButtons()
                # Returns true so the simulation will start
                return True
            elif 185 < x < 375 and not self.startFlagBlocked:
                # Changes selected to start flag if start flag was pressed
                self.selected = "START FLAG"
            elif 376 < x < 561 and not self.endFlagBlocked:
                # Changes selected to end flag if end flag was pressed
                self.selected = "END FLAG"
            elif 562 < x < 751 and not self.wallBlocked:
                # Changes selected to wall if wall is pressed
                self.selected = "WALL"
        # Prevents simulation until play button is pressed
        return False


if __name__ == '__main__':
    # Initialises pygame
    pygame.init()

    # Sets the screen size and creates a window
    size = screenWidth, screenHeight = (750, 850)
    window = pygame.display.set_mode(size)
    pygame.display.set_caption("A* Algorithm")

    # Creates a screen and draws the background and buttons
    screen = setup(screenWidth, screenHeight, 25)
    screen.drawGrid()
    screen.drawButtons()

    # Used so drawing can include dragging
    drag = False
    # Used for simulation
    ready = False
    firstRun = True

    # Game loop
    while True:
        # Iterates through all the events
        for event in pygame.event.get():
            # Checks if the player has quit, if so will close the window
            if event.type == pygame.QUIT:
                sys.exit()
            # Checks if the player has pressed
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Allows the player to drag and draw walls
                drag = True
                mouse = pygame.mouse.get_pos()
                # Checks if the simulation is ready
                ready = screen.checkClick(mouse[0], mouse[1])
            # Checks if the player has lifted the mouse and therefore stopped dragging
            if event.type == pygame.MOUSEBUTTONUP:
                drag = False
            # Checks if the player is dragging and drawing
            if event.type == pygame.MOUSEMOTION and drag:
                mouse = pygame.mouse.get_pos()
                ready = screen.checkClick(mouse[0], mouse[1])

        # If the simulation is ready
        if ready:
            # Checks if the button was just pressed
            if firstRun:
                # Will create an algorithm object
                firstRun = False
                algorithm = aStar.aStar(screen.startFlagLocation, screen.endFlagLocation, screen.wallLocations)
            # Gets the result of each calculation
            result, done = algorithm.calculate()
            # If a list is returned, draw the solution
            if type(result) == list:
                screen.drawSolution(result, done)
            # Else end the simulation
            else:
                done = True
            if done:
                ready = False

