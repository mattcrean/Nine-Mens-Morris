"""
MATH20621 - Coursework 3
Student name: Matthew Crean
Student id: 11093712
Student mail: matthew_crean@student.manchester.ac.uk
"""

def request_location(question_str):
    """
    Prompt the user for a board location, and return that location.
    
    Takes a string parameter, which is displayed to the user as a prompt.
    
    Raises ValueError if input is not a valid integer, 
    or RuntimeError if the location typed is not in the valid range.
    
    *************************************************************
    DO NOT change this function in any way
    You MUST use this function for ALL user input in your program
    *************************************************************
    """
    loc = int(input(question_str))
    if loc<0 or loc>=24:
        raise RuntimeError("Not a valid location")
    return loc

def draw_board(g):
    """
    Display the board corresponding to the board state g to console.
    Also displays the numbering for each point on the board, and the
    number of counters left in each players hand, if any.
    A reference to remind players of the number of each point is also displayed.
    
    You may use this function in your program to display the board
    to the user, but you may also use your own similar function, or
    improve this one, to customise the display of the game as you choose
    """
    def colored(r, g, b, text):
        """
        Spyder supports coloured text! This function creates coloured
        version of the text 'text' that can be printed to the console.
        The colour is specified with red (r), green (g), blue (b) components,
        each of which has a range 0-255.
        """
        return f"\033[38;2;{r};{g};{b}m{text}\033[0m"

    def piece_char(i):
        """
        Return the (coloured) character corresponding to player i's counter,
        or a + to indicate an unoccupied point
        """
        if i==0:
            return colored(100,100,100,'+')
        elif i==1:
            return colored(255,60,60,'X')
        elif i==2:
            return colored(60,120,255,'O')

        
    board = '''
x--------x--------x  0--------1--------2 
|        |        |  |        |        |
|  x-----x-----x  |  |  3-----4-----5  |
|  |     |     |  |  |  |     |     |  |
|  |  x--x--x  |  |  |  |  6--7--8  |  |
|  |  |     |  |  |  |  |  |     |  |  |
x--x--x     x--x--x  9-10-11    12-13-14
|  |  |     |  |  |  |  |  |     |  |  |
|  |  x--x--x  |  |  |  | 15-16-17  |  |
|  |     |     |  |  |  |     |     |  |
|  x-----x-----x  |  |  18---19----20  |
|        |        |  |        |        |
x--------x--------x  21------22-------23
'''    
    boardstr = ''
    i = 0
    for c in board:
        if c=='x':
            boardstr += piece_char(g[0][i])
            i += 1
        else:
            boardstr += colored(100,100,100,c)
    if g[1]>0 or g[2]>0:
        boardstr += '\nPlayer 1: ' + (piece_char(1)*g[1])
        boardstr += '\nPlayer 2: ' + (piece_char(2)*g[2])
    print(boardstr)


#The index of the following list gives you a list of numbers that the point 
#is adjacent to. eg. the 2nd index of the list gives [1, 14], and on the board,
#the 2nd point is next to the 1st and 14th. This is used in the is_adjacent
#and player_can_move functions.
adjacent = [[1, 9], [0, 2, 4], [1, 14], [4, 10], [1, 3, 5, 7], [4, 13],\
            [7, 11], [4, 6, 8], [7, 12], [0, 10, 21], [3, 9, 11, 18],\
            [6, 10, 15], [8, 13, 17], [5, 12, 14, 20], [2, 13, 23], [11, 16],\
            [15, 17, 19], [12, 16], [10, 19], [16, 18, 20, 22], [13, 19],\
            [9, 22], [19, 21, 23], [14, 22]]

def is_adjacent(i, j):
    """
    Takes two integers, i and j, and determines whether their points on the
    game board are adjacent to each other.
    Returns True if i and j are adjacent, and False otherwise.
    """
    if adjacent[i].count(j) == 1:
        return True
    return False

def new_game():
    """
    Returns a game state with each player having 9 counters, 
    an empty board and player 1 being the current player.
    """
    return [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],9,9,1]

def remaining_counters(g):
    """
    Takes game state g and returns the number of counters the current player,
    given by the final number in the game state g, has available. 
    (the sum of the counters to hand and on the board)
    """
    return g[g[3]] + g[0].count(g[3])
        
def is_in_mill(g, i): 
    """
    Takes game state g and integer i and returns:
        -1 if i is outside of the range 0-23 inclusive, or if there is no 
           counter at point i
        0 if there is no mill at point i
        1 if there is one or more mills at point i and it belongs to Player 1
        2 if there is ore or more mills at point i and it belongs to Player 2
    """
    if i<0 or i>23 or g[0][i] == 0:
        return -1 
    #y is a list of all of the sets of points for mills on the game board.
    y = [[0, 1, 2], [0, 9, 21], [1, 4, 7], [2, 14, 23], [3, 4, 5], [3, 10, 18],\
         [5, 13, 20], [6, 7, 8], [6, 11, 15], [8, 12, 17], [9, 10, 11],\
         [12, 13, 14], [15, 16, 17], [16, 19, 22], [18, 19, 20], [21, 22, 23]]
    total = 0
    for l in range(16):
        if y[l].count(i) == 1: #picks out mills that contain point i
            for j in range(3):
                if g[0][y[l][j]] == g[0][i]:
                    total = total + 1 #total +1 if points in mill that point i
                                      #is a part of has counter from the same
                                      #player
        if total == 3:
            return int(g[0][i]) #the player number is returned if mill formed
        else:
            total = 0 #total reset to 0 since mill is not formed
    return 0
    
def player_can_move(g):
    """
    Takes game state g and determines whether the current player can move a 
    counter or not. The function returns True if they can and False if they 
    cannot.
    """
    if g[g[3]] > 0: #if current player has any counters to hand, they can move
        return True 
    for i in range(23):
        if g[0][i] == g[3]: #if point i has a counter from current player
            for j in range(len(adjacent[i])):
                if g[0][adjacent[i][j]] == 0: #if there is at least one point
                                              #adjacent to i that has no counter
                    return True
    return False

def place_counter(g, i):
    """
    Takes game state g and integer i between 0 and 23 inclusive and determines 
    whether point i has a counter on it, and raises RuntimeError if so.
    Otherwise, the player whose turn it is has their counter placed on 
    point i and g is altered appropriately.
    """
    if g[0][i] == 0: #if no counter at point i
        g[0][i] = g[3] #counter from current player placed at point i
        g[g[3]] = g[g[3]] - 1 #number of counters current player has to hand
                              #decreases by 1
    else:
        raise RuntimeError('\n Your input must be a free space on the board.'\
                           ' Please try again. \n')

def move_counter(g, i, j):
    """
    Takes game state g and integers i and j and changes g such that the counter
    from the current player is removed from point i and placed on point j.
    This is only done if the move is applicable, otherwise the function rasises
    a RuntimeError.
    """
    if is_adjacent(i, j) == False: #if i and j are not adjacent points
        raise RuntimeError('\n Your input points must be adjacent. Please'\
                           ' try again. \n')
    if g[0][i] != g[3] and g[0][j] != 0:
        raise RuntimeError('\n Your first input must be a point on the board'\
                           ' that has a counter of yours on it, and your second'\
                           ' input must be a free space on the board. Please'\
                           ' try again. \n')
    if g[0][i] != g[3]: #if current player does not have a counter at point i
        raise RuntimeError('\n Your first input must be a point on the board'\
                           ' that has a counter of yours on it. Please try again. \n')
    if g[0][j] != 0: #if there is a counter placed at point j
        raise RuntimeError('\n Your second input must be a free space on the'\
                           ' board. Please try again. \n')
    #the current players' counter is placed on point j of the board and
    #removed from point i
    g[0][j] = g[0][i]
    g[0][i] = 0

def remove_opponent_counter(g, i):
    """
    Takes game state g and integer i and alters g such that the counter from
    point i, that must be of the players whose current turn it is not, is
    removed. Otherwise, a RuntimeError is raised.
    """
    if g[0][i] == 0 or g[0][i] == g[3]: #if point i doesn't have opponent's
                                        #counter
        raise RuntimeError('\n Your input must be a point on the board of'\
                           ' one of your opponents counters. Please try again. \n')
    g[0][i] = 0 #counter removed from point i

def turn(g):
    """
    Takes game state g and allows the current player to have a turn at the game:
        1. Returns False if the player cannot move or they have less than 3 
           counters on the board.
        2. User either places a counter on the board, or moves their counter 
           from one point to another if they have no counters left to hand.
        3. If that counter placed or moved is part of a mill (three in a row),
           the player can remove one of the other players' counters from the 
           board.
        4. The current player is switched to the other player.
        5. Returns True once the turn is finished.
    In both 2 and 3, if the player inputs something incorrect, they are 
    prompted to input again.
    """
    #If the current player can't move or either players have less than three
    #counters on the board and have less than three counters to hand, the
    #function returns False.
    if player_can_move(g) == False or g[0].count(1) < 3 and g[1] == 0 or \
        g[0].count(2) < 3 and g[2] == 0:
        return False
    
    draw_board(g)
    print('\n Your turn, Player', g[3])
    
    if g[g[3]] > 0: #if current player has any counters to hand
        while True:
            try: #current player asked to input point to place counter
                move = request_location('\n Give the location of the counter'\
                                        ' you would like to place: ', )
                place_counter(g, move) #counter is placed
            #if the function raises an error, the player is told their input
            #was invalid and they must input again
            except RuntimeError as e:
                print(e)
            except ValueError:
                print('\n Your input must be an integer. Please try again. \n')
            else:
                break

    else: #if current player has no counters to hand
        while True:
            try: #current player prompted to input location of one of their
                 #counters on the board they'd like to move, and the point
                 #they would like to move it to
                current = request_location('\n Give the location of the counter'\
                                           ' you would like to move: ', )
                move = request_location('\n Now give the location you would'\
                                        ' like to move this counter to: ', )
                move_counter(g, current, move) #counter is moved
            #if the function raises an error, the player is told their input
            #was invalid and they must input again
            except RuntimeError as e:
                print(e)
            except ValueError:
                print('\n Your input must be an integer. Please try again. \n')
            else:
                break
            
    if is_in_mill(g, move) == g[3]: #if location of counter just placed is in mill
        draw_board(g)
        print('\n Player', g[3], 'you have formed a mill!')
        while True:
            try: #current player asked to input point of opponent counter to remove
                remove = request_location('\n Choose the location of one of your'\
                                          ' opponents counters to remove: ', )
                remove_opponent_counter(g, remove) #counter is removed
            #if function raises an error, player is told input was invalid and
            #prompted to input again
            except RuntimeError as e:
                print(e)
            except ValueError:
                print('\n Your input must be an integer. Please try again. \n')
            else:
                break
           
    #current player switches to opponent
    g[3] = (g[3]%2)+1
    return True

def save_state(g, filename):
    """
    Takes game state g and string filename and saves the game state into
    a text file with each element of the list on a separate line. The first 
    line of the file saves the status of the game board as integers with a 
    comma separating each of them. A RuntimeError is called if g cannot be 
    saved to the file.
    """
    if len(g) != 4:
        raise RuntimeError
    try:
        f = open(filename, mode="wt", encoding="utf8") #open file to f in mode
                                                       #for writing text
        #list 'lines' saves g as a list, but with the first variable as
        #just the counter at point 0
        lines = [str(g[0][0]), str(g[1])+"\n", str(g[2])+"\n", str(g[3])]
        for i in range(1, 23):
            #the following extends the first element of 'lines' to full game
            #board, with each point separated by a comma, all as one string
            lines[0] = lines[0] + ", " + str(g[0][i])
        lines[0] = lines[0] + "\n"
        f.writelines(lines) #each line of file saved as element of 'lines'
        f.close()
    except Exception:
        raise RuntimeError
    
def load_state(filename):
    """
    Opens the file with name 'filename' and returns a game state, where the 
    game board is the first line of the file, the number of counters players 1 
    and 2 have is lines 2 and 3 respectively, and the player whose turn it 
    currently is is line 4. A RuntimeError is raised if the file cannot be 
    changed into a game state.
    """
    try:
        f = open(filename, mode="rt", encoding="utf8") #open file to f in mode
                                                       #for reading text
        board = []
        x = str(f.readline())
        for i in range(23):
            board.append(int(x[3*i])) #list 'board' extended to be game board
        g1 = f.readline() #next three lines of the file are saved to variables
        g2 = f.readline()
        g3 = f.readline()
        g = [board, int(g1), int(g2), int(g3)] #now a game state
        f.close()
        return g
    except Exception:
        raise RuntimeError

def play_game():
    """
    Creates a new game state and calls turn() function repeatedly until the
    game is finished. The winning player is then congratulated.
    """
    g = new_game()
    turn(g)
    while turn(g) == True:
        turn(g)
    draw_board(g)
    print('\n Congratulations Player', (g[3]%2)+1,', you are the winner!')
    pass

def main():
    play_game()

main()