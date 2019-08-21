import sys
from collections import namedtuple

Point = namedtuple('Point', 'x,y')
ai = False


class SokobanMap:
    """
    Instance of a Sokoban game map. You may use this class and its functions
    directly or duplicate and modify it in your solution. You should avoid
    modifying this file directly.

    COMP3702 2019 Assignment 1 Support Code

    Last updated by njc 11/08/19
    """

    # input file symbols
    BOX_SYMBOL = 'B'
    TGT_SYMBOL = 'T'
    PLAYER_SYMBOL = 'P'
    OBSTACLE_SYMBOL = '#'
    FREE_SPACE_SYMBOL = ' '
    BOX_ON_TGT_SYMBOL = 'b'
    PLAYER_ON_TGT_SYMBOL = 'p'

    # move symbols (i.e. output file symbols)
    LEFT = 'l'
    RIGHT = 'r'
    UP = 'u'
    DOWN = 'd'

    # render characters
    FREE_GLYPH = '   '
    OBST_GLYPH = 'XXX'
    BOX_GLYPH = '[B]'
    TGT_GLYPH = '(T)'
    PLAYER_GLYPH = '<P>'

    def __init__(self, filename):
        """
        Build a Sokoban map instance from the given file name
        :param filename:
        """
        f = open(filename, 'r')

        rows = []
        for line in f:
            if len(line.strip()) > 0:
                rows.append(list(line.strip()))

        f.close()

        row_len = len(rows[0])
        for row in rows:
            assert len(row) == row_len, "Mismatch in row length"

        num_rows = len(rows)

        box_positions = []
        tgt_positions = []
        dead_positions = []
        # All obstacle positions
        obstacle_positions = []
        # Obstacle positions by row and column
        obstacle_positions_x = []
        obstacle_positions_y = []
        player_position = None

        for i in range(num_rows):
            # Trying to get the deadzones on walls
            # Positions of obstacles by row and column
            obstacle_positions_row = []
            obstacle_positions_column = []
            obstacle_positions_x.append(obstacle_positions_row)
            obstacle_positions_y.append(obstacle_positions_column)

            for j in range(row_len):

                if rows[i][j] == self.BOX_SYMBOL:
                    box_positions.append((i, j))
                    rows[i][j] = self.FREE_SPACE_SYMBOL

                elif rows[i][j] == self.TGT_SYMBOL:
                    tgt_positions.append((i, j))
                    rows[i][j] = self.FREE_SPACE_SYMBOL

                elif rows[i][j] == self.PLAYER_SYMBOL:
                    player_position = (i, j)

                    # Check if player start is possible dead zone
                    # Corner deadzone
                    if rows[i][j - 1] == self.OBSTACLE_SYMBOL or rows[i][j + 1] == self.OBSTACLE_SYMBOL:
                        if rows[i - 1][j] == self.OBSTACLE_SYMBOL or rows[i + 1][j] == self.OBSTACLE_SYMBOL:
                            dead_positions.append((i, j))
                    rows[i][j] = self.FREE_SPACE_SYMBOL

                elif rows[i][j] == self.BOX_ON_TGT_SYMBOL:
                    box_positions.append((i, j))
                    tgt_positions.append((i, j))
                    rows[i][j] = self.FREE_SPACE_SYMBOL

                elif rows[i][j] == self.PLAYER_ON_TGT_SYMBOL:
                    player_position = (i, j)
                    tgt_positions.append((i, j))
                    rows[i][j] = self.FREE_SPACE_SYMBOL

                    # Check for "deadzones" from map layout and add to list
                    # Corner deadzones
                elif rows[i][j] == self.FREE_SPACE_SYMBOL:
                    if rows[i][j - 1] == self.OBSTACLE_SYMBOL or rows[i][j + 1] == self.OBSTACLE_SYMBOL:
                        if rows[i - 1][j] == self.OBSTACLE_SYMBOL or rows[i + 1][j] == self.OBSTACLE_SYMBOL:
                            dead_positions.append((i, j))

                elif rows[i][j] == self.OBSTACLE_SYMBOL:
                    obstacle_positions.append((i, j))
                    obstacle_positions_row.append((i, j))
                    obstacle_positions_column.append((j, i))

        print(dead_positions)



        assert len(box_positions) == len(tgt_positions), "Number of boxes does not match number of targets"

        self.x_size = row_len
        self.y_size = num_rows
        self.box_positions = box_positions
        self.tgt_positions = tgt_positions
        self.player_position = player_position
        self.player_x = player_position[1]
        self.player_y = player_position[0]
        self.obstacle_map = rows
        self.obstacle_positions = obstacle_positions
        self.obstacle_positions_x = obstacle_positions_x
        self.obstacle_positions_y = obstacle_positions_y
        self.dead_positions = dead_positions
        print(self.dead_positions)
        print(self.tgt_positions)

    def search(self, obstacle_map, player_position, dead_positions,search):
        return False


    def apply_move(self, move):
        """
        Apply a player move to the map.
        :param move: 'L', 'R', 'U' or 'D'
        :return: True if move was successful, false if move could not be completed
        """
        # basic obstacle check
        if move == self.LEFT:
            if self.obstacle_map[self.player_y][self.player_x - 1] == self.OBSTACLE_SYMBOL:
                return False
            else:
                new_x = self.player_x - 1
                new_y = self.player_y

        elif move == self.RIGHT:
            if self.obstacle_map[self.player_y][self.player_x + 1] == self.OBSTACLE_SYMBOL:
                return False
            else:
                new_x = self.player_x + 1
                new_y = self.player_y

        elif move == self.UP:
            if self.obstacle_map[self.player_y - 1][self.player_x] == self.OBSTACLE_SYMBOL:
                return False
            else:
                new_x = self.player_x
                new_y = self.player_y - 1

        else:
            if self.obstacle_map[self.player_y + 1][self.player_x] == self.OBSTACLE_SYMBOL:
                return False
            else:
                new_x = self.player_x
                new_y = self.player_y + 1

        # pushed box collision check
        if (new_y, new_x) in self.box_positions:
            if move == self.LEFT:
                if self.obstacle_map[new_y][new_x - 1] == self.OBSTACLE_SYMBOL or (new_y, new_x - 1) in self.box_positions:
                    return False
                else:
                    new_box_x = new_x - 1
                    new_box_y = new_y

            elif move == self.RIGHT:
                if self.obstacle_map[new_y][new_x + 1] == self.OBSTACLE_SYMBOL or (new_y, new_x + 1) in self.box_positions:
                    return False
                else:
                    new_box_x = new_x + 1
                    new_box_y = new_y

            elif move == self.UP:
                if self.obstacle_map[new_y - 1][new_x] == self.OBSTACLE_SYMBOL  or (new_y - 1, new_x) in self.box_positions:
                    return False
                else:
                    new_box_x = new_x
                    new_box_y = new_y - 1

            else:
                if self.obstacle_map[new_y + 1][new_x] == self.OBSTACLE_SYMBOL or (new_y + 1, new_x) in self.box_positions:
                    return False
                else:
                    new_box_x = new_x
                    new_box_y = new_y + 1

            # update box position
            self.box_positions.remove((new_y, new_x))
            self.box_positions.append((new_box_y, new_box_x))

        # update player position
        self.player_x = new_x
        self.player_y = new_y

        return True

    """
    Check if the boxes have created a 'dead-zone' and the game is over
    @:return True if the game is over
    """
    def check_box_dead_zone(self):
        # If 2 boxes are next to each other and against the wall then no move can be made
        #####
        for y, x in self.box_positions:
            if self.box_positions.__contains__((y-1, x)) or \
                    self.box_positions.__contains__((y + 1, x)):
                if self.obstacle_positions.__contains__((y, x - 1)) or \
                        self.obstacle_positions.__contains__((y, x + 1)):
                    if self.tgt_positions.__contains__((y, x)):
                        return False
                    else:
                        return True
            if self.box_positions.__contains__((y, x - 1)) or \
                    self.box_positions.__contains__((y, x + 1)):
                if self.obstacle_positions.__contains__((y - 1, x)) or \
                        self.obstacle_positions.__contains__((y + 1, x)):
                    if self.tgt_positions.__contains__((y, x)):
                        return False
                    else:
                        return True


    def wall_dead_zone(self):
            # Trying to implement wall dead zones
        for y, x in self.tgt_positions:
            if not self.obstacle_positions_x[-1].__contains__((y + 1, x)):
                self.add_to_dead_zone(self.obstacle_positions_x[-1])

            if not self.obstacle_positions_x[0].__contains__((y - 1, x)):
                self.add_to_dead_zone(self.obstacle_positions_x[0])

            if not self.obstacle_positions_y[0].__contains__((y, x - 1)):
                self.add_to_dead_zone(self.obstacle_positions_y[0])

            if not self.obstacle_positions_y[-1].__contains__((y, x + 1)):
                self.add_to_dead_zone(self.obstacle_positions_y[-1])

    """
    Check if the box is in a 'dead-zone' from the map positioning
    @:return True if the game is over
    """
    def check_map_dead_zone(self):
        # Corner check
        for i in self.box_positions:
            for j in self.dead_positions:
                if i == j:
                    return True

    def add_to_dead_zone(self, coordinates):
        # Adding coordinates to deadzones
        for y, x in coordinates:
            self.dead_positions.append((y, x))

    def render(self):
        """
        Render the map's current state to terminal
        """
        for r in range(self.y_size):
            line = ''
            for c in range(self.x_size):
                symbol = self.FREE_GLYPH
                if self.obstacle_map[r][c] == self.OBSTACLE_SYMBOL:
                    symbol = self.OBST_GLYPH
                if (r, c) in self.tgt_positions:
                    symbol = self.TGT_GLYPH
                # box or player overwrites tgt
                if (r, c) in self.box_positions:
                    symbol = self.BOX_GLYPH
                if self.player_x == c and self.player_y == r:
                    symbol = self.PLAYER_GLYPH
                line += symbol
            print(line)

        print('\n\n')

    def is_finished(self):
        finished = True
        for i in self.box_positions:
            if i not in self.tgt_positions:
                finished = False
        return finished

def main(arglist):
    """
    Run a playable game of Sokoban using the given filename as the map file.
    :param arglist: map file name
    """
    try:
        import msvcrt
        getchar = msvcrt.getch
    except ImportError:
        getchar = sys.stdin.read(1)

    if len(arglist) != 1:
        print("Running this file directly launches a playable game of Sokoban based on the given map file.")
        print("Usage: sokoban_map.py [map_file_name]")
        return

    print("Use the arrow keys to move. Press 'q' to quit. Press 'r' to restart the map.")

    map_inst = SokobanMap(arglist[0])
    map_inst.render()
    actions = ['d','l','l','u','l','d','d']
    #map_inst.wall_dead_zone()
    #print(dead_positions)

    steps = 0
    if ai:
        for a in actions:
            map_inst.apply_move(a)
            map_inst.render()
            map_inst.check_box_dead_zone()
            # check if the box is in a map dead zone
            if map_inst.check_map_dead_zone():
                print("can not complete/fail")
                return
            if map_inst.check_box_dead_zone():
                print("can not complete/fail")
                return



            steps += 1

            if map_inst.is_finished():
                print("Puzzle solved in " + str(steps) + " steps!")
                return
    else:
        while True:
            char = getchar()

            if char == b'q':
                break

            if char == b'r':
                map_inst = SokobanMap(arglist[0])
                map_inst.render()

                steps = 0

            if char == b'\xe0':
                # got arrow - read direction
                dir = getchar()
                if dir == b'H':
                    a = SokobanMap.UP
                elif dir == b'P':
                    a = SokobanMap.DOWN
                elif dir == b'K':
                    a = SokobanMap.LEFT
                elif dir == b'M':
                    a = SokobanMap.RIGHT
                else:
                    print("!!!error")
                    a = SokobanMap.UP

                map_inst.apply_move(a)
                map_inst.render()
                if map_inst.check_map_dead_zone():
                    print("can not complete/fail")
                    return


                steps += 1

                if map_inst.is_finished():
                    print("Puzzle solved in " + str(steps) + " steps!")
                    return
                if map_inst.check_box_dead_zone():
                    print("can not complete/fail")
                    return


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

if __name__ == '__main__':
    main(sys.argv[1:])







