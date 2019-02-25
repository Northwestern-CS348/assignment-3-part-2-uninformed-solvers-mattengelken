from game_master import GameMaster
from read import *
from util import *


class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.
        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.
        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.
        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))
        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here
        peg1 = []
        peg2 = []
        peg3 = []

        ask1 = parse_input("fact: (on ?disk peg1")
        ask2 = parse_input("fact: (on ?disk peg2")
        ask3 = parse_input("fact: (on ?disk peg3")

        if self.kb.kb_ask(ask1):
            disks = self.kb.kb_ask(ask1).list_of_bindings
            for i in disks:
                disk = (int(i[0].bindings[0].constant.element[4]))
                peg1.append(disk)
        if self.kb.kb_ask(ask2):
            disks = self.kb.kb_ask(ask2).list_of_bindings
            for i in disks:
                disk = (int(i[0].bindings[0].constant.element[4]))
                peg2.append(disk)
        if self.kb.kb_ask(ask3):
            disks = self.kb.kb_ask(ask3).list_of_bindings
            for i in disks:
                disk = (int(i[0].bindings[0].constant.element[4]))
                peg3.append(disk)

        peg1 = tuple(sorted(peg1))
        peg2 = tuple(sorted(peg2))
        peg3 = tuple(sorted(peg3))

        return (peg1, peg2, peg3)

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.
        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)
        Args:
            movable_statement: A Statement object that contains one of the currently viable moves
        Returns:
            None
        """
        disk = movable_statement.terms[0]
        initial = movable_statement.terms[1]
        target = movable_statement.terms[2]

        askontop = parse_input("fact: (ontop %s ?d)" % disk)

        if self.kb.kb_ask(askontop):
            topdisk = (self.kb.kb_ask(askontop).list_of_bindings[0])[0].bindings[0].constant.element
            self.kb.kb_assert(parse_input("fact: (top %s %s)" % (topdisk, initial)))
            self.kb.kb_retract(parse_input("fact: (ontop %s %s)" % (disk, topdisk)))
        else:
            self.kb.kb_assert(parse_input("fact: (empty %s)" % initial))

        askthetop = parse_input("fact: (top ?d %s)" % target)
        if self.kb.kb_ask(askthetop):
            oldtop = (self.kb.kb_ask(askthetop).list_of_bindings[0])[0].bindings[0].constant.element
            self.kb.kb_retract(parse_input("fact: (top %s %s)" % (oldtop, target)))
            self.kb.kb_assert(parse_input("fact: (ontop %s %s)" % (disk, oldtop)))
        if self.kb.kb_ask(parse_input("fact: (empty %s)" % target)):
            self.kb.kb_retract(parse_input("fact: (empty %s)" % target))

        oldpeg = parse_input("fact: (on %s %s)" % (disk, initial))
        self.kb.kb_retract(oldpeg)
        oldtop = parse_input("fact: (top %s %s)" % (disk, initial))
        self.kb.kb_retract(oldtop)

        newpeg = parse_input("fact: (on %s %s)" % (disk, target))
        self.kb.kb_assert(newpeg)
        newtop = parse_input("fact: (top %s %s)" % (disk, target))
        self.kb.kb_assert(newtop)

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.
        Args:
            movable_statement: A Statement object that contains one of the previously viable moves
        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))


class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.
        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.
        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))
        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here
        row1 = ()
        row2 = ()
        row3 = ()

        ask1 = parse_input("fact: (position ?tile ?x 1")
        ask2 = parse_input("fact: (position ?tile ?x 2")
        ask3 = parse_input("fact: (position ?tile ?x 3")


        for i in range(1, 4):
            ask = parse_input("fact: (position ?tile %s 1)" % str(i))
            tile = self.kb.kb_ask(ask)[0].bindings[0].constant.element[4]
            if tile == 'y':
                tile = -1,
            else:
                tile = int(tile),
            row1 = row1 + tile

        for i in range(1, 4):
            ask = parse_input("fact: (position ?tile %s 2)" % str(i))
            tile = self.kb.kb_ask(ask)[0].bindings[0].constant.element[4]
            if tile == 'y':
                tile = -1,
            else:
                tile = int(tile),
            row2 = row2 + tile

        for i in range(1, 4):
            ask = parse_input("fact: (position ?tile %s 3)" % str(i))
            tile = self.kb.kb_ask(ask)[0].bindings[0].constant.element[4]
            if tile == 'y':
                tile = -1,
            else:
                tile = int(tile),
            row3 = row3 + tile
        return row1, row2, row3

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.
        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)
        Args:
            movable_statement: A Statement object that contains one of the currently viable moves
        Returns:
            None
        """
        tile = movable_statement.terms[0]

        x1 = movable_statement.terms[1]
        y1 = movable_statement.terms[2]

        x2 = movable_statement.terms[3]
        y2 = movable_statement.terms[4]

        oldloc = parse_input("fact: (position %s %s %s)" % (tile, x1, y1))
        newloc = parse_input("fact: (position %s %s %s)" % (tile, x2, y2))

        oldempty = parse_input("fact: (position empty %s %s)" % (x2, y2))
        newempty = parse_input("fact: (position empty %s %s)" % (x1, y1))

        self.kb.kb_retract(oldloc)
        self.kb.kb_retract(oldempty)
        self.kb.kb_assert(newempty)
        self.kb.kb_assert(newloc)



    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.
        Args:
            movable_statement: A Statement object that contains one of the previously viable moves
        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
