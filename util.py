#!/usr/bin/env python3
# Created By: Atri Sarker
# Date: May 26, 2025
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


def get_color_from_number(num: int):
    # Color variables
    red = 0
    green = 0
    blue = 0
    match num:
        case 0:
            red = 255
            green = 255
            blue = 255
        case 2:
            red = 30
            green = 190
            blue = 70
        case 4:
            red = 255
            green = 203
            blue = 164
        case 8:
            red = 180
            blue = 90
        case 16:
            red = 240
            blue = 160
        case 32:
            red = 50
            blue = 150
        case 64:
            red = 170
            green = 70
            blue = 170
        case 128:
            red = 150
            green = 150
        case 256:
            red = 200
            blue = 50
        case 512:
            red = 220
            blue = 40
        case 1024:
            red = 200
            blue = 200
        case 2048:
            green = 255
            blue = 255
        case 4096:
            red = 255
        case _:
            red = 255
            green = num // 7
    return f"\033[38;2;{red};{green};{blue}m"


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


# DISPLAYS THE TITLE
def display_title():
    yellow("##################################\n")
    yellow("######## Merge the Numbers ########\n")
    yellow("##################################\n")
