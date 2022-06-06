"""
Author: Luke Laurie
Date: 5/27/2022
DESCRIPTION: This program starts by creating an displaying an empty Sudoku
    board on a GUI. It then allows the user to either click a randomize button
    to create a randomized game board or it to create a custom board by
    manually clicking on each tile and typing a number. When the solve button
    is clicked it will display the algorithm used to find the solution.
"""
import pygame
from solver_tools import *

pygame.font.init()

# creates rgb values for all the needed colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (144, 238, 144)
DARK_GREEN = (114, 208, 114)
RED = (170, 74, 68)
GREY = (150, 150, 150)
BLUE = (173, 216, 230)
DARK_BLUE = (143, 186, 200)

WIDTH, HEIGHT = 567, 621
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku Solver")

NUMBER_FONT = pygame.font.SysFont("Times New Roman", 40)
WORD_FONT = pygame.font.SysFont("Times New Roman", 22)

class SudokuTile:
    '''
    This class represents a single individual tile of the Sudoku board.
        It will both store information on the tile and use pygame to
        display the tile.
    The constructor will take in four parameters. The x and y parameters
        are integers representing the location of the tile on the GUI. The
        tile_value parameter is a string that contains the value that the tile
        holds. And the border parameter is a tuple with 3 rgb values
        representing the color of the border.
    Methods:
        draw_rect(): Displays the Sudoku tile on the GUI.
        change_value(): Changes the value of the tile.
        change_border(): Changes the color of the border.
    '''
    def __init__(self, x, y, border, tile_value):
        self.x = x
        self.y = y
        self.border = border
        self.tile_value = tile_value

    def draw_rect(self):
        '''
        This will first create and display the tile that will show
            information about the value and border color of the tile.
        '''
        cur_rect = pygame.Rect(self.x, self.y, 63, 63)
        # draws rectangles with their colored borders
        pygame.draw.rect(WIN, WHITE, cur_rect)
        pygame.draw.rect(WIN, GREY, cur_rect, 1)
        pygame.draw.rect(WIN, self.border, pygame.Rect(self.x + 1, self.y + 1, 61, 61), 5)
        # draws the value onto the tile
        if self.tile_value != "0":
            value = NUMBER_FONT.render(self.tile_value, 1, BLACK)
            WIN.blit(value, (self.x + 27, self.y + 11))

    def change_value(self, value):
        '''
        This function will change the value of the tile to
            be a new value.
        Parameters:
            value: An integer that is 1-9 which represents the new
                value of the tile.
        '''
        self.tile_value = str(value)

    def change_border(self, border):
        '''
        This function will change the border color of the tile to
            be a new color.
        Parameters:
            border: A tuple with 3 integers representing the rgb value
                of the new border color.
        '''
        self.border = border

class Board():
    '''
    This class will use tiles created from the SudokuTile class to create
        a game board. This will both initialize the beginning board, and it
        will display the board on a GUI as well.
    The constructor will initialize an array which will later will contain all
        the tiles on the board. The solve_box and random_box are arrays
        containing the information to create the boxes at the bottom of the
        screen. The valid_board variable is a boolean representing if the
        given board was valid. And the correct_border and incorrect_border are
        the two needed RGB colors.
    Methods:
         draw_window(): Displays the Sudoku board onto a GUI.
         create_board(): Creates and then adds each tile of the
            board to an array.
    '''
    def __init__(self):
        self.game_board = []
        self.solve_box = [pygame.Rect(290, 574, 140, 40), GREEN]
        self.random_box = [pygame.Rect(137, 574, 140, 40), BLUE]
        self.valid_board = True
        self.correct_border = GREEN
        self.incorrect_border = RED

    def draw_window(self, solve, random, is_valid):
        '''
        This draws each of the Sudoku tiles and the lines separating the
            tiles onto the GUI.
        Parameters:
            solve: An array where the first value is a tuple with 3 integers
                representing a rgb value and the second is a rectangle.
            random: An array where the first value is a tuple with 3 integers
                representing a rgb value and the second is a rectangle.
            is_valid: A boolean value representing if the inputted board
                is valid or not.
        '''
        WIN.fill(WHITE)
        # draws each tile onto the board
        for tile in self.game_board:
            tile.draw_rect()
        # draws the solve/random boxes
        pygame.draw.rect(WIN, solve[1], solve[0])
        pygame.draw.rect(WIN, random[1], random[0])
        # draws the words on the boxes
        random_word = WORD_FONT.render("Random Board", 1, BLACK)
        WIN.blit(random_word, (139, 579))
        solve_word = WORD_FONT.render("Solve", 1, BLACK)
        WIN.blit(solve_word, (330, 579))
        # draw the lines separating the tiles
        pygame.draw.line(WIN, BLACK, (0, 189), (567, 189), 5)
        pygame.draw.line(WIN, BLACK, (0, 378), (567, 378), 5)
        pygame.draw.line(WIN, BLACK, (189, 0), (189, 567), 5)
        pygame.draw.line(WIN, BLACK, (378, 0), (378, 567), 5)
        # checks if the given board was valid
        if not is_valid:
            invalid_word = WORD_FONT.render("Invalid Input", 1, RED)
            WIN.blit(invalid_word, (440, 579))
        pygame.display.update()

    def create_board(self):
        '''
        This function creates the initial Sudoku board where each value
            of the tiles will be initialized to zero.
        Return Type:
            Returns an array of objects where each object represents a tile
            on the Sudoku board.
        '''
        self.game_board = []
        for i in range(9):
            for j in range(9):
                # determines the location of each tile
                x_location = j * 63
                y_location = i * 63
                border = WHITE
                tile_value = "0"
                # adds each tile object individually to the array
                new_tile = SudokuTile(x_location, y_location, border, tile_value)
                self.game_board.append(new_tile)

def main():
    # creates the initial game board
    sudoku_board = Board()
    sudoku_board.create_board()
    cur_board = sudoku_board.game_board
    keep_running, final_position = True, None
    # runs until the user exits out of the program
    while keep_running:
        # displays the board
        sudoku_board.draw_window(sudoku_board.solve_box,
            sudoku_board.random_box, sudoku_board.valid_board)
        for event in pygame.event.get():
            solve_button = sudoku_board.solve_box[0]
            random_button = sudoku_board.random_box[0]
            # determines the location of the cursor
            cur_position = pygame.mouse.get_pos()
            x_location = cur_position[0] // 63
            y_location = cur_position[1] // 63
            # checks if the cursor is hovering over the random box
            if random_button.collidepoint(cur_position):
                sudoku_board.random_box[1] = DARK_BLUE
            else:
                sudoku_board.random_box[1] = BLUE
            # checks if the cursor is hovering over the solve box
            if solve_button.collidepoint(cur_position):
                sudoku_board.solve_box[1] = DARK_GREEN
            else:
                sudoku_board.solve_box[1] = GREEN
            # ends the program when the user exits out
            if event.type == pygame.QUIT:
                keep_running = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # runs the solver if the solve box is clicked
                if solve_button.collidepoint(cur_position) and \
                                        sudoku_board.valid_board:
                    sudoku_board.valid_board = back_track(cur_board,
                                                sudoku_board, False)
                # creates a random board if the random button is pressed
                if random_button.collidepoint(cur_position):
                    sudoku_board.valid_board = True
                    sudoku_board.create_board()
                    cur_board = sudoku_board.game_board
                    back_track(cur_board, sudoku_board, True)
                    remove_vals(cur_board)
                elif y_location <= 8:
                    # only allows for one block to be selected at a time
                    if final_position is not None:
                        cur_board[final_position].change_border(WHITE)
                    final_position = x_location + (y_location * 9)
                    cur_board[final_position].change_border(BLUE)
            if event.type == pygame.KEYDOWN:
                key_pressed = pygame.key.name(event.key)
                # changes the selected squares value to the number typed by the user
                if final_position is not None and key_pressed.isdigit():
                    # checks if the inputted number was valid
                    if not is_valid(cur_board, y_location, x_location, key_pressed):
                        sudoku_board.valid_board = False
                    else:
                        sudoku_board.valid_board = True
                    cur_board[final_position].change_border(WHITE)
                    cur_board[final_position].change_value(key_pressed)
                    final_position = None


if __name__ == main():
    main()