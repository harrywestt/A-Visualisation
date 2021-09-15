import heapq


class aStar:
    def __init__(self, start, stop, walls):
        # Generates the start node, as well as a variable for the location of the walls
        self.startNode = node(position=start, g=0, h=0, f=0)
        self.endNode = node(position=stop, g=0, h=0, f=0)
        self.walls = walls

        # Creates a open and closed list. Open is converted into a heap queue and the start node is added
        self.open = []
        heapq.heapify(self.open)
        heapq.heappush(self.open, self.startNode)
        self.closed = []

    def calculate(self):
        # Checks if the open list is not empty
        if len(self.open) > 0:

            # Sets the current node to be the node with the best f value, adds this to the closed list
            currentNode = heapq.heappop(self.open)
            self.closed.append(currentNode)

            # Checks if the current node is at the end
            if currentNode == self.endNode:
                # Creates a path
                path = []
                current = currentNode
                # Iterates through the nodes backwards and adds them to the list
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                # Returns a reversed path
                return path[::-1], True

            # Creates a temporary list for the children and the nodes to be displayed to the screen
            children = []
            toDisplay = []
            # Iterates over all the 8 possible directions
            for newPosition in [[0, 1], [0, -1], [1, 0], [1, -1], [1, 1], [-1, 0], [-1, 1], [-1, -1]]:
                # Creates a location for the new node
                childNode = [currentNode.position[0] + newPosition[0], currentNode.position[1] + newPosition[1]]
                # Checks if the node is in a valid location
                if not self.isValid(childNode[0], childNode[1]):
                    continue
                # Adds the new node to the toDisplay list and creates a node object and adds it to the children list
                children.append(node(currentNode, childNode))
                toDisplay.append(childNode)

            # Iterates over the children
            for child in children:
                # Checks if any children are already in the closed list
                if len([closedChild for closedChild in self.closed if closedChild == child]) > 0:
                    continue

                # Generates the g, h and f values for the child. Uses euclidean distance formula
                child.g = currentNode.g + 1
                child.h = ((child.position[0] - self.endNode.position[0]) ** 2) + ((child.position[1] - self.endNode.position[1]) ** 2)
                child.f = child.g + child.h

                # Checks if the child is in the open heap with a larger g value
                if len([openNode for openNode in self.open if child.position == openNode.position and child.g >= openNode.g]) > 0:
                    continue

                # Adds the child to the open heap
                heapq.heappush(self.open, child)
            # Returns the children to be displayed to the screen
            return toDisplay, False

        # If nothing is found, the program will print that there is not solution
        print("No path found")
        return None, True

    def isValid(self, x, y):
        # Checks if the new position is in a valid location
        if [x, y] not in self.walls and 30 > y >= 0 and 30 > x >= 0:
            return True
        else:
            return False


class node:
    def __init__(self, parent=None, position=None, g=0, h=0, f=0):
        # Creates a node
        # Generates the parent and the current location
        self.parent = parent
        self.position = position

        self.g = g  # Distance to start
        self.h = h  # Heuristic - estimated distance to the end
        self.f = f  # Total cost of node

    def __eq__(self, other):
        # Changes what self.position is equal to
        return self.position == other.position

    def __gt__(self, other):
        # Allows nodes to be compared for the heap
        return self.f > other.f
