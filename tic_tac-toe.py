import os


class new_player:
    def __init__(self, name, side):
        self.name = name
        self.side = side


def new_board():
    """Returns an empty, nested 3 x 3 list"""
    return [[' ' for line in range(0, 3)] for line in range(0, 3)]


def main_menu():
    while True:
        print("\n\tTIC-TAC-TOE")
        print("\t[1] Start Game")
        print("\t[Q] Quit")

        player_choice = input("\t Please make your selection: ").lower()

        if player_choice == '1':
            return True

        elif player_choice == 'q':
            return False

        else:
            print("\t Sorry I didn't understand that.")


def print_board(board):
    """Takes the inputted board and prints it as a regular Tic-Tac-Toe board
    with x & y co-ordinates shown."""
    print("\n\t   0   1   2   x")
    for y, line in enumerate(board):
        print("\t%d  %s | %s | %s " % (y, line[0], line[1], line[2]))
        if y != 2:
            print("\t  -----------")
    print("\n\ty")


def get_move(name):
    """Takes the name of the player and asks them for co-ordinates. Checks
    that the co-ordinates are reasonable and requests again if they are not.
    Function then returns the co-ordinates as integers."""
    while True:
        y = input("\n\t%s enter your Y co-ordinate: " % name.title())
        # If the input is not a co-ordinate, print an error and ask again.
        if y != '0' and y != '1' and y != '2':
            print("\tYou must enter a number between 0 and 2.")
        else:
            break

    while True:
        x = input("\t%s enter your X co-ordinate: " % name.title())
        # If the input is not a co-ordinate, print an error and ask again.
        if x != '0' and x != '1' and x != '2':
            print("\tYou must enter a number between 0 and 2.")
        else:
            break

    return int(y), int(x)


def is_valid_move(board, cords):
    """Takes the board and entered co-ordinates and checks that the board is
    empty in that location. If empty returns True,
    if already in use returns False"""
    if board[cords[0]][cords[1]] == ' ':
        return True
    else:
        return False


def make_move(board, move_cords, player):
    """Takes a board, co-ordinates and a player, adds the players side at the
    co-ordinates received and returns an updated board."""
    next_board = board
    next_board[move_cords[0]][move_cords[1]] = player.side
    return next_board


def take_turn(turn_board, player):
    """Takes a board and player which are used to process a players turn.
    Then returns an updated board and if the game should continue by returning
    True or False."""
    os.system('cls')
    print_board(turn_board)

    checking = True
    while checking:
        coordinates = get_move(player.name)
        valid = is_valid_move(turn_board, coordinates)
        if valid:
            checking = False
        else:
            os.system('cls')
            print_board(turn_board)
            print("\n\tSorry, this move has already been made!!.")

    turn_board = make_move(turn_board, coordinates, player)

    winner = get_winner(turn_board)
    drawn = check_for_draw(turn_board)

    if winner is not None:
        print_board(turn_board)
        print("\n\tCONGRATULATIONS %s(%s) is the winner!"
              % player.name.title(), player.side)
        return turn_board, False

    if drawn:
        print_board(turn_board)
        print("\n\tTHE GAME IS A TIE!")
        return turn_board, False

    return turn_board, True


def get_winner(board):
    """Takes a board and checks against all possible winning lines, if a line
    contains all "X" or all "O" that letter is returned as the winner."""
    lines_to_check = winning_lines()

    for line in lines_to_check:
        line_values = [board[y][x] for (y, x) in line]
        # If all values are the same and don't equal ' ' return the value.
        if len(set(line_values)) == 1 and line_values[0] != ' ':
            return line_values[0]

    return None


def winning_lines():
    """Creates lists of winning lines and outputs them"""
    columns = []
    rows = []
    for y, height in enumerate(range(0, 3)):
        column = []
        row = []
        for x, width in enumerate(range(0, 3)):
            column.append((y, x))
            row.append((x, y))
        columns.append(column)
        rows.append(row)

    diagonals = [[(0, 0), (1, 1), (2, 2)], [(0, 2), (1, 1), (2, 0)]]

    return columns + rows + diagonals


def check_for_draw(board):
    """Takes a board and checks each cell and returns True if all
    cells are full"""
    draw = True
    for y in board:
        for x in y:
            if x == ' ':
                draw = False
    return draw


player_1 = new_player('player 1', 'X')
player_2 = new_player('player 2', 'O')

while True:
    playing_game = main_menu()
    if not playing_game:
        break

    game_board = new_board()

    while playing_game:
        # Player_1's turn
        game_board, playing_game = take_turn(game_board, player_1)

        if playing_game:
            # Player_2'a turn.
            game_board, playing_game = take_turn(game_board, player_2)
