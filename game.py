# importing important things
import cmd
import textwrap
import sys
import os
import time
from random import *

screen_width = 100

player_name = "Isa"
equipped_companion = 0
companions = []
player_max_hp = 20
player_hp = 20
weapon_type = 0
shield_type = 0
gold = 0
current_commands = []
location = ""
travel_commands = []

# enemy = ["Name", HP, minATK, maxATK, ability, dodgeChance, gold drop]
worm = ["Worm", 10, 2, 2, 0, 0, 5]
earth_knight = ["Earth Knight", 20, 3, 4, 0, 0, 15]
dirt_elemental = ["Dirt Elemental", 15, 3, 3, 0, 0, 10]
earth_boar = ["Earth Boar", 30, 4, 6, 0, 5, 25]
rock_monster = ["Rock Monster", 75, 7, 10, 0, 0, 80]

intro_story = ["Once upon a time, there was a world named Isuren, which was home to many amazing creatures.",
               "Isuren was divided into various kingdoms, each with their own element.",
               "Each kingdom's power rests in an elemental crystal, sealed within the kingdom.",
               "One day, an elemental crystal was stolen and the kingdom's power slowly faded away.",
               "Within a few years, multiple different elemental crystals were stolen and their kingdoms fell.",
               "Soon enough, every single kingdom had lost their elemental crystal.",
               "Then, a prophecy has been spoken about a young hero, who can find and return the crystals from the thief.",
               "Isuren will be saved one day..."]

tutorial_story = ["I open my eyes.",
                  "I feel as if they have been closed for an eternity.",
                  "Where am I...?\n",
                  "I see a sword right in front of me.",
                  "I guess I have no choice but to take it, as it is my only defence out here."]

tutorial_story2 = ["Suddenly, a hissing sound came from a bush",
                   "A worm comes out of the bush and jumps at me",
                   "I guess I have no choice but to fight it!"]

tutorial_story3 = ["The worm fled me.",
                   "I guess I'm ok for now.\n",
                   "I make my way navigating the forest. It wasn't easy.",
                   "I was starving. I didn't think it was possible to escape anymore.",
                   "Then I hear a voice...",
                   "\"Who's there? Come out now.\"",
                   "I take a peak. It was a knight in red armor. He must be from the Fire Kingdom.",
                   "He spots me and looks surprised.",
                   "\"It's ok\", he says. \"I'm not here to hurt you.\"",
                   "I come out. \"Hello\" was all I could say to him.",
                   "\"What's your name?\", he asks.",
                   "My name? My name is..."]
tutorial_story4 = []
tutorial_story5 = []


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
    global player_name
    print("\n")
    story_num = int(len(story))
    story_current = 0
    while story_current < story_num:
        for char in story[story_current]:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(text_speed)
        time.sleep(wait_time)
        sys.stdout.write("\n")
        story_current = story_current + 1
    print("\n")
    # he said it couldn't be done
    if output == 1:
        print("█" * 25)
        print("█ The adventure begins! █")
        print("█" * 25)
        time.sleep(2)
        setup_game(tutorial_story, 0.06, 1.5, 2)
    if output == 2:
        global weapon_type
        print("Type \"Pickup\" to pickup the sword.")
        sword_check = input(">")
        if sword_check.lower() == "pickup":
            setup_game(["You have picked up sword!", "It has automatically been equipped."], 0.04, 0.5, 0)
            current_commands.append("attack")
            weapon_type = 1
            setup_game(tutorial_story2, 0.05, 0.75, 3)
        while sword_check.lower() != "pickup":
            print("Type \"Pickup\" to pickup the sword.")
            sword_check = input(">")
            if sword_check.lower() == "pickup":
                setup_game(["You have picked up sword!", "It has automatically been equipped."], 0.04, 0.5, 0)
                current_commands.append("attack")
                weapon_type = 1
                setup_game(tutorial_story2, 0.05, 0.75, 3)
    if output == 3:
        print("Tip: When using a command, make sure you spell the command properly. Or else nothing will happen.")
        enter_battle(worm, 1)
    if output == 4:
        setup_name()
        setup_game(tutorial_story4, 0.05, 0.5, 5)
    if output == 5:
        global equipped_companion
        heal(20)
        print("Flame Knight is now your companion. You can use his ability to boost your attack by 2!")
        equipped_companion = 1
        current_commands.append("ability")
        print("Type anything to continue...")
        input(">")
        os.system('cls')
        enter_battle(earth_knight, 2)
    if output == 6:
        global location
        enter_city("Earth")


def enter_city(loc):
    global weapon_type
    global shield_type
    global location
    global travel_commands
    global player_hp
    global player_max_hp
    global gold
    global equipped_companion
    global companions
    location = loc
    print("\nGold: " + str(gold) + "       Kingdom:" + location)
    if location == "Earth":
        travel_commands = ["shop", "medic", "hunt", "journey", "companions"]
        print("Commands:")
        print(travel_commands)
        command = get_command(travel_commands)
        if command.lower() == "shop":
            items = ["wooden shield", "wooden sword", "leave"]
            print("Current items in stock:")
            print("Wooden Shield - 10 gold")
            print("Wooden Sword - 10 gold")
            print("Type \"Leave\" to leave.")
            buy = get_command(items)
            if buy == items[0]:
                if gold >= 10:
                    shield_type = 1
                    player_max_hp += 10
                    player_hp += 10
                    current_commands.append("block")
                    print("You have bought Wooden Shield.")
                    print("It has been automatically equipped.")
                    gold -= 10
                else:
                    print("You need more gold!")
            if buy == items[1]:
                if gold >= 10:
                    weapon_type = 2
                    print("You have bought Wooden Sword.")
                    print("It has been automatically equipped.")
                    gold -= 10
                else:
                    print("You need more gold!")
            if buy == items[-1]:
                print("Come again!")
            enter_city("Earth")
        if command.lower() == "medic":
            heal(100)
            enter_city("Earth")
        if command.lower() == "hunt":
            preys = ["dirt elemental", "earth boar", "rock monster"]
            print("1 - Dirt Elemental")
            print("2 - Earth Boar")
            print("3 - Rock Monster")
            prey = get_command(preys)
            if prey == preys[0]:
                enter_battle(dirt_elemental, 3)
            elif prey == preys[1]:
                enter_battle(earth_boar, 3)
            elif prey == preys[2]:
                enter_battle(rock_monster, 3)
        if command.lower() == "companions":
            companion_name = ""
            if equipped_companion == 1:
                companion_name = "Flame Knight"
            if equipped_companion == 2:
                companion_name = "Aqua Mage"
            print("Active companion: " + companion_name)
            print("Inactive companions: ")
            length = len(companions)
            for i in range(length):
                if companions[i] == 1:
                    companion_name = "Flame Knight"
                elif companions[i] == 2:
                    companion_name = "Aqua Mage"
                print(companion_name)
            enter_city("Earth")


def get_command(commands):
    command = input("> ")
    if command.lower() in commands:
        return command.lower()
    while command not in commands:
        print("Invalid Command!")
        command = input(">")
        if command.lower() in commands:
            return command.lower()


def battle(enemy, output):
    # all vars
    global player_hp
    global player_max_hp
    global current_commands
    global weapon_type
    global shield_type
    global equipped_companion
    global gold
    print("\n")
    blocked_damage = 0
    minATK = 0
    maxATK = 0
    min_block = 0
    max_block = 0
    companion_name = ""
    companion_ATK = 0
    companion_boost = 0
    companion_ability = 0
    enemy_name = enemy[0]
    enemy_hp = enemy[1]
    enemy_minATK = enemy[2]
    enemy_maxATK = enemy[3]
    enemy_ability = enemy[4]
    enemy_dodge_chance = enemy[5]
    enemy_gold_drop = enemy[6]
    enemy_extra_damage = 0
    # weapons
    if weapon_type == 1:
        minATK = 3
        maxATK = 5
        # print(minATK)
    if weapon_type == 2:
        minATK = 5
        maxATK = 7
    # shields
    if shield_type == 1:
        min_block = 2
        max_block = 4
    # companions
    if equipped_companion == 1:
        companion_name = "Flame Knight"
        companion_ATK = 4
        companion_ability = 1
    if equipped_companion == 2:
        companion_name = "Aqua Mage"
        companion_ATK = 18
        companion_ability = 2
    for char in (enemy[0] + " would like to fight!"):
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.03)
    print("\nCommands:")
    print(current_commands)
    command = get_command(current_commands)
    if command.lower() == "attack":
        dodge = randint(0, 100)
        if enemy_dodge_chance > dodge:
            print("You attacked " + enemy_name + " but you missed!")
        else:
            damage = randint(minATK, maxATK) + companion_boost
            enemy_hp = enemy_hp - damage - companion_ATK
            print("You attacked " + enemy_name + " for " + str(damage) + " damage!")
            if equipped_companion != 0:
                print(companion_name + " attacked " + enemy_name + " for " + str(companion_ATK) + " damage!")
            if enemy_hp <= 0:
                print("You have defeated " + enemy_name + "!")
                print("You earned " + str(enemy_gold_drop) + " gold.")
                gold += enemy_gold_drop
                return output
    if command.lower() == "block":
        blocked_damage = randint(min_block, max_block)
        print("You blocked " + str(blocked_damage) + " damage!")
    if command.lower() == "ability":
        if enemy_ability != 2:
            ability = ""
            if companion_ability == 1:
                print("Flame Enhancement!")
                companion_boost += 2
                ability = "ATK_boost"
            if companion_ability == 2:
                print("Aqua Surge!")
                heal(8)
            if ability == "ATK_boost":
                print(companion_name + " has boosted your attack by " + str(companion_boost) + "!")
        else:
            print(enemy_name + " has negated the ability's activation.")
    while enemy_hp > 0:
        if enemy_ability == 1:
            enemy_extra_damage += 5
            print(enemy_name + " has boosted their attack by " + enemy_extra_damage)
        enemy_damage = (randint(enemy_minATK, enemy_maxATK) - blocked_damage) + enemy_extra_damage
        if enemy_damage < 0:
            enemy_damage = 0
        player_hp = player_hp - enemy_damage
        print(enemy_name + " attacked you for " + str(enemy_damage) + " damage!")
        if player_hp <= 0:
            print("You have died!")
            time.sleep(5)
            sys.exit()
        if player_hp > 0:
            print("You have " + str(player_hp) + " health left.")
            print(enemy_name + " has " + str(enemy_hp) + " health left.")
            print("\nCommands:")
            print(current_commands)
            blocked_damage = 0
            command = get_command(current_commands)
            if command.lower() == "attack":
                dodge = randint(0, 100)
                if enemy_dodge_chance > dodge:
                    print("You attacked " + enemy_name + " but you missed!")
                else:
                    damage = randint(minATK, maxATK) + companion_boost
                    enemy_hp = enemy_hp - damage - companion_ATK
                    print("You attacked " + enemy_name + " for " + str(damage) + " damage!")
                    if equipped_companion != 0:
                        print(companion_name + " attacked " + enemy_name + " for " + str(companion_ATK) + " damage!")
                    if enemy_hp <= 0:
                        print("You have defeated " + enemy_name + "!")
                        print("You earned " + str(enemy_gold_drop) + " gold.")
                        gold += enemy_gold_drop
                        return output
            if command.lower() == "block":
                blocked_damage = randint(min_block, max_block)
                print("You blocked " + str(blocked_damage) + " damage!")
            if command.lower() == "ability":
                if enemy_ability != 2:
                    ability = ""
                    if companion_ability == 1:
                        print("Flame Enhancement!")
                        companion_boost += 2
                        ability = "ATK_boost"
                    if companion_ability == 2:
                        print("Aqua Surge!")
                        heal(8)
                    if ability == "ATK_boost":
                        print(companion_name + " has boosted your attack by " + str(companion_boost) + "!")
                else:
                    print(enemy_name + " has negated the ability's activation.")


def enter_battle(enemy, output):
    outcome = battle(enemy, output)
    if outcome == 1:
        setup_game(tutorial_story3, 0.05, 0.5, 4)
    if outcome == 2:
        setup_game(tutorial_story5, 0.05, 0.5, 6)
    if outcome == 3:
        enter_city("Earth")


def heal(healing):
    global player_max_hp
    global player_hp
    player_hp += healing
    if player_hp > player_max_hp:
        player_hp = player_max_hp
    heal_statement = "You have been healed " + str(healing) + " and are now at " + str(player_hp) + " health.\n"
    for char in heal_statement:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.01)


def setup_name():
    global player_name
    global tutorial_story4
    global tutorial_story5
    print("Type your name. Leave blank for the default name.")
    player_name = input(">")
    if player_name.lower() == "":
        player_name = "Isa"
    tutorial_story4 = ["\"" + player_name + "? I've heard that name before. You must be the hero.",
                       "Me? A hero? What does he mean?",
                       "\"Your name was the name that came from a prophecy, which a great mage has foreseen.\"",
                       "he said.\n",
                       "\"I'm a bit lost right now. I have no idea where I am.\", I said.",
                       "\"You are in the Earth Kingdom's forest. I came down here because I heard a person went missing down here.\", he said.",
                       "\"I am Nadrus, the Flame Knight. Pleased to meet you.\"",
                       "He helped guide me out of the forest and gave me some food.\n",
                       "\"Thank you\", I said. \"For everything you've done.\"",
                       "Then another knight appeared. He was from the Earth Kingdom.",
                       "\"Trespassers are not welcome here.\", he grunted.",
                       "Flame Knight looks at you. " + player_name + "! I'll help you fight him off."]
    tutorial_story5 = ["\"Grrr\", he grunts. \"You won't get away next time.\"",
                       "Flame Knight looks at you. \"You fought well " + player_name + "\", he said.",
                       "You look at Flame Knight and Smile."
                       "\"It was nice knowing you. I must go now.\"",
                       "\"" + player_name + "! Wait!\" he said.",
                       "\"If you are the hero of Isuren, let me join you. I'll protect you.\"",
                       "\"Why do want to help me?\", I asked.\n",
                       "You see... Fire Kingdom once lived in peace.",
                       "Ever since the fire crystal was stolen, our power shrank a lot.",
                       "Warring kingdoms would attack us while they still had their crystal.",
                       "Some of our people were tortured. Killed. Or worse.",
                       "I cannot forgive this crystal thief. So I want to help you on this journey, " + player_name + "\n",
                       "\"Alright\", I say. \"You may join me. On the journey to save Isuren...\""]


current_commands.append("attack")
# current_commands.append("block")
current_commands.append("ability")
weapon_type = 1
# shield_type = 1
equipped_companion = 2
enter_city("Earth")
# enter_battle(worm, 1, False)
# title_screen()
time.sleep(100)
