#!/usr/bin/python3.14
#Made by Conrad Boltz, and Declan Mancilla
import contextlib
import json
try:
    import curses
except ModuleNotFoundError:
    print("curses implementation not found, but required for program")
    if input("install windows-curses from pypi? ('yes' to continue) ") == "yes":
        import subprocess
        import sys
        try:
            subprocess.check_call(['py', '-%d.%d' % (sys.version_info.major, sys.version_info.minor), '-m', 'pip', 'install', 'windows-curses'])
        except CalledProcessError as error:
            print("unable to install; exiting")
            exit(error.returncode)
        # run self as new process
        argv = [sys.executable]
        argv += [*sys.argv] if sys.argv != [""] else []
        returncode = subprocess.run(argv).returncode
        # cleanup by uninstalling windows-curses
        # requires user confirmation by default
        try:
            subprocess.check_call(['py', '-%d.%d' % (sys.version_info.major, sys.version_info.minor), '-m', 'pip', 'uninstall', 'windows-curses'])
        except CalledProcesssError as error:
            print("unable to uninstall; exiting")
            exit(error.returncode)
        exit(returncode)
    else:
        exit()
#Put a do you want to see your stats or play the game here.

#List of Win/Loss/Tie for each name with the name as key to access it and display as pie chart.
#At the end of the game display who wins or if it is a tie.
#After end ask if they want to play another round.

#made by conrad starts
Playing = True
PlayerXWinning = False
PlayerOWinning = False
#Start while loop here
PlayerX = input('What is the name of the first player?')
PlayerO = input('What is the name of the second player?')
Board = ['___','___','___']
PlayerTurn = 'X'
#While playing == true repeat game
#Example of printing the board
#print(Board[0])
#print(Board[1])
#print(Board[2])

#Make sure this part is run after every move
def AreYouWinningSon(): #A giant blob of a if to figure out when someone wins
    global Board,PlayerXWinning,PlayerOWinning
    if Board[0]=='XXX' or Board[1]=='XXX' or Board[2]=='XXX' or (
        Board[0][0]=='X' and Board[1][0]=='X' and Board[2][0]=='X') or (
            Board[0][1]=='X' and Board[1][1]=='X' and Board[2][1]=='X') or (
                Board[0][2]=='X' and Board[1][2]=='X' and Board[2][2]=='X') or (
                    Board[0][0]=='X' and Board[1][1]=='X' and Board[2][2]=='X') or (
                        Board[0][2]=='X' and Board[1][1]=='X' and Board[2][0]=='X'):
        PlayerXWinning = True
    elif Board[0]=='OOO' or Board[1]=='OOO' or Board[2]=='OOO' or (
        Board[0][0]=='O' and Board[1][0]=='O' and Board[2][0]=='O') or (
            Board[0][1]=='O' and Board[1][1]=='O' and Board[2][1]=='O') or (
                Board[0][2]=='O' and Board[1][2]=='O' and Board[2][2]=='O') or (
                    Board[0][0]=='O' and Board[1][1]=='O' and Board[2][2]=='O') or (
                        Board[0][2]=='O' and Board[1][1]=='O' and Board[2][0]=='O'):
        PlayerOWinning = True
#made by conrad ends
TOKENS = {
    13: {
        'x': "╲ ╱ ╳ ╱ ╲",
        'o': "╭─╮│ │╰─╯",
        'grid':1,
    },
    7: {'x': "X", 'o': "O", 'grid':1,},
    3: {'x': "X", 'o': "O", 'grid':0,},
}
DECALS = {
    'vert': "│",
    'horiz': "─",
    'intersect': "┼",
}
SCORES_FORMAT = {"win":0,"loss":0,"draw":0,}

def init(screen):
    global TOKENS, DECALS
    # Get maximum window size
    board_size = min((curses.LINES,curses.COLS))
    while not board_size in TOKENS.keys():
        if board_size <= 0:
            # TODO: support 3x3 terminal
            # should be possible with variable margin size
            raise RuntimeError("Unsupported terminal size")
        board_size -= 1
    # Center board window in viewport
    margin_horizontal = (curses.COLS - board_size) // 2
    margin_vertical = (curses.LINES - board_size) // 2
    boardwin = curses.newwin(board_size, board_size, margin_vertical, margin_horizontal)

    # Populate board with token slots
    padding_size = TOKENS[board_size]['grid']
    tile_size = (board_size - (4 * padding_size)) // 3
    windows = []
    for i in range(3):
        row = []
        for j in range(3):
            # offset = number of previous tiles multiplied by tile size, added to previous tile margins
            row += [curses.newwin(
                tile_size, tile_size,
                margin_vertical + tile_size*i+(1+i)*padding_size,
                margin_horizontal + tile_size*j+(1+j)*padding_size,
            )]
        windows += [row]
    # Decorate board
    for i in range(tile_size + padding_size):
        boardwin.addstr(" " * padding_size + (" " * tile_size + DECALS['vert'] * padding_size) * 2 + " " * tile_size + " " * padding_size)
    if padding_size > 0:
        boardwin.addstr(DECALS['horiz']*padding_size + (DECALS['horiz']*tile_size + DECALS['intersect'])*2 + DECALS['horiz']*tile_size + DECALS['horiz']*padding_size)
    for i in range(tile_size):
        boardwin.addstr(" " * padding_size + (" " * tile_size + DECALS['vert'] * padding_size) * 2 + " " * tile_size + " " * padding_size)
    if padding_size > 0:
        boardwin.addstr(DECALS['horiz'] * padding_size + (DECALS['horiz'] * tile_size + DECALS['intersect']) * 2 + DECALS['horiz'] * tile_size + DECALS['horiz'] * padding_size)
    for i in range(tile_size):
        boardwin.addstr((" " * padding_size + (" " * tile_size + DECALS['vert'] * padding_size) * 2 + " " * tile_size + " " * padding_size))
    if padding_size > 0:
        # python curses limitation: cannot addstr to lower right corner of window
        # workaround: use insstr for the last character
        boardwin.addstr((" " * padding_size + (" " * tile_size + DECALS['vert'] * padding_size) * 2 + " " * tile_size))
        boardwin.insstr(" " * padding_size)
    boardwin.refresh()
    for row in windows:
        for win in row:
            win.noutrefresh()
    curses.doupdate()
    return windows, boardwin

def parse_arrows(window) -> str:
    k = window.getkey()
    if k == "[":
        k = window.getkey()
        match k:
            case "A":
                return curses.KEY_UP
            case "B":
                return curses.KEY_DOWN
            case "C":
                return curses.KEY_RIGHT
            case "D":
                return curses.KEY_LEFT
            case _:
                window.ungetch(k)
                return "["
    return k

def select_move(board, windows, selected: tuple) -> tuple:
    # transforms `selected` (previous selection coordinates) into new coordinates
    y,x = selected
    oldwin = windows[x][y]
    win = oldwin
    oldwin.bkgd(" ",curses.A_REVERSE)
    oldwin.refresh()
    k = board.getkey()
    while not (k in ["\n", " ", curses.KEY_ENTER]):
        if k == "\x1b":
            k = parse_arrows(board)
        oldwin = win
        match k:
            case curses.KEY_UP | "k" | "w":
                x = x-1 if x > 0 else x
            case curses.KEY_DOWN | "j" | "s":
                x = x+1 if x < 2 else x
            case curses.KEY_LEFT | "h" | "a":
                y = y-1 if y > 0 else y
            case curses.KEY_RIGHT | "l" | "d":
                y = y+1 if y < 2 else y
        win = windows[x][y]
        oldwin.bkgd(" ",0)
        oldwin.noutrefresh()
        win.bkgd(" ",curses.A_REVERSE)
        win.noutrefresh()
        curses.doupdate()
        k = board.getkey()
    win.bkgd(" ",0)
    win.refresh()
    return y,x
def update_board(board, windows, state, target):
    global TOKENS, PlayerTurn
    board_size = min(board.getmaxyx())
    win = windows[target[1]][target[0]]
    win.clear()
    win.addstr(TOKENS[board_size][PlayerTurn.lower()][:-1])
    win.insstr(TOKENS[board_size][PlayerTurn.lower()][-1])
    win.refresh()
def start_menu():
    return True

def normalized_score(serialized) -> dict:
    if type(serialized) != dict:
        serialized = {}
    serialized = SCORES_FORMAT | serialized
    for key,value in SCORES_FORMAT.items():
        if type(serialized[key]) != type(value):
            serialized[key] = value
    return serialized

def increment_win(scores, winning, losing):
    for player in winning, losing:
        score = normalized_score(scores.get(player))
        score["win" if player == winning else "loss"] += 1
        scores[player] = score

def increment_draw(scores, player1, player2):
    for player in player1, player2:
        score = normalized_score(scores.get(player))
        score["draw"] += 1
        scores[player] = score

def updated_scores(PlayerX, PlayerO, PlayerXWinning, PlayerOWinning):
    file = None
    scores = {}
    try:
        file = open("scores","r+")
    except FileNotFoundError:
        # make sure someone has created the file
        with contextlib.suppress(FileExistsError):
            file = open("scores", "x")
            file.close()
        file = open("scores","r+")

    try:
        scores = json.loads(file.read())
    except:
        # either a json deserialization error or an io error
        # probably not worth attempting to repair data in either case
        scores = {}
    if not (PlayerXWinning or PlayerOWinning):
        increment_draw(scores, PlayerX, PlayerO)
    if PlayerXWinning:
        increment_win(scores, PlayerX, PlayerO)
    if PlayerOWinning:
        increment_win(scores, PlayerO, PlayerX)
    # write scores back to file
    file.seek(0)
    file.write(json.dumps(scores))
    file.truncate()
    file.close()
    return scores

def main(screen):
    global Playing, PlayerX, PlayerO, Board, PlayerTurn, PlayerXWinning, PlayerOWinning, SCORES_FORMAT
    # supported by most terminals but not guaranteed
    try:
        cursor_style = curses.curs_set(0)
    except:
        cursor_style = -1
    while start_menu():
        screen.noutrefresh()
        windows, board = init(screen)
        selected = {'x': (1,1,), 'o': (1,1,),}
        Playing = True
        PlayerXWinning = False
        PlayerOWinning = False
        Board = ['___','___','___']
        while Playing:
            selected[PlayerTurn.lower()] = select_move(board, windows, selected[PlayerTurn.lower()])
            y,x = selected[PlayerTurn.lower()]
            if Board[y][x] == "_":
                row = list(Board[y])
                row[x] = PlayerTurn
                Board[y] = "".join(row)
                update_board(board, windows, Board, selected[PlayerTurn.lower()])
            AreYouWinningSon()
            if PlayerXWinning or PlayerOWinning or not any(["_" in row for row in Board]):
                Playing = False
            else:
                PlayerTurn = "X" if PlayerTurn == "O" else "O"
        score = updated_scores(PlayerX, PlayerO, PlayerXWinning, PlayerOWinning)
        del windows, board
    if cursor_style >= 0:
        curses.curs_set(cursor_style)
if __name__=="__main__":
    curses.wrapper(main)
