#!/usr/bin/env python3
# Created By: Atri Sarker
# Date: May 26, 2025
# Game: Merge the Numbers

import random
import util
import getch


# Class for the game
class Game:
    # CONSTRUCTOR
    def __init__(self, num_rows: int, num_cols: int):
        # SET row and column counts, according to the provided values
        self.row_count = num_rows
        self.col_count = num_cols
        # Initialize the game board as an empty grid
        self.game_matrix = self.empty_matrix()
        # Initialize score, starts at 0
        self.score = 0

    # FUNCTION THAT RETURNS A MATRIX OF SIZE [row_count * col_count]
    # WITH EVERY ELEMENT BEING A 0
    def empty_matrix(self) -> list:
        # INITIALIZE AN EMPTY LIST
        result_matrix = []
        # FOR LOOP [CREATE (row_count) rows]
        for row_num in range(self.row_count):
            # INITIALIZE A NEW ROW
            new_row = []
            # FOR LOOP [CREATE (col_count) columns]
            for col_num in range(self.col_count):
                # APPEND AN EMPTY SLOT
                new_row.append(0)
            # Append the new row to the result matrix
            result_matrix.append(new_row)
        # RETURN THE EMPTY MATRIX
        return result_matrix

    # FUNCTION THAT SPAWNS A VALUE OF 2 or 4 into the game matrix
    def spawn_box(self):
        # GET AMOUNT OF EMPTY SPACES WITHIN THE GAME MATRIX
        num_empty_spaces = 0
        # LOOP THROUGH EVERY ELEMENT IN THE GRID
        for row in self.game_matrix:
            for col in row:
                # CHECK IF THE ELEMENT IS A 0
                if col == 0:
                    # IF IT IS, INCREMENT THE COUNT
                    num_empty_spaces += 1
        # GENERATE a random number between 0 and num_empty_spaces
        rand_num = random.randint(0, num_empty_spaces - 1)
        # LOOP THROUGH EVERY ELEMENT POSITION
        for index in range(self.row_count * self.col_count):
            # GET ROW AND COLUMN INDICES
            row_index = index // self.col_count
            col_index = index % self.col_count
            # CHECK IF THE ELEMENT FOUND AT THE GRID POSITION IS EMPTY
            if self.game_matrix[row_index][col_index] == 0:
                # CHECK IF the random number has reached 0
                if rand_num == 0:
                    # GENERATE A RANDOM NUMBER
                    rand_box_num = 4 if random.randint(0, 9) == 9 else 2
                    # UPDATE SCORE BASED ON THE GENERATED NUMBER
                    self.score += rand_box_num
                    # ADD THE NUMBER TO THE BOARD
                    self.game_matrix[row_index][col_index] = rand_box_num
                    # BREAK
                    break
                else:
                    # OTHERWISE, DECREMENT the random number
                    rand_num -= 1

    # FUNCTION THAT DISPLAYS THE GAME BOARD [GAME MATRIX]
    def display_board(self):
        # LOOP THROUGH EVERY ROW
        for row in self.game_matrix:
            # LOOP THROUGH EVERY COLUMN IN THE ROW
            for col in row:
                # GET THE COLOR FOR THE NUMBER
                text_color = util.get_color_from_number(col)
                # CHECK IF NUMBER IS SMALL ENOUGH
                if col < 100_000:
                    print(f"\033[1m{text_color}{str(col).center(6)}", end="")
                else:
                    # IF IT ISN't, SHORTEN IT USING SCIENTIFIC NOTATION
                    print(f"\033[1m{text_color}{col:.0e} ", end="")
            # PRINT A NEWLINE
            print()
        # RESET TEXT STYLE
        util.white("\033[0m")

    # FUNCTION THAT DISPLAYS THE STATE OF THE GAME
    def display_game(self):
        # CLEAR TERMINAL
        util.clear_terminal()
        # DISPLAY TITLE
        util.display_title()
        # DISPLAY SCORE
        util.purple(f"SCORE: {self.score}\n")
        # DISPLAY BOARD
        self.display_board()

    # GAME LOOP
    def game_loop(self):
        # SPAWN A BOX
        self.spawn_box()
        # CHECK IF THE GAME IS OVER
        if self.is_game_over():
            # IF IT IS, STOP THE GAME LOOP BY RETURNING
            return
        # DISPLAY THE GAME
        self.display_game()
        # HANDLE USER'S ACTION
        while True:
            # GET THE USER'S ACTION
            user_action = self.get_action()
            # CHECK IF THE ACTION DOES SOMETHING
            if self.game_matrix == self.handle_action(user_action):
                # IF IT DOESN'T, ASK THE USER FOR AN ACTION AGAIN
                # Reset the terminal display
                self.display_game()
                continue
            else:
                # CHANGE Game matrix, according to the user's action
                # 2nd argument is true, because this move actually counts
                # towards the player's score
                self.game_matrix = self.handle_action(user_action, True)
                # BREAK THE LOOP
                break

    # FUNCTION THAT PLAYS THE GAME
    def play(self):
        while True:
            # GAME LOOP
            self.game_loop()
            # CHECK IF THE GAME IS OVER
            if self.is_game_over():
                # IF IT IS, STOP THE LOOP AND DISPLAY THE LOSING MESSAGE
                # DISPLAY THE FINAL GAME STATE
                self.display_game()
                # DISPLAY THE LOSING MESSAGE
                util.red(f"GAME OVER. FINAL SCORE : {self.score}\n")
                # BREAK
                break

    # FUNCTION THAT GETS AND RETURNS THE USER'S ACTION
    def get_action(self) -> str:
        # DISPLAY PROMPT
        print("Enter a keypress (WASD/ARROW KEYS): ")
        while True:
            # Wait for any key press
            key = getch.getch()
            # Match the key with the movement
            match (key):
                case "w" | "W":
                    return "UP"
                case "a" | "A":
                    return "LEFT"
                case "s" | "S":
                    return "DOWN"
                case "d" | "D":
                    return "RIGHT"
                # ARROW KEYS
                case "\x1b":
                    # Arrow keys are composed of 3 characters in sequence
                    # The first character was "\x1b"
                    # The next 2 characters determine the direction
                    # Match the 2 characters following "\x1b"
                    match (getch.getch() + getch.getch()):
                        # [A is the up arrow
                        case "[A":
                            return "UP"
                        # [D is the left arrow
                        case "[D":
                            return "LEFT"
                        # [B is the down arrow
                        case "[B":
                            return "DOWN"
                        # [C is the down arrow
                        case "[C":
                            return "RIGHT"
                        # Incase it's not an arrow sequence
                        case _:
                            pass
                case _:
                    pass

    # Function that returns the future game board, according to the action
    def handle_action(self, action: str, update_score=False) -> list:
        # MATCH THE ACTION WITH THE MOVEMENT
        match (action):
            case "UP":
                return self.move_up(update_score)
            case "LEFT":
                return self.move_left(update_score)
            case "DOWN":
                return self.move_down(update_score)
            case "RIGHT":
                return self.move_right(update_score)

    # UP
    def move_up(self, update_score=False) -> list:
        # Initialize an empty matrix
        new_matrix = self.empty_matrix()
        # Loop through all the column positions
        for col_index in range(self.col_count):
            # Get column
            col = []
            for row in self.game_matrix:
                col.append(row[col_index])
            # Initialize an empty list
            new_col = []
            # Extract all the non-zero numbers
            for num in col:
                if num != 0:
                    new_col.append(num)
            # Loop through the extracted numbers, excluding the last
            for row_index in range(len(new_col) - 1):
                # Check if 2 adjacent numbers are the same
                if new_col[row_index] == new_col[row_index + 1]:
                    # MERGE
                    new_col[row_index] *= 2
                    new_col[row_index + 1] = 0
                    # If update_score is true, update the score
                    if update_score:
                        self.score += new_col[row_index]
            real_index = 0
            for row_index in range(len(new_col)):
                # Ignore Zeroes
                if new_col[row_index] != 0:
                    new_matrix[real_index][col_index] = new_col[row_index]
                    real_index += 1
        return new_matrix

    # LEFT
    def move_left(self, update_score=False) -> list:
        # Initialize an empty matrix
        new_matrix = self.empty_matrix()
        # Loop through all the row positions
        for row_index in range(self.row_count):
            # Get row
            row = self.game_matrix[row_index]
            # Initialize an empty list
            new_row = []
            # Extract all the non-zero numbers
            for col in row:
                # If the number is not zero, append it to the list
                if col != 0:
                    new_row.append(col)
            # Loop through the extracted numbers, excluding the last
            for col_index in range(len(new_row) - 1):
                # Check if 2 adjacent numbers are the same
                if new_row[col_index] == new_row[col_index + 1]:
                    # MERGE
                    new_row[col_index] *= 2
                    new_row[col_index + 1] = 0
                    # If update_score is true, update the score
                    if update_score:
                        self.score += new_row[col_index]
            real_index = 0
            for col_index in range(len(new_row)):
                # Ignore Zeroes
                if new_row[col_index] != 0:
                    new_matrix[row_index][real_index] = new_row[col_index]
                    real_index += 1
        return new_matrix

    # DOWN
    def move_down(self, update_score=False) -> list:
        # Initialize an empty matrix
        new_matrix = self.empty_matrix()
        # Loop through all the column positions
        for col_index in range(self.col_count):
            # Get column
            col = []
            for row in self.game_matrix:
                col.append(row[col_index])
            # Initialize an empty list
            new_col = []
            # Extract all the non-zero numbers
            for num in col:
                # If the number is not zero, append it to the list
                if num != 0:
                    # If the number is not zero, append it to the list
                    new_col.append(num)
            # Reverse the list
            new_col = new_col[::-1]
            # Loop through the extracted numbers, excluding the last
            for row_index in range(len(new_col) - 1):
                # Check if 2 adjacent numbers are the same
                if new_col[row_index] == new_col[row_index + 1]:
                    # MERGE
                    new_col[row_index] *= 2
                    new_col[row_index + 1] = 0
                    # If update_score is true, update the score
                    if update_score:
                        self.score += new_col[row_index]
            real_index = -1
            for row_index in range(len(new_col)):
                # Ignore Zeroes
                if new_col[row_index] != 0:
                    new_matrix[real_index][col_index] = new_col[row_index]
                    real_index -= 1
        return new_matrix

    # RIGHT
    def move_right(self, update_score=False) -> list:
        # Initialize an empty matrix
        new_matrix = self.empty_matrix()
        # Loop through all the row positions
        for row_index in range(self.row_count):
            # Get row
            row = self.game_matrix[row_index]
            # Initialize an empty list
            new_row = []
            # Extract all the non-zero numbers
            for col in row:
                if col != 0:
                    new_row.append(col)
            new_row = new_row[::-1]
            # Loop through the extracted numbers, excluding the last
            for col_index in range(len(new_row) - 1):
                # Check if 2 adjacent numbers are the same
                if new_row[col_index] == new_row[col_index + 1]:
                    # MERGE
                    new_row[col_index] *= 2
                    new_row[col_index + 1] = 0
                    # If update_score is true, update the score
                    if update_score:
                        self.score += new_row[col_index]
            real_index = -1
            for col_index in range(len(new_row)):
                # Ignore Zeroes
                if new_row[col_index] != 0:
                    new_matrix[row_index][real_index] = new_row[col_index]
                    real_index -= 1
        return new_matrix

    # FUNCTION THAT DETERMINES WHETHER THE GAME IS OVER OR NOT
    def is_game_over(self) -> bool:
        # GIANT BOOLEAN EXPRESSION
        # CHECKS IF THERE ARE ANY POSSIBLE MOVEMENTS
        return (
            (self.game_matrix == self.move_left())
            and (self.game_matrix == self.move_right())
            and (self.game_matrix == self.move_up())
            and (self.game_matrix == self.move_down())
        )


# PROBLEM FUNCTION CALL
def summation_game(num_rows: int, num_cols: int):
    # Instantiate the game
    new_game = Game(num_rows, num_cols)
    # Play the game
    new_game.play()


# MAIN
def main():
    # DISPLAY INTRODUCTION MESSAGE
    util.purple("Welcome to Merge the Numbers!\n")
    # Ask user for the amount of rows as a string
    num_rows_string = input("Enter the amount of rows: ")
    # Ask user for the amount of columns as a string
    num_cols_string = input("Enter the amount of columns: ")
    try:
        # Convert user input to an integer
        num_rows = int(num_rows_string)
        try:
            # Convert user input to an integer
            num_cols = int(num_cols_string)
            # Number of rows has to be greater than 0
            if num_rows < 1:
                # Tell the user that the amount of rows is too low
                util.red("Number of rows must be greater than 0.\n")
            # Number of columns has to be greater than 1
            elif num_cols < 2:
                # Tell the user that the amount of columns is too low
                util.red("Number of columns must be greater than 1.\n")
            else:
                # CALL THE FUNCTION THAT CREATES AND PLAYS THE GAME
                summation_game(num_rows, num_cols)
        except:
            # Tell the user that their input wasn't an integer
            util.red(f"{num_cols_string} is not a valid integer.\n")
    except:
        # Tell the user that their input wasn't an integer
        util.red(f"{num_rows_string} is not a valid integer.\n")


if __name__ == "__main__":
    main()
