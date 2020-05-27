# importing important things
import cmd
import textwrap
import sys
import os
import time
import random

screen_width = 100

# Game Execution
def title_screen_menu():
    # Allows the player to select menu options, which is case-sensitive.
    option = input("> ")
    if option.lower() == "play":
        setup_game()
    elif option.lower() == "quit":
        sys.exit()
    while option.lower() not in ['play', 'quit']:
        print("Invalid command, please try again")
        option = input("> ")
        if option.lower() == "play":
            setup_game()
        elif option.lower() == "quit":
            sys.exit()


def title_screen():
    print("█" * 16)
    print("█ Mini Fantasy █")
    print("█   Text Game  █")
    print("█" * 16)
    print("     .:Play:.   ")
    print("     .:Quit:.   ")
    title_screen_menu()


def setup_game():
    print("\n")
    story = ["Once upon a time, there was a world named Isuren, which was home to many amazing creatures.\n",
             "Isuren was divided into various kingdoms, each with their own element.\n",
             "Each kingdom's power rests in an elemental crystal, sealed within the kingdom.\n",
             "One day, an elemental crystal was stolen and the kingdom's power slowly faded away.\n",
             "Within a few years, multiple different elemental crystals were stolen and their kingdoms fell.\n",
             "Soon enough, every single kingdom had lost their elemental crystal.\n",
             "Then, a prophecy has been spoken about a young hero, who can find and return the crystals from the thief.\n",
             "Isuren will be saved one day...\n"]
    story_num = int(len(story))
    story_current = 0
    text_speed = 0.045
    while story_current < story_num:
        for char in story[story_current]:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(text_speed)
        time.sleep(1)
        story_current = story_current + 1
    time.sleep(2)
    # he said it couldn't be done

title_screen()
