from collections import namedtuple

Point = namedtuple('Point', 'x,y')


class Astar(object):
    """
    Abstract implementation of AStar search
    """

    # heuristic
    def heuristic(self, node):
        """
        Heuristic of this node (it's cost)
        :param node:
        :return:
        """
        raise NotImplementedError

    # findPath(self,start,end)

    def findPath(self, start, end):
        """
        Find a path from start node to end node, if path not found raise exception else return path.
        :param start: Starting node
        :param end: Ending node
        :return: path if exists else raise error
        """
        ###list of open nodes
        ###list of closed / searched nodes
        ###method to check open/closed
        raise NotImplementedError

    ###helper functions for finding path
    # is end?
    def isEnd(self, node, end):
        """
        Determine if the node is the end node
        :param node:
        :return:
        """
        raise NotImplementedError

    ##buildPath
    def retrace_path(self, start, end, closed_set):
        """
        Take the closedlist
        :param start:
        :param end:
        :param closed_set:
        :return:
        """
        raise NotImplementedError

    def reparent(self, node):
        """
        Reparents a node if necessary.
        :param node:
        :return:
        """
        raise NotImplementedError

    # neighbours
    def neighbours(self, node):
        """
        Returns all neighbours of the supplied node
        :param node:
        :return:
        """
        raise NotImplementedError


class AStarNode(object):
    """
    Class implementing a node for use in A* search.
    """

    def __init__(self):
        """
        Constructor. Initialises h,g,f,parent to none
        """
        self.h = 0
        self.g = 0
        self.f = 0
        self.parent = None

    def calculate_move_cost(self, node):
        """
        Calculates cost to move from this node to target node --> 1 + the parent's move cost
        :param node: target node
        :return: move_cost
        """
        raise NotImplementedError


    def calculate_heuristic(self, goal_node):
        """
        Calculates the heuristic of from this node to target node
        :param goal_node: the target node
        :return: heuristic for node in nodes: node.h = node.calculate_heuristic(goal_node)
        """
        raise NotImplementedError

    def __hash__(self):
        """
        Hash function for use in equivalency check if this node has already been visited
        """
        raise NotImplementedError

    def __eq__(self, node):
        """
        determine if this node is equivalent to another node
        :param node: other node
        :return: true if equal false if not
        """
        raise NotImplementedError


class AstarGridNode(AStarNode):

    def __init__(self, xyPoint, parent, h, g, f):
        """
        Concrete constructor of an AStarNode for use within AStarGrid
        :param xy: a namedTuple 'Point' containing the x,y co-ords of the node
        """
        self.xy = xyPoint
        self.directions = [Point(0, +1), Point(+1, 0), Point(0, -1), Point(-1, 0)]
        self.parent = parent
        self.h = h
        self.g = g
        self.f = f

    def move_cost(self, direction, to_node):
        """
        movement cost between any two adjacent nodes should be one if L/R else 2 if diagonal
        :param to_node: the node to be moved to
        :param direction: the direction of the to node
        :return: int move cost
        """
        raise NotImplementedError

    def move_cost(self, to_node):
        """

        :param to_node:
        :return:
        """
        return 1 + self.parent.g

    def parent(self, node):
        """
        Make the supplied node the parent of this node.
        :param node:
        :return:
        """

    def get_parent(self):
        """
        Return the parent node of this node, return None if not exists
        :return:
        """

    def __hash__(self):
        pass

    def __eq__(self, node):
        pass


class AStarSoko(Astar):

    #visited list
    #unvisited list ==> literally everyone
    #???

    def reparent(self, node):
        pass

    def __init__(self, sokoban_map):
        self.smap = sokoban_map

    def heuristic(self, node):
        """
        Manhattan distance from the search's target/end node.
        :param node: target node
        :return: the manhattan distance from the search's target/end node to the provided node.
        """
        # manhattan = sum abs difference X + abs difference Y
        diff = node.xy - self.end.xy  # (x1-x2 , y1-y2) --> (x3,y3)
        return abs(diff.x) + abs(diff.y) #for node in sokoMap --> node.h = AStarSoko.heuristic(

    def neighbours(self, node):
        """
        Returns
        :param node:
        :return:
        """
        neighbours = []
        for direction in self.directions:  ## node holds the possible directions u,r,d,l
            xy = node.xy + direction
            if xy in self.grid:
                neighbours.append(AstarGridNode(xy))
        return neighbours
        pass

    def findPath(self, start, end):
        """
        A* Search the map. If no path return None else return path.
        :param start: initial node
        :param end: end node
        :return: an iterable of movement commands specifying the u,d,r,l path from start to end.
        """

        #need open set/list/tree --> BST probably best
        #closed set/list/tree
        #start
        pass

    def isEnd(self, node, end): #goal reached
        pass

    def buildPath(self, start, end, closeList):
        pass