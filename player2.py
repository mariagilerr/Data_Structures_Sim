from __future__ import annotations
from itertools import combinations
from consts import Board, Color, Edge, NUM_NODES


class Player2:
    """
    Implements a winning strategy for the second player in a game of Sim
    """

    @staticmethod
    def get_move(board: Board) -> Edge:
        """
        Return a possible move for the second player (blue) that follows the optimal strategy laid out in the handout,
        given the input board state. If multiple moves are viable, this method can return any of them.
        """
        mini = Player2.get_miniboard(board)
        if mini is None:
            raise ValueError("no miniboard")

        moves = Player2.get_allowed_moves(Color.P2, mini)
        if len(moves) == 1:
            return moves[0]

        sets = Player2.get_maximal_allowed_sets(Color.P2, mini)
        counts = {}
        for e in moves:
            count = 0
            for s in sets:
                if e in s:
                    count += 1
            counts[e] = count

        best = max(counts.values())
        top = []
        for e in counts:
            if counts[e] == best:
                top.append(e)

        if len(top) == 1:
            return top[0]

        p1_sets = Player2.get_maximal_allowed_sets(Color.P1, mini)
        counts2 = {}
        for e in top:
            count = 0
            for s in p1_sets:
                if e in s:
                    count += 1
            counts2[e] = count

        best2 = max(counts2.values())
        for e in counts2:
            if counts2[e] == best2:
                return e

    @staticmethod
    def get_miniboard(board: Board) -> Board | None:
        """
        Return a miniboard from the input board state. If there are multiple miniboards, this method can return any of them.
        """
        R = set()
        for i,j in combinations(range(NUM_NODES),2):
            if board[i][j] == Color.P1 or board[i][j] == Color.P2:
                R.add(i)
                R.add(j)

        mini = [row[:] for row in board]
        for node in range(NUM_NODES):
            if node not in R:
                for k in range(NUM_NODES):
                    mini[node][k] = Color.NONE
                    mini[k][node] = Color.NONE
        if Player2.get_allowed_moves(Color.P2, mini):
            return mini

        for x in range(NUM_NODES):
            if x in R:
                continue
            trial = [row[:] for row in mini]
            for k in R:
                trial[x][k] = Color.UNCOLORED
                trial[k][x] = Color.UNCOLORED
            if Player2.get_allowed_moves(Color.P2, trial):
                return trial
        return None

    @staticmethod
    def get_maximal_allowed_sets(player: Color, board: Board) -> set[frozenset[Edge]]:
        """
        Return a set of all distinct maximal allowed sets for the given player over the input board state.
        If player is Color.P1, find all maximal p1-allowed sets; if player is Color.P2, find all maximal p2-allowed sets.
        """
        candidates = Player2.get_allowed_moves(player, board)
        m = len(candidates)
        for k in range(m,0,-1):
            found = set()
            for candidate_set in combinations(candidates,k):
                test_board = [row[:] for row in board]
                allowed = True
                for edge in candidate_set:
                    if edge not in Player2.get_allowed_moves(player, test_board):
                        allowed = False
                        break
                    i, j = edge
                    test_board[i][j] = player
                    test_board[j][i] = player
                if allowed:
                    found.add(frozenset(candidate_set))
            if found:
                return found
        return set()

    @staticmethod
    def get_allowed_moves(player: Color, board: Board) -> list[Edge]:
        """
        Return a list of all distinct valid moves for the given player over the input board state.
        """
        result = []
        for x,y in combinations(range(NUM_NODES), 2):
            if board[x][y] != Color.UNCOLORED:
                continue
            allowed = True
            for z in range(NUM_NODES):
                if z == x or z == y:
                    continue
                if board[x][z] == board[y][z] == player:
                    allowed = False
            if allowed:
                result.append((x,y))
        return result
