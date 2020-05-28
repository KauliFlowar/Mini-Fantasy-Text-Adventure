# importing important things
import cmd
import textwrap
import sys
import os
import time
import random

screen_width = 100

intro_story = ["Once upon a time, there was a world named Isuren, which was home to many amazing creatures.\n",
               "Isuren was divided into various kingdoms, each with their own element.\n",
               "Each kingdom's power rests in an elemental crystal, sealed within the kingdom.\n",
               "One day, an elemental crystal was stolen and the kingdom's power slowly faded away.\n",
               "Within a few years, multiple different elemental crystals were stolen and their kingdoms fell.\n",
               "Soon enough, every single kingdom had lost their elemental crystal.\n",
               "Then, a prophecy has been spoken about a young hero, who can find and return the crystals from the thief.\n",
               "Isuren will be saved one day...\n"]

tutorial_story = ["I open my eyes.\n",
                  "I feel as if they have been closed for eternity.\n",
                  "Where am I...?\n"]


def title_screen():
    print("█" * 16)
    print("█ Mini Fantasy █")
    print("█   Text Game  █")
    print("█" * 16)
    print("    .:Play:.   ")
    print("    .:Quit:.   ")
    # Allows the player to select menu options, which is case-sensitive.
    option = input("> ")
    if option.lower() == "play":
        setup_game(intro_story, 0.045, 1, 1)
    elif option.lower() == "quit":
        sys.exit()
    while option.lower() not in ['play', 'quit']:
        print("Invalid command, please try again")
        option = input("> ")
        if option.lower() == "play":
            setup_game(intro_story, 0.045, 1, 1)
        elif option.lower() == "quit":
            sys.exit()


def setup_game(story, text_speed, wait_time, output):

    print("\n")
    story_num = int(len(story))
    story_current = 0
    while story_current < story_num:
        for char in story[story_current]:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(text_speed)
        time.sleep(wait_time)
        story_current = story_current + 1
    print("\n")
    # he said it couldn't be done
    if output == 1:
        print("█" * 25)
        print("█ The adventure begins! █")
        print("█" * 25)
        time.sleep(2)
        setup_game(tutorial_story, 0.06, 1.5, 2)

title_screen()

print("\n")
print("Location: ???     Kingdom: Earth")
print("Map Legend:           ")
print("@ you              |.|")
print(". path             |.|")
print("-| wall            |@|")
print("? battle           ---")
print("\n")
print("You find yourself in a strange place, surrounded\nby many trees")
print("\n")
print("To move,\ntype n(north), s(south),\ne(east), or w(west).\nYou can only move where there is a path.")

