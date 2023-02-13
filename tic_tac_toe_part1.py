import sys
import pygame
from pygame.locals import *
import pygame_menu
import random

pygame.init()

# determine the sizes
square_size = 150
width = square_size * 3
height = square_size * 3
window_size = (width, height)

# font for displaying the marks
font_size = square_size * 80 // 100
font = pygame.font.Font(pygame.font.get_default_font(), font_size)

# create the game window
game_window = pygame.display.set_mode(window_size)
pygame.display.set_caption('Tic Tac Toe')

class Square:

    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.mark = None

    def draw(self):
        if self.mark is not None:
            white = (255, 255, 255)
            text = font.render(self.mark, True, white)
            text_rect = text.get_rect()
            center_x = self.col * square_size + square_size // 2
            center_y = self.row * square_size + square_size // 2
            text_rect.center = (center_x, center_y)
            game_window.blit(text, text_rect)

class Board:

    def __init__(self):

        # create a dictionary of squares
        # key will be a (row, col) tuple
        # value is a square object
        self.squares = dict()

        # create a blank board
        self.create_new_board()

    def create_new_board(self):

        # create 3 rows and 3 cols
        for row in range(3):
            for col in range(3):
                # add an empty square
                self.squares[(row, col)] = Square(row, col)

        # for highlighting the squares after winning
        self.winning_squares = []

    def draw(self):

        # draw the background
        green = (94, 173, 106)
        game_window.fill(green)

        # highlight the winning squares
        yellow = (228, 235, 134)
        for square in self.winning_squares:
            rect_x = square.col * square_size
            rect_y = square.row * square_size
            rect = Rect(rect_x, rect_y, square_size, square_size)
            pygame.draw.rect(game_window, yellow, rect)

        # draw the lines
        black = (0, 0, 0)
        for i in range(3):

            # vertical lines
            start_pos = (i * square_size, 0)
            end_pos = (i * square_size, height)
            pygame.draw.line(game_window, black, start_pos, end_pos)

            # horizontal lines
            start_pos = (0, i * square_size)
            end_pos = (width, i * square_size)
            pygame.draw.line(game_window, black, start_pos, end_pos)

            # draw the squares
            for row, col in self.squares:
                square = self.squares[(row, col)]
                square.draw()

    def check_row_win(self, row, mark):

        # assume for now that all marks in this row are the same
        same_marks_in_row = True

        # check if there's a square in the row that doesn't have the same mark
        for col in range(3):
            if self.squares[(row, col)].mark != mark:
                same_marks_in_row = False

        # add the winning squares
        if same_marks_in_row:
            for col in range(3):
                self.winning_squares.append(self.squares[(row, col)])

        return same_marks_in_row

    def check_col_win(self, col, mark):

        # assume for now that all marks in this col are the same
        same_marks_in_col = True

        # check if there's a square in the col that doesn't have the same mark
        for row in range(3):
            if self.squares[(row, col)].mark != mark:
                same_marks_in_col = False

        # add the winning squares
        if same_marks_in_col:
            for row in range(3):
                self.winning_squares.append(self.squares[(row, col)])

        return same_marks_in_col

    def check_diagonal_win(self, mark):

        # assume for now that all marks in the upper-left to lower-right diagonal are the same
        same_marks_in_diagonal = True

        # check if there's a square in the diagonal that doesn't have the same mark
        row = 0
        col = 0
        for i in range(3):
            if self.squares[(row + i, col + i)].mark != mark:
                same_marks_in_diagonal = False

        # add the winning squares then return True
        if same_marks_in_diagonal:
            row = 0
            col = 0
            for i in range(3):
                self.winning_squares.append(self.squares[(row + i, col + i)])
            return True

        # check the other diagonal direction (lower-left to upper-right)
        same_marks_in_diagonal = True
        row = 2
        col = 0
        for i in range(3):
            if self.squares[(row - i, col + i)].mark != mark:
                same_marks_in_diagonal = False

        # add the winning squares then return True
        if same_marks_in_diagonal:
            row = 2
            col = 0
            for i in range(3):
                self.winning_squares.append(self.squares[(row - i, col + i)])
            return True

        return same_marks_in_diagonal

    def check_winner(self, clicked_square, mark):
        
        if self.check_row_win(clicked_square.row, mark):
            return True
        elif self.check_col_win(clicked_square.col, mark):
            return True
        elif self.check_diagonal_win(mark):
            return True
        else:
            return False

    def check_tie(self):
        
        # check if there's an open square
        for row, col in self.squares:
            if self.squares[(row, col)].mark is None:
                return False
        return True

class Player:

    def __init__(self, mark):
        self.mark = mark

    def move(self, board, click_pos):

        # get the x,y positions of the mouse click
        click_x, click_y = click_pos

        # get the row and col of the clicked square
        row = click_y // square_size
        col = click_x // square_size

        # mark the square if it's empty
        if board.squares[(row, col)].mark is None:
            board.squares[(row, col)].mark = self.mark
            return board.squares[(row, col)]
        else:
            return None

def display_results(msg):

    my_theme = pygame_menu.themes.THEME_BLUE
    my_theme.title_font_size = 18
    my_theme.widget_font_size = 12
    results_popup = pygame_menu.Menu('Game over', 150, 150, theme = my_theme)
    results_popup.add.label(msg)
    results_popup.add.vertical_margin(30)
    results_popup.add.button('Play Again', run_game)
    results_popup.mainloop(game_window)

def run_game():

    # create the board
    board = Board()

    # create the players
    player = Player('X')
    opponent = Player('O')

    # randomly select who goes first
    current_player = random.choice([player, opponent])

    # game status (playing, winner, or tie)
    game_status = 'playing'

    # game loop
    while True:

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            # check for mouse click
            if event.type == MOUSEBUTTONDOWN:

                # fill the square that was clicked
                square = current_player.move(board, pygame.mouse.get_pos())

                # check if clicking the square was successful
                if square is not None:

                    # update the game status if there's a winner or if it's a tie
                    # otherwise switch players
                    if board.check_winner(square, current_player.mark):
                        game_status = 'winner'
                    elif board.check_tie():
                        game_status = 'tie'
                    else:
                        if current_player == player:
                            current_player = opponent
                        else:
                            current_player = player

        board.draw()
        pygame.display.update()

        # display in the title who the current player is
        pygame.display.set_caption(f"Tic Tac Toe - {current_player.mark}'s move")

        # if there's a winner or a tie
        # wait 3 seconds, then display the results
        if game_status == 'winner':
            pygame.time.wait(3000)
            display_results(f'Player {current_player.mark} wins!')
        elif game_status == 'tie':
            pygame.time.wait(3000)
            display_results("It's a Tie!")

if __name__ == '__main__':
    run_game()