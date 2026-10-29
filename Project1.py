#Made by Conrad Boltz, and Declan Mancilla

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
