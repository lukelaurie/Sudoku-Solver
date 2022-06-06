"""
Author: Luke Laurie
Date: 5/27/2022
DESCRIPTION: This program will run a recursive backtracking algorithm to find
    the solution to any given Sudoku puzzle. It solves the puzzle by checking
    each number 1-9 to see if it is a valid placement on the puzzle, and if so
    it places the number. If none of the numbers 1-9 are valid it recurses
    backwards into a previous tile and tries placing a different value.
"""
import random
import pygame

def back_track(game_board, sudoku_board, is_random):
    '''
    This implements a recursive backtracking algorithm through the
        each of the Sudoku tiles. It will check for a value 1-9 to see if the
        number is valid and if so the number will be placed in the tile. If
        none of the numbers are valid it will backtrack into the previous
        tile and try changing that value to a different value.
    Parameters:
        game_board: This is an array of objects where each object represents
            a tile on the Sudoku board.
        sudoku_board: An object of a class that represents the board for the
            sudoku game.
        is_random: A boolean value representing if a randomized board needs to
            be created.
    Return Type:
        Returns a boolean value representing if the given board was valid.
    '''
    # ends the program if user tries to exit out
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    zero_location = find_zero(game_board)
    # if no zeros are left in the board then the solution is found
    if zero_location == False:
        return True
    row_index, column_index = zero_location[0], zero_location[1]
    tile_number = (row_index * 9) + column_index
    # looks for a valid number to be placed
    possible_values = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    for cur_index in range(1, 10):
        placement_val = str(cur_index)
        # gets a random value to be attempted to be placed
        if is_random:
            cur_index = random.randint(0, len(possible_values) - 1)
            placement_val = possible_values[cur_index]
            possible_values.pop(cur_index)
        valid = is_valid(game_board, row_index, column_index, placement_val)
        if valid:
            # changes the value and border color of the tile
            game_board[tile_number].change_value(placement_val)
            if not is_random:
                change_border(tile_number, game_board, sudoku_board, sudoku_board.correct_border)
            back_track(game_board, sudoku_board, is_random)
            # backtracks again with a different value
            if find_zero(game_board) != False:
                game_board[tile_number].change_value("0")
                if not is_random:
                    change_border(tile_number, game_board, sudoku_board, sudoku_board.incorrect_border)
            else:
                # ends recursion if the board is completed
                return True
    # not a valid board
    return False

def is_valid(game_board, i, j, val):
    '''
    This determines whether a given number is a valid placement on the
        Sudoku board or not. The number will be valid if it is not in the
        same horizontal/vertical line or in the same cell.
    Parameters:
        game_board: This is an array of objects where each object represents
            a tile on the Sudoku board.
        i: An integer representing the index for the row of the tile.
        j: An integer representing the index for the column of the tile.
        val: An integer 1-9 that is attempting to be placed in the tile.
    Return Type:
        Returns a boolean value representing if the value is a valid.
    '''
    # checks if row/column is invalid
    for index in range(9):
        if game_board[(i * 9) + index].tile_value == str(val):
            return False
        if game_board[(index * 9) + j].tile_value == str(val):
            return False
    # checks if value is contained in the cell
    i = (i // 3) * 3
    j = (j // 3) * 3
    for index in range(i, i + 3):
        for j_index in range(j, j+ 3):
            if game_board[(index * 9) + j_index].tile_value == str(val):
                return False
    return True

def find_zero(game_board):
    '''
    This checks to see if any of the Sudoku tiles contains a 0. If
        it does then it determines the location of the 0.
    Parameters:
        game_board: This is an array of objects where each object
            represents a tile on the Sudoku board.
    Return Type:
        Returns a tuple containing the row/column index or a Boolean
        value representing if the board is completed or not.
    '''
    for i in range(9):
        for j in range(9):
            # determines if the value of the tile is 0
            cur_val = game_board[(9 * i) + j].tile_value
            if cur_val == "0":
                row_index = i
                column_index = j
                return (row_index, column_index)
    return False

def remove_vals(game_board):
    '''
    This will change a random amount of randomly selected values on
        the game board back to zero.
    Parameters:
        game_board: This is an array of objects where each object
            represents a tile on the Sudoku board.
    '''
    removal_amount = random.randint(25, 65)
    # sets random tiles back to 0
    for i in range(removal_amount):
        rand_index = random.randint(0, 80)
        game_board[rand_index].change_value("0")

def change_border(tile_number, game_board, sudoku_board, color):
    '''
    This will change the background color of a specific tile to either
        green or red and then display the changed tile onto the GUI.
    Parameters:
        tile_number: An integer representing the index of the tile that
            needs to be changed on the game board.
        sudoku_board: An object of a class that represents the board
            of the sudoku game.
        game_board: This is an array of objects where each object
            represents a tile on the Sudoku board.
        color: A tuple with three integers each representing an rgb value.
    '''
    # changes the background color of the tile
    game_board[tile_number].change_border(color)
    sudoku_board.draw_window(sudoku_board.solve_box,
        sudoku_board.random_box, sudoku_board.valid_board)
    pygame.time.delay(50)