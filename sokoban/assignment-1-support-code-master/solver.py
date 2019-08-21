import random
import sys
import copy
#goal state is a box on top of every target
#hash that for quickly checking
#only be concerned where the box goes for each state
    #man can get there it just has a cost to get to that state

#S1 = initial state
#S1 + SELECT and apply a move
    #--> state change?
        #no, SELECT and apply again moves +=1
        #yes, is new state goal state?
            #no, S1 becomes parent
            #select next shortest path to test --> test.


#, repeat until state change or unsolveable
#S2 initial state is it's parent

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
        player_position = None
        for i in range(num_rows):
            for j in range(row_len):
                if rows[i][j] == self.BOX_SYMBOL:
                    box_positions.append((i, j))
                    rows[i][j] = self.FREE_SPACE_SYMBOL
                elif rows[i][j] == self.TGT_SYMBOL:
                    tgt_positions.append((i, j))
                    rows[i][j] = self.FREE_SPACE_SYMBOL
                elif rows[i][j] == self.PLAYER_SYMBOL:
                    player_position = (i, j)
                    rows[i][j] = self.FREE_SPACE_SYMBOL
                elif rows[i][j] == self.BOX_ON_TGT_SYMBOL:
                    box_positions.append((i, j))
                    tgt_positions.append((i, j))
                    rows[i][j] = self.FREE_SPACE_SYMBOL
                elif rows[i][j] == self.PLAYER_ON_TGT_SYMBOL:
                    player_position = (i, j)
                    tgt_positions.append((i, j))
                    rows[i][j] = self.FREE_SPACE_SYMBOL

        assert len(box_positions) == len(tgt_positions), "Number of boxes does not match number of targets"

        self.x_size = row_len
        self.y_size = num_rows
        self.box_positions = box_positions
        self.tgt_positions = tgt_positions
        self.player_position = player_position
        self.player_x = player_position[1]
        self.player_y = player_position[0]
        self.obstacle_map = rows

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

    def search(self):
        """
        :param self:
        :param smap:
        :return:
        """
        root = Node(None, -1, None, self.player_position, self.box_positions)
        key = hash((tuple(sorted(root.box_positions)), root.player_position))
        cost = root.cost
        Node.seen_states.update({key:root})
        add(Node.leaf_states,cost,root)


        #HERE IS WHERE WE INSERT OUR TIME LIMIT AND COUNTERS FOR SEARCH

        # (WHILE GOAL NOT found) OR LEAF EXISTS THAT IS LESS COST THAN SMALLEST REACHED GOAL STATE
        while (len(Node.goals_reached)==0 or
               sorted(Node.leaf_states)[0] < sorted(Node.goals_reached)[0]):

            #POP THE SMALLEST LEAF
            for node in Node.leaf_states.pop(sorted(Node.leaf_states)[0]):
                # MAKE SUCCESSORS
                    node.successor_states = node.next_states(self.obstacle_map,self.tgt_positions)
            #ADD SUCCESSORS TO LEAF (done in next states) OR GOAL REACHED (done in next states)
        #REPEAT TILL SATISFIED

        # get smallest solution node and retrace steps
        key = sorted(Node.goals_reached.keys())[0]
        goal_state = Node.goals_reached.get(key)[0]
        g = Node.goals_reached
        path = []
        path = goal_state.retrace_path()
        return (reversed(path),Node.num_nodes,len(Node.leaf_states),len(Node.seen_states))




        ##make a root state
        ##add state to the list of seen states
        ##find successors
        ##add to those
        ##select shortest




class SokobanMiniMap:

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

    def __init__(self, obstacle_map, player_position, box_positions,tgt_positions):
            """
            constructs a sokoban map without parsing a file
            :param obstacle_map:
            :param player_position:
            :param box_positions:
            """
            self.obstacle_map = obstacle_map
            self.player_position = player_position
            self.player_x = player_position[1]
            self.player_y = player_position[0]
            self.box_positions = list(box_positions)
            self.tgt_positions = tgt_positions

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
                if self.obstacle_map[new_y][new_x - 1] == self.OBSTACLE_SYMBOL or (
                        new_y, new_x - 1) in self.box_positions:
                    return False
                else:
                    new_box_x = new_x - 1
                    new_box_y = new_y

            elif move == self.RIGHT:
                if self.obstacle_map[new_y][new_x + 1] == self.OBSTACLE_SYMBOL or (
                        new_y, new_x + 1) in self.box_positions:
                    return False
                else:
                    new_box_x = new_x + 1
                    new_box_y = new_y

            elif move == self.UP:
                if self.obstacle_map[new_y - 1][new_x] == self.OBSTACLE_SYMBOL or (
                        new_y - 1, new_x) in self.box_positions:
                    return False
                else:
                    new_box_x = new_x
                    new_box_y = new_y - 1

            else:
                if self.obstacle_map[new_y + 1][new_x] == self.OBSTACLE_SYMBOL or (
                        new_y + 1, new_x) in self.box_positions:
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
        self.player_position = (self.player_y, self.player_x)
        return True


class Node:

    def __repr__(self):
        return print("box: % player: %" % self.box_positions, self.player_position)

    seen_states = {} # where we hash and keep our seen states
    leaf_states = {} # where we search for our shortest path to check next
    goals_reached = {} #where we store the reached goal state and their costs
    num_nodes = 0
    moves = ['u', 'r', 'd', 'l']

    def __init__(self, parent_state, cost_till_now, dir_taken_to_here_from_parent, player_position, box_positions):
        self.parent_state = parent_state
        self.cost = cost_till_now + 1
        self.dir_to_here = dir_taken_to_here_from_parent #u,d,l,r
        self.box_positions = list(box_positions)
        self.player_position = tuple(player_position) #this is the current location also that decides where it can be moved to
        ##targets remain in same place in map
        self.successor_states = []
        Node.num_nodes = Node.num_nodes+1


    def test_state_is_goal(self,smap):
            finished = True
            for i in self.box_positions:
                if i not in smap.tgt_positions:
                    finished = False
            return finished

    def make_minimap(self, obstacle_map, player_position, box_positions,tgt_positions):
        """
        used with the apply_move from sokoban map to determine if it is a valid move.
        :param obstacle_map:
        :param player_position:
        :param big_map: a sokobanMap
        :return: a modified sokobanmap that does not read file input
        """
        smap = SokobanMiniMap(obstacle_map, player_position, box_positions,tgt_positions)
        return smap

    def next_states(self, obstacle_map,tgt_positions):
        """
        a state tells you it's possible next states (adjacent squares that haven't been a visited state)
        :return:
        """


        successors = []
        ##UCS --> next state is just neighbours. Costs are uniform so we don't care which way we go

        # compute next states by applying a move to the map that moves the player to a non-visited node
        # visited and non-visited nodes are held in the SokobanMap?

        current_map = self.make_minimap(obstacle_map, self.player_position, self.box_positions, tgt_positions)
        for move in self.moves: #they're all equally weighted by cost

            ##select the state with lowest move cost and do it first (already done prior to here)
            next_map = self.make_minimap(obstacle_map, current_map.player_position, current_map.box_positions, tgt_positions)

            if next_map.apply_move(move): ##false if invalid --> terminate that path
                ##create new state if not exists in list of exisiting states
                new_state = Node(self,self.cost,move,next_map.player_position,next_map.box_positions)
                if new_state.test_state_is_goal(next_map):

                    ##if it's the lowest cost solution it wins if all leafs are empty or longer
                    cost= new_state.cost
                    add(Node.goals_reached,cost, new_state)
                    continue

                ##if new_state in set of existing states, is it less than the other state? Yes? Replace
                key = hash((tuple(sorted(new_state.box_positions)), new_state.player_position))
                if key in Node.seen_states:
                    continue
                    #we've been here before, we did it quicker or we got a hash collision but whatever
                    ##if we did, is this state already a leaf? --> not possible for UCS
                        #if so, replace leaf and seen value
                        #else, replace seen
                else:
                    cost= new_state.cost
                    add(Node.leaf_states,cost,new_state)
                    Node.seen_states.update({key:new_state})
                    successors.append(new_state)

        return successors

    def retrace_path(self):
        path = []
        self.retrace_recursively(self,path)
        return path

    def retrace_recursively(self,node,path):
        if node.parent_state is None:
            return
        path.append(node.dir_to_here)
        node.retrace_recursively(node.parent_state,path)


#helper hashmap builder basically because we aint got no good tree traversal
def add(dictionary, key, values):
    info = dictionary.get(key, [])
    info.append(values)
    dictionary[key] = info


def main(arglist):
        """
        Run a playable game of Sokoban using the given filename as the map file.
        :param arglist: map file name
        """
        map_inst = SokobanMap(arglist[0])
        map_inst.render()
        steps = 0
        solution = map_inst.search()
        for move in solution[0]:
            map_inst.apply_move(move)
            steps += 1
            print(str(move))
            map_inst.render()



        if map_inst.is_finished():
            print("Puzzle solved in " + str(steps) + " steps!")
        return

if __name__ == '__main__':
    main(['testcases/2box_m1.txt'])


