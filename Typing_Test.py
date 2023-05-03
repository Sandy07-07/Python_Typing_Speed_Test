# This program is return for conducting the Typing test in the Terminal
# The curses package is for conducting actions in the Terminal
# Run the program in the Terminal

import curses
from curses import wrapper
import time
import random


def start_screen(stdscr):
    stdscr.clear()  # Clears the Terminal
    stdscr.addstr("Welcome to the Typing Speed Test !!!")  # Prints in the Terminal with the specified Row and Column
    stdscr.addstr("\nPress any Key to begin the Typing Test !!!")
    stdscr.addstr("\nYou can press Esc anytime to Quit the test !!!")
    stdscr.refresh()  # Refreshes the Terminal
    stdscr.getkey()  # Does not let the screen close automatically and wait for the User for the Input


def display_text(stdscr, target_text, current_text, wpm=0):
    stdscr.addstr(target_text)
    stdscr.addstr(1, 0, f"WPM :- {wpm}")

    for i, char in enumerate(current_text):
        correct_char = target_text[i]
        colour = curses.color_pair(1)
        if char != correct_char:
            colour = curses.color_pair(2)
        stdscr.addstr(0, i, char, colour)


def load_text():
    with open("text.txt", "r") as f:  # To open the text file in read mode
        lines = f.readlines()  # Returns all the lines in the file in a list
        return random.choice(lines).strip()  # Returns a random line and strips the line from unwanted characters


def wpm_test(stdscr):
    target_text = load_text()
    current_text = []
    wpm = 0
    start_time = time.time()
    stdscr.nodelay(True)  # To not delay if key is not entered

    while True:
        time_elapsed = max(time.time() - start_time, 1)  # To not get a Zero division error and set default value 1
        wpm = round((len(current_text) / (time_elapsed / 60)) / 5)  # As a on average each word has 5 characters

        stdscr.clear()
        display_text(stdscr, target_text, current_text, wpm)
        stdscr.refresh()

        if "".join(current_text) == target_text:
            stdscr.nodelay(False)  # To stop the WPM count when the all characters have been taken
            break

        try:
            key = stdscr.getkey()
        except:
            continue

        if ord(key) == 27:  # Its for User to exit the Test using Esc Button
            break

        if key in ("KEY_BACKSPACE", "\b", "\x7f"):  # To check for Backspace
            if len(current_text) > 0:
                current_text.pop()  # To remove the last character when backspace is there
        elif len(current_text) < len(target_text):
            current_text.append(key)  # To stop when there are no more character left in the text


def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # (Pair_ID, Text Colour, Background Colour)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)  # (Pair_ID, Text Colour, Background Colour)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)  # (Pair_ID, Text Colour, Background Colour)

    start_screen(stdscr)

    while True:
        wpm_test(stdscr)
        stdscr.addstr(2, 0, "You completed the Test!! Press any key to continue!!")
        key = stdscr.getkey()

        if ord(key) == 27:
            break


wrapper(main)
