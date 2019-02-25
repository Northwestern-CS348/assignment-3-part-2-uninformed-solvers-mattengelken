from solver import *
from queue import *


class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.
        Returns:
            True if the desired solution state is reached, False otherwise
        """
        if self.currentState.state == self.victoryCondition:
            return True

        if self.gm.getMovables():
            for move in self.gm.getMovables():
                self.gm.makeMove(move)
                child = GameState(self.gm.getGameState(), self.currentState.depth + 1, move)
                self.currentState.children.append(child)
                child.parent = self.currentState
                self.gm.reverseMove(move)
            for child in self.currentState.children:
                if child not in self.visited:
                    self.visited[child] = True
                    depth = self.currentState.depth + 1
                    self.currentState = child
                    self.currentState.depth = depth
                    self.gm.makeMove(child.requiredMovable)
                    break
        else:
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent

        return False


class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    q = Queue()
    moves = 0

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.
        Returns:
            True if the desired solution state is reached, False otherwise
        """
        if self.currentState.state == self.victoryCondition:
            if not self.q.empty():
                while not self.q.empty():
                    self.q.get()
            return True

        if self.gm.getMovables():
            for move in self.gm.getMovables():
                self.gm.makeMove(move)
                child = GameState(self.gm.getGameState(), 0, move)
                self.currentState.children.append(child)
                child.parent = self.currentState
                self.gm.reverseMove(move)

        for child in self.currentState.children:
            if child not in self.visited:
                self.q.put(child)

        while not self.q.empty():
            child = self.q.get()
            if child not in self.visited:
                state = self.currentState
                pathtoroot = []
                while state.requiredMovable:
                    pathtoroot.append(state.requiredMovable)
                    state = state.parent

                state = child
                pathtochild = []
                while state.requiredMovable:
                    pathtochild.append(state.requiredMovable)
                    state = state.parent
                pathtochild = reversed(pathtochild)

                for move in pathtoroot:
                    self.gm.reverseMove(move)
                for move in pathtochild:
                    self.gm.makeMove(move)

                self.currentState = child
                self.visited[child] = True
                self.moves += 1
                self.currentState.depth = self.moves
                break

        return False
