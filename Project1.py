#Made by Conrad Boltz, and Declan Mancilla
import curses

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
                Board[0][3]=='X' and Board[1][3]=='X' and Board[2][3]=='X') or (
                    Board[0][0]=='X' and Board[1][1]=='X' and Board[2][2]=='X') or (
                        Board[0][2]=='X' and Board[1][1]=='X' and Board[2][0]=='X'):
        PlayerXWinning = True
    elif Board[0]=='OOO' or Board[1]=='OOO' or Board[2]=='OOO' or (
        Board[0][0]=='O' and Board[1][0]=='O' and Board[2][0]=='O') or (
            Board[0][1]=='O' and Board[1][1]=='O' and Board[2][1]=='O') or (
                Board[0][3]=='O' and Board[1][3]=='O' and Board[2][3]=='O') or (
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
            token = __import__("random").choice(('o','x'))
            win.addstr(TOKENS[board_size][token][:-1])
            win.insstr(TOKENS[board_size][token][-1])
            win.noutrefresh()
    curses.doupdate()
    return windows, boardwin

def select_move(board, windows, selected):
    x,y = selected
    oldwin = windows[x][y]
    win = oldwin
    oldwin.bkgd(" ",curses.A_REVERSE)
    oldwin.refresh()
    k = board.getkey()
    while not (k in ["\n", " ", curses.KEY_ENTER]):
        oldwin = win
        match k:
            case curses.KEY_UP | "k":
                x = x-1 if x > 0 else x
            case curses.KEY_DOWN | "j":
                x = x+1 if x < 2 else x
            case curses.KEY_LEFT | "h":
                y = y-1 if y > 0 else y
            case curses.KEY_RIGHT | "l":
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
    return x,y

def main(screen):
    global Playing, PlayerX, PlayerO, Board, PlayerTurn
    windows, board = init(screen)
    cursor_style = curses.curs_set(0)
    selected = {'x': (1,1,), 'y': (1,1,),}
    #while Playing:
    selected[PlayerTurn.lower()] = select_move(board, windows, selected[PlayerTurn.lower()])
if __name__=="__main__":
    curses.wrapper(main)
