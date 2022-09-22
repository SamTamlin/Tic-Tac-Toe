import os
from random import randint


class new_player:
    def __init__(self, name, side):
        self.name = name
        self.side = side
        self.human = True
        self.games_played = 0
        self.games_won = 0
        self.games_tied = 0
        self.games_lost = 0


def new_board():
    """Returns an empty, nested 3 x 3 list"""
    return [[' ' for line in range(0, 3)] for line in range(0, 3)]


def main_menu():
    while True:
        print("\n\tTIC-TAC-TOE")
        print("\t[1] Single Player Game")
        print("\t[2] Multiplayer Game")
        print("\t[S] Settings & Statistics")
        print("\t[Q] Quit Game")

        player_choice = input("\t Please make your selection: ").lower()

        if player_choice == '1':
            player_2.human = False
            return True

        elif player_choice == '2':
            player_2.human = True
            return True

        elif player_choice == 's':
            settings_menu()

        elif player_choice == 'q':
            return False

        else:
            print("\tSorry I didn't understand that.")


def settings_menu():
    os.system('cls')
    while True:
        print("\n\tSettings & Statistics Menu")
        print("\t[1] Rename %s" % player_1.name.title())
        print("\t[2] Rename %s" % player_2.name.title())
        print("\t[S] Statistics")
        print("\t[Q] Exit Settings Menu")

        settings_choice = input("\tPlease make your selection: ").lower()

        if settings_choice == '1':
            rename(player_1)

        elif settings_choice == '2':
            rename(player_2)

        elif settings_choice == 's':
            stats()

        elif settings_choice == 'q':
            return False

        else:
            print("\tSorry I didn't understand that.")


def stats():
    os.system('cls')
    print("\n\tStatistics")
    print("\n\t'%s' has played %d games: \n\t\tWon: %s \n\t\tLost: %s "
          "\n\t\tDrawn: %s" % (player_1.name.upper(), player_1.games_played,
                               player_1.games_won, player_1.games_lost,
                               player_1.games_tied))
    print("\n\t'%s' has played %d games: \n\t\tWon: %s \n\t\tLost: %s "
          "\n\t\tDrawn: %s" % (player_2.name.upper(), player_2.games_played,
                               player_2.games_won, player_2.games_lost,
                               player_2.games_tied))
    input("\n\t Press enter to return to the Settings menu.")

def rename(player):
    new_name = input(
        "\t%s, what would you like to be called? "
        % player.name.title()).lower()
    if new_name:
        player.name = new_name


def print_board(board):
    """Takes the inputted board and prints it as a regular Tic-Tac-Toe board
    with x & y co-ordinates shown."""
    print("\n\t   0   1   2   x")
    for y, line in enumerate(board):
        print("\t%d  %s | %s | %s " % (y, line[0], line[1], line[2]))
        if y != 2:
            print("\t  -----------")
    print("\n\ty")


def get_move(turn_board, player):
    """Takes the name of the player and asks them for co-ordinates. Checks
    that the co-ordinates are reasonable and requests again if they are not.
    Function then returns the co-ordinates as integers."""
    if player.human:
        while True:
            y = input("\n\t%s enter your Y co-ordinate: "
                      % player.name.title())
            # If the input is not a co-ordinate, print an error and ask again.
            if y != '0' and y != '1' and y != '2':
                print("\tYou must enter a number between 0 and 2.")
            else:
                break

        while True:
            x = input("\t%s enter your X co-ordinate: " % player.name.title())
            # If the input is not a co-ordinate, print an error and ask again.
            if x != '0' and x != '1' and x != '2':
                print("\tYou must enter a number between 0 and 2.")
            else:
                break
    else:
        y, x = get_random_move(turn_board, player)

    return int(y), int(x)


def get_random_move(turn_board, player):
    """Takes a board and a player, then returns co-ordinates
    of a random empty cell."""
    good_move = False
    while not good_move:
        y = randint(0, 2)
        x = randint(0, 2)
        cords = y, x

        good_move = is_valid_move(turn_board, cords)

    return y, x


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


def take_turn(turn_board, turn_taker, other_player):
    """Takes a board and player which are used to process a players turn.
    Then returns an updated board and if the game should continue by returning
    True or False."""
    os.system('cls')
    print_board(turn_board)

    checking = True
    while checking:
        coordinates = get_move(turn_board, turn_taker)
        valid = is_valid_move(turn_board, coordinates)
        if valid:
            checking = False
        else:
            os.system('cls')
            print_board(turn_board)
            print("\n\tSorry, this move has already been made!!.")

    turn_board = make_move(turn_board, coordinates, turn_taker)

    winner = get_winner(turn_board)
    drawn = check_for_draw(turn_board)

    if winner is not None:
        print_board(turn_board)
        print("\n\t'%s' WINS! Congratulations %s you are the winner!!!"
              % (turn_taker.side, turn_taker.name.title()))
        turn_taker.games_won += 1
        turn_taker.games_played += 1
        other_player.games_played += 1
        other_player.games_lost += 1
        return turn_board, False

    if drawn:
        print_board(turn_board)
        print("\n\tTHE GAME IS A TIE!")
        turn_taker.games_tied += 1
        turn_taker.games_played += 1
        other_player.games_tied += 1
        other_player.games_played += 1
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
        game_board, playing_game = take_turn(
            game_board, player_1, player_2)

        if playing_game:
            # Player_2'a turn.
            game_board, playing_game = take_turn(
                game_board, player_2, player_1)
