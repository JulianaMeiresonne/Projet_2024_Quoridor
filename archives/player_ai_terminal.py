# The game state is state = {"players": players, "current": 0, "board": [None] * 16, "piece": None}
# None is stored for empty cell
# 0 is stored for 'LUR' (player 1)
# 1 is stored for 'FKY' (player 2)
import copy
import time
from collections import defaultdict

def timeit(fun):
    def wrapper(*args, **kwargs):
        start = time.time()
        res = fun(*args, **kwargs)
        print('Executed in {}s'.format(time.time() - start))
        return res
    return wrapper

def same(L):
    if None in L:
        return False
    common = set(L[0])
    for elem in L[1:]:
        common &= set(elem)
    return len(common) > 0

def getLine(board, i):
    return board[i * 4: (i + 1) * 4]

def getColumn(board, j):
    return [board[i] for i in range(j, 16, 4)]

def getDiagonal(board, dir):
    start = 0 if dir == 1 else 3
    return [board[start + i * (4 + dir)] for i in range(4)]

def isWinning(board):
    for i in range(4):
        if same(getLine(board, i)) or same(getColumn(board, i)):
            return True
    return same(getDiagonal(board, 1)) or same(getDiagonal(board, -1))

def isFull(board):
    return all(elem is not None for elem in board)

def gameOver(state):
    return isWinning(state['board']) or isFull(state['board'])

def Quarto(players):
    if len(players) != 2:
        raise ValueError("Quarto must be played by 2 players")

    pieces = set()
    for s in "BS":
        for c in "DL":
            for w in "EF":
                for sh in "CP":
                    pieces.add(frozenset({s, c, w, sh}))

    state = {
        "players": players,
        "current": 0,
        "board": [None] * 16,
        "piece": None,
        "pieces": pieces
    }

    def next(state, move):
        newState = copy.deepcopy(state)

        if state["piece"] is not None:
            pos = move.get("pos")
            if pos is None or not (0 <= pos < 16) or state["board"][pos] is not None:
                raise ValueError("Invalid move position")
            newState["board"][pos] = state["piece"]
            if isWinning(newState["board"]):
                raise TimeoutError
            if isFull(newState["board"]):
                print(newState, "Draw")

        piece_str = move.get("piece")
        if not isinstance(piece_str, str):
            raise ValueError("Move['piece'] must be a string")
        piece = frozenset(piece_str)
        if piece not in newState["pieces"]:
            raise ValueError(f"Piece '{piece_str}' not available")

        newState["piece"] = piece_str
        newState["current"] = (state["current"] + 1) % 2
        newState["pieces"].remove(piece)
        return newState

    return state, next

def show(board):
    for i in range(4):
        print(getLine(board, i))

def moves(game_board, piece):
    all_pieces = [f"{s}{c}{w}{sh}" for s in "BS" for c in "DL" for w in "EF" for sh in "CP"]
    used_pieces = [p for p in game_board if p is not None]
    available_pieces = [p for p in all_pieces if p not in used_pieces and p != piece]
    positions = [i for i, val in enumerate(game_board) if val is None]
    result = {}
    nb = 0
    for pos in positions:
        for p in available_pieces:
            nb += 1
            result[nb] = {"pos": pos, "piece": p}
    return result

def apply(state, move):
    newState = copy.deepcopy(state)
    newState["board"][move["pos"]] = state["piece"]
    newState["piece"] = move["piece"]
    newState["current"] = (state["current"] + 1) % 2
    return newState

def fill_Lines(board):
    lines = [getDiagonal(board, 1), getDiagonal(board, -1)]
    for i in range(4):
        lines.append(getLine(board, i))
        lines.append(getColumn(board, i))
    return lines

def lineValue(line):
    if None in line:
        return 0
    common = set(line[0])
    for elem in line[1:]:
        common &= set(elem)
    return 1 if common else 0

def heuristic(state, player):
    if isWinning(state["board"]):
        return 9 if state["players"][state["current"]] == player else -9
    return sum(lineValue(line) for line in fill_Lines(state["board"]))

@timeit
def negamaxWithPruningIterativeDeepening(state, player, timeout=0.03):
	cache = defaultdict(lambda : 0)
	def cachedNegamaxWithPruningLimitedDepth(state, player, depth, alpha=float('-inf'), beta=float('inf')):
		over = gameOver(state)
		if over or depth == 0:
			res = -heuristic(state, player), None, over

		else:
			theValue, theMove, theOver = float('-inf'), None, True
			possibilities = [(move, apply(state, move)) for move in moves(state["board"],state['piece'] ).values()]
			possibilities.sort(key=lambda poss: cache[tuple(poss[1])])
			for move, successor in reversed(possibilities):
				value, _, over = cachedNegamaxWithPruningLimitedDepth(successor, state["current"]%2+1, depth-1, -beta, -alpha)
				theOver = theOver and over
				if value > theValue:
					theValue, theMove = value, move
				alpha = max(alpha, theValue)
				if alpha >= beta:
					break
			res = -theValue, theMove, theOver
		cache[tuple(state)] = res[0]
		return res

	value, move = 0, None
	depth = 1
	start = time.time()
	over = False
	while value > -9 and time.time() - start < timeout and not over:
		value, move, over = cachedNegamaxWithPruningLimitedDepth(state, player, depth)
		depth += 1

	return value, move

# MAIN

state, next = Quarto(["LUR", "FKY"])
try:
    while True:
        show(state["board"])
        print(f"Piece: {state['piece']}")
        print(f"Player: {state['players'][state['current']]}")

        _, move_ai = negamaxWithPruningIterativeDeepening(state, state['players'][state['current']])
        if move_ai is None:
            print("No moves possible!")
            break
        state = next(state, move_ai)

except TimeoutError:
    show(state["board"])
    print(f"{state['players'][state['current']]} wins the game!")

