#!/usr/bin/env python3
# Created By: Atri Sarker
# Date: May 26, 2025
# 2048 Game

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
        for row in self.game_matrix:
            for col in row:
                if (col == 0):
                    num_empty_spaces += 1
        # GENERATE a random number between 0 and num_empty_spaces
        rand_num = random.randint(0, num_empty_spaces - 1)
        for index in range(self.row_count * self.col_count):
            row_index = index // self.col_count 
            col_index = index % self.col_count
            if (self.game_matrix[row_index][col_index] == 0):
                if (rand_num == 0):
                    # GENERATE A RANDOM NUMBER
                    rand_box_num = 4 if random.randint(1,10) == 10 else 2
                    # UPDATE SCORE BASED ON THE GENERATED NUMBER
                    self.score += rand_box_num
                    # ADD THE NUMBER TO THE BOARD
                    self.game_matrix[row_index][col_index] = rand_box_num
                    break
                else:
                    rand_num -= 1
    
    # FUNCTION THAT DISPLAYS THE GAME BOARD [GAME MATRIX]
    def display_board(self):
        for row in self.game_matrix:
            for col in row:
                text_color = util.get_color_from_number(col)
                if col < 100_000:
                    print(f"\033[1m{text_color}{str(col).center(6)}", end="")
                else:
                    print(f"\033[1m{text_color}{col:.0e} ", end="")
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
        # DISPLAY GAME
        util.white()
        # DISPLAY BOARD
        self.display_board()

    # GAME LOOP
    def game_loop(self):
        # SPAWN A BOX
        self.spawn_box()
        # CHECK IF THE GAME IS OVER
        if (self.is_game_over()):
            # IF IT IS, STOP THE GAME LOOP BY RETURNING
            return
        # DISPLAY THE GAME
        self.display_game()
        # HANDLE USER'S ACTION
        while (True):
            # GET THE USER'S ACTION
            user_action = self.get_action()
            # CHECK IF THE ACTION DOES SOMETHING
            if (self.game_matrix == self.handle_action(user_action)):
                # IF IT DOESN'T, ASK THE USER FOR AN ACTION AGAIN
                # Reset the terminal display
                self.display_game()
                continue
            else:
                # CHANGE Game matrix, according to the user's action
                # 2nd argument is true, because this move actually counts towards the player's score
                self.game_matrix = self.handle_action(user_action, True)
                # BREAK THE LOOP
                break
    
    # FUNCTION THAT PLAYS THE GAME
    def play(self):
        while (True):
            # GAME LOOP
            self.game_loop()
            # CHECK IF THE GAME IS OVER
            if (self.is_game_over()):
                # IF IT IS, STOP THE LOOP AND DISPLAY THE LOSING MESSAGE
                # Display the losing game state
                self.display_game()
                # Display the losing message
                util.red(f"GAME OVER. FINAL SCORE : {self.score}\n")
                # BREAK
                break
    
    # FUNCTION THAT GETS AND RETURNS THE USER'S ACTION
    def get_action(self) -> str:
        # Display prompt
        print("Enter a keypress: ")
        while (True):
            # Wait for any key press
            key = getch.getch()
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
                    match (getch.getch() + getch.getch()):
                        case "[A":
                            return "UP"
                        case "[D":
                            return "LEFT"
                        case "[B":
                            return "DOWN"
                        case "[C" | "D":
                            return "RIGHT"
                        case _:
                            pass
                case _:
                    pass
    
    def handle_action(self, action: str, update_score = False) -> list:
        match (action):
            case "UP":
                return self.move_up(update_score)
            case "LEFT":
                return self.move_left(update_score)
            case "DOWN":
                return self.move_down(update_score)
            case "RIGHT":
                return self.move_right(update_score)
            
    def move_up(self, update_score = False) -> list:
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
                    if new_col[row_index] == new_col[row_index+1]:
                        # MERGE
                        new_col[row_index] *= 2
                        new_col[row_index+1] = 0
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
    
    def move_left(self, update_score = False) -> list:
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
                    if new_row[col_index] == new_row[col_index+1]:
                        # MERGE
                        new_row[col_index] *= 2
                        new_row[col_index+1] = 0
                        # If update_score is true, update the score
                        if update_score:
                            self.score += new_row[col_index]
            real_index = 0
            for col_index in range(len(new_row)):
                # Ignore Zeroes
                if new_row[col_index] != 0:
                    # 
                    new_matrix[row_index][real_index] = new_row[col_index]
                    real_index += 1
        return new_matrix
    
    def move_down(self, update_score = False) -> list:
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
            new_col = new_col[::-1]
            # Loop through the extracted numbers, excluding the last
            for row_index in range(len(new_col) - 1):
                    # Check if 2 adjacent numbers are the same
                    if new_col[row_index] == new_col[row_index+1]:
                        # MERGE
                        new_col[row_index] *= 2
                        new_col[row_index+1] = 0
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
    
    def move_right(self, update_score = False) -> list:
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
                    if new_row[col_index] == new_row[col_index+1]:
                        # MERGE
                        new_row[col_index] *= 2
                        new_row[col_index+1] = 0
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
        return (self.game_matrix  == self.move_left()) and (self.game_matrix == self.move_right()) and (self.game_matrix == self.move_up()) and (self.game_matrix == self.move_down())


        

        



    
# PROBLEM FUNCTION CALL
def summation_game(num_rows: int, num_cols: int):
    # Instantiate the game
    new_game = Game(num_rows, num_cols)
    # Play the game
    new_game.play()

# MAIN
def main():
    summation_game(2,2)


if __name__ == "__main__":
    main()
