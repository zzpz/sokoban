import sys
import time


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
        # dead positions
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

    def asearch(self):
        ##calculate all those heuristic values
        root = Node(None,-1,None,self.player_position,self.box_positions)
        key = hash((tuple(sorted(root.box_positions)), root.player_position))
        root.heuristic(self.tgt_positions)
        cost = root.cost
        Node.seen_states.update({key:root})
        add(Node.leaf_states,cost,root)


        # (WHILE GOAL NOT found) OR LEAF EXISTS THAT IS LESS COST THAN SMALLEST REACHED GOAL STATE
        while (len(Node.goals_reached)==0 or
               sorted(Node.leaf_states)[0] < sorted(Node.goals_reached)[0]):

            #POP THE SMALLEST LEAF
            for node in Node.leaf_states.pop(sorted(Node.leaf_states)[0]):
                # MAKE SUCCESSORS
                    node.successor_states = node.anext_states(self.obstacle_map,self.tgt_positions,self.obstacle_positions,self.dead_positions)
            #ADD SUCCESSORS TO LEAF (done in next states) OR GOAL REACHED (done in next states)
        #REPEAT TILL SATISFIED

        # get smallest solution node and retrace steps
        key = sorted(Node.goals_reached.keys())[0]
        goal_state = Node.goals_reached.get(key)[0]
        g = Node.goals_reached
        path = []
        path = goal_state.retrace_path()
        leaves = root.leaf_count()
        return (reversed(path),
                Node.num_nodes,
                len(Node.leaf_states),
                len(Node.seen_states),
                leaves)






    def search(self):
        """
        :param self:
        :param smap:
        :return:
        """
        player_pos = list(self.player_position)
        box_pos = list(self.box_positions)
        root = Node(None, -1, None, player_pos, box_pos)
        key = hash((tuple(sorted(root.box_positions)), root.player_position))
        cost = root.cost
        Node.seen_states.update({key:root})
        add(Node.leaf_states,cost,root)


        # (WHILE GOAL NOT found) OR LEAF EXISTS THAT IS LESS COST THAN SMALLEST REACHED GOAL STATE
        while (len(Node.goals_reached)==0 or
               (len((Node.leaf_states)) != 0 and sorted(Node.leaf_states)[0] < sorted(Node.goals_reached)[0])):

            #POP THE SMALLEST LEAF
            for node in Node.leaf_states.pop(sorted(Node.leaf_states)[0]):
                # MAKE SUCCESSORS
                    node.successor_states = node.next_states(self.obstacle_map,self.tgt_positions,self.obstacle_positions,self.dead_positions)
            #ADD SUCCESSORS TO LEAF (done in next states) OR GOAL REACHED (done in next states)
        #REPEAT TILL SATISFIED

        # get smallest solution node and retrace steps
        key = sorted(Node.goals_reached.keys())[0]
        goal_state = Node.goals_reached.get(key)[0]
        g = Node.goals_reached
        path = []
        path = goal_state.retrace_path()
        leaves = root.leaf_count()
        return (reversed(path),
                Node.num_nodes,
                len(Node.leaf_states),
                len(Node.seen_states),
                leaves)




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

    def __init__(self, obstacle_map, player_position, box_positions,tgt_positions,obstacle_positions,dead_positions):
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
            self.obstacle_positions = obstacle_positions
            # self.obstacle_positions_x = obstacle_positions_x
            # self.obstacle_positions_y = obstacle_positions_y
            self.dead_positions = list(dead_positions)

    def apply_move(self, move):
        """
        Apply a player move to the map.
        :param move: 'L', 'R', 'U' or 'D'
        :return: True if move was successful, false if move could not be completed
        """

        if self.check_map_dead_zone():
            return False
        # if self.check_box_dead_zone(): invalid. immediately fails on 4box_m2
        #     return False

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

    """
    Check if the boxes have created a 'dead-zone' and the game is over
    @:return True if the game is over
    """
    def check_box_dead_zone(self):
        # If 2 boxes are next to each other and both against the same wall then no move can be made
        #####
        for box in self.box_positions:
            a = (box[0]+1,box[1])
            b = (box[0]-1,box[1])
            if a in self.box_positions or b in self.box_positions:
                for obstacle in self.obstacle_positions:
                    c = (obstacle[0]+1,obstacle[1])
                    d = (obstacle[0]-1,obstacle[1])
                    if c in self.obstacle_positions or d in self.obstacle_positions:
                        if box in self.tgt_positions:
                            return False
                        else:
                            return True
            for box in self.box_positions:
                a = (box[0], box[1]+1)
                b = (box[0], box[1]-1)
                if a in self.box_positions or b in self.box_positions:
                    for obstacle in self.obstacle_positions:
                        c = (obstacle[0], obstacle[1]+1)
                        d = (obstacle[0], obstacle[1]-1)
                        if c in self.obstacle_positions or d in self.obstacle_positions:
                            if box in self.tgt_positions:
                                return False
                            else:
                                return True
            # if self.box_positions.__contains__((y-1, x)) or \
            #         self.box_positions.__contains__((y + 1, x)):
            #     if self.obstacle_positions.__contains__((y, x - 1)) or \
            #             self.obstacle_positions.__contains__((y, x + 1)):
            #         if self.tgt_positions.__contains__((y, x)):
            #             return False
            #         else:
            #             return True
            # if self.box_positions.__contains__((y, x - 1)) or \
            #         self.box_positions.__contains__((y, x + 1)):
            #     if self.obstacle_positions.__contains__((y - 1, x)) or \
            #             self.obstacle_positions.__contains__((y + 1, x)):
            #         if self.tgt_positions.__contains__((y, x)):
            #             return False
            #         else:
            #             return True

class Node:

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

    def make_minimap(self, obstacle_map, player_position, box_positions,tgt_positions,obstacle_positions,dead_positions):
        """
        used with the apply_move from sokoban map to determine if it is a valid move.
        :param obstacle_map:
        :param player_position:
        :param big_map: a sokobanMap
        :return: a modified sokobanmap that does not read file input
        """
        smap = SokobanMiniMap(obstacle_map, player_position, box_positions,tgt_positions,obstacle_positions,dead_positions)
        return smap

    def next_states(self, obstacle_map,tgt_positions,obstacle_positions,dead_positions):
        """
        a state tells you it's possible next states (adjacent squares that haven't been a visited state)
        :return:
        """


        successors = []
        ##UCS --> next state is just neighbours. Costs are uniform so we don't care which way we go

        # compute next states by applying a move to the map that moves the player to a non-visited node
        # visited and non-visited nodes are held in the SokobanMap?

        current_map = self.make_minimap(obstacle_map, self.player_position, self.box_positions, tgt_positions,obstacle_positions,dead_positions)
        for move in self.moves: #they're all equally weighted by cost

            ##select the state with lowest move cost and do it first (already done prior to here)
            next_map = self.make_minimap(obstacle_map, current_map.player_position, current_map.box_positions, tgt_positions,obstacle_positions,dead_positions)

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

    def anext_states(self,obstacle_map,tgt_positions,obstacle_positions,dead_positions):
        """
               a state tells you it's possible next states (adjacent squares that haven't been a visited state)
               :return:
               """

        successors = []
        ##UCS --> next state is just neighbours. Costs are uniform so we don't care which way we go

        # compute next states by applying a move to the map that moves the player to a non-visited node
        # visited and non-visited nodes are held in the SokobanMap?

        current_map = self.make_minimap(obstacle_map, self.player_position, self.box_positions, tgt_positions,obstacle_positions,dead_positions)
        for move in self.moves:  # they're all equally weighted by cost but the node they land on will have a heuristic

            ##select the state with lowest move cost and do it first (already done prior to here)
            next_map = self.make_minimap(obstacle_map, current_map.player_position, current_map.box_positions,
                                         tgt_positions,obstacle_positions,dead_positions)

            if next_map.apply_move(move):  ##false if invalid --> terminate that path
                ##create new state if not exists in list of exisiting states
                new_state = Node(self, self.cost, move, next_map.player_position, next_map.box_positions)
                new_state.heuristic(tgt_positions) #update's its cost
                if new_state.test_state_is_goal(next_map):
                    ##if it's the lowest cost solution it wins if all leafs are empty or longer
                    cost = new_state.cost
                    add(Node.goals_reached, cost, new_state)
                    continue

                ##if new_state in set of existing states, is it less than the other state? Yes? Replace
                key = ((tuple(sorted(new_state.box_positions)), new_state.player_position))
                if key in Node.seen_states:
                    continue
                    # we've been here before, we did it quicker or we got a hash collision but whatever
                    ##if we did, is this state already a leaf? --> not possible for UCS
                    # if so, replace leaf and seen value
                    # else, replace seen
                else:
                    cost = new_state.cost
                    add(Node.leaf_states, cost, new_state)
                    Node.seen_states.update({key: new_state})
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

    def leaf_count(self):
        blood_on_leaves = 0 #yahndi
        for node in Node.seen_states.values():
            if len(node.successor_states) == 0:
                blood_on_leaves +=1
        return blood_on_leaves

    def heuristic(self, tgt_positions):
        """
        heuristic is the manhattan distance to the nearest target position from a square.
        playerposition is its current position because
        player has moved onto it.
        """
        heuristic = []
        for target in tgt_positions:
            diffy = self.player_position[0] - target[0]  # (x1-x2 , y1-y2) --> (x3,y3)
            diffx = self.player_position[1] - target[1]
            heuristic.append((abs(diffy)+abs(diffx)))
        self.cost += min(heuristic)



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
        start = time.time()
        search = ''
        if True:
            solution = map_inst.search()
            search = 'UCS'
        else:
            solution = map_inst.asearch()
            search = 'A*'

        end = time.time()
        print_sol = []
        num_nodes = solution[1]
        num_leaves = solution[4]
        for move in solution[0]:
            print_sol.append(str(move))
            map_inst.apply_move(move)
            steps += 1

        map_inst.render() #finished
        timeyboy = end-start

        # if map_inst.is_finished():
        #     print("--------------------------------------------")
        #     print("%s %s => Steps: %d || Nodes: %d || Leaves: %d || Time: %3.6f seconds"%(search,str(arglist[0]),steps,num_nodes,num_leaves,timeyboy))
        #     print("Solution:" + str(print_sol))


        ##manually include write out
        if True:
            w = open(arglist[1],'a')
            s = str(print_sol)+"\n"
            s2 = ("%d,%d,not tracked,%3.6f\n" %(num_nodes,num_leaves,timeyboy,))
            w.write(s)
            w.write(s2)

            w.close()

        return

if __name__ == '__main__':
    main(sys.argv[1:])

# Python ProgramName.py inputFileName outputFileName