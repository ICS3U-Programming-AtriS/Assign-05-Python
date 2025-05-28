#!/usr/bin/env python3
# Created By: Atri Sarker
# Date: April 29, 2025
# This module handles input+output

import os
import time


# Colors
BLACK = "\033[0;30m"
RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"
BLUE = "\033[0;34m"
PURPLE = "\033[0;35m"
CYAN = "\033[0;36m"
WHITE = "\033[0;37m"
# I used the rgb trick for these colors
GREY = "\033[38;5;240m"
ORANGE = "\033[38;5;208m"


# print(msg, end="") but in black
def black(msg: str = ""):
    print(BLACK + msg, end="")


# print(msg, end="") but in red
def red(msg: str = ""):
    print(RED + msg, end="")


# print(msg, end="") but in green
def green(msg: str = ""):
    print(GREEN + msg, end="")


# print(msg, end="") but in yellow
def yellow(msg: str = ""):
    print(YELLOW + msg, end="")


# print(msg, end="") but in blue
def blue(msg: str = ""):
    print(BLUE + msg, end="")


# print(msg, end="") but in purple
def purple(msg: str = ""):
    print(PURPLE + msg, end="")


# print(msg, end="") but in cyan
def cyan(msg: str = ""):
    print(CYAN + msg, end="")


# print(msg, end="") but in white
def white(msg: str = ""):
    print(WHITE + msg, end="")


# print(msg, end="") but in grey
def grey(msg: str = ""):
    # I need flush=True for this because Im using it in pause()
    print(GREY + msg, end="", flush=True)


# print(msg, end="") but in orange
def orange(msg: str = ""):
    print(ORANGE + msg, end="")


# Function that gets the player's decision
def get_decision(question: str, decisions: list) -> str:
    while True:
        # Display question
        cyan(question)
        # Get user input [WHITE]
        white()
        choice = input()
        # Check if the choice is in the list of possible decisions
        # using .upper() to ensure case-insensitivity
        if choice.upper() in decisions:
            # Return the selected choice
            return choice.upper()
        else:
            # Invalid Input
            red("Invalid decision, try again.\n")


# Clears the terminal
def clear_terminal():
    os.system("clear")


# Function for pausing the terminal
# Used for allowing the read to read the effects
# Also acts as a downtime between events
def pause():
    grey("Continue in [")
    # 2 seconds long [1.5 + 0.5]
    for half_second in range(3):
        # Halt the program for half a second
        time.sleep(0.5)
        # Display a progress marker
        grey("#")
    time.sleep(0.5)
    # Close off progress bar
    grey("]\n")
    # Give user a signal to continue
    yellow("Press enter to continue >>>")
    # Pause will end once user presses enter
    # Since we are using input()
    input()


# DISPLAYS THE TITLE
def display_title():
    yellow("##################################\n")
    yellow("######## Merge the Numbers ########\n")
    yellow("##################################\n")
