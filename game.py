# importing important things
import sys
import os
import time
from random import *

# no hecking clue what this does. you put it there and it's been there since the dawn of time
screen_width = 100

# These are player variables. player_name only changes after the setup_name() command. equipped companion is the number of the current companion in use.
# It can be changed while in a city. Check the git folder for the companions.txt file for all info on companions including their number, their ability, and
# their attack. Unlike a player weapon, companions can only deal flat damage. I preset some of the companion abilities already, including the enemy abilities
# too. The var companions is a list, containing all the companions you have gotten along your journeys. It can be extended with the py command:
# companions.append(x), where x is the number of the companion. player_max_hp is what it says it is. The player's max hp. It can be increased by buying
# shields, which also give a block command (check battle() for the details). player_hp is the current hp the player is sitting at. weapon_type is the
# current weapon the player is using. It is called upon when battle() occurs. It is an int var and it can be changed by buying weapons from a shop, or
# some journey or hunt drops. It is like the companions, each number is a different weapon. I might create a txt file to list those weapons too later.
# Unlike companions, they don't have a list to store the separate weapons. Once it is equipped, it stays, and the last weapon is destroyed.
# shield_type is the exact same thing as weapon_type except with shields. don't worry about shield_boost. It is only called in battle() and all code
# regarding shield_boost is already finished. Thinking about it, I might just move shield_boost to the battle() command itself (EDIT: I found out that
# shield_boost is actually the amount of extra max hp the current shield grants. This var can only change when a new shield is equipped). gold is the amount of gold
# you currently have, and it's the currency of the game. The main way you can get it is by killing enemies, which list how much gold they drop. Every
# similar enemy drops a certain amount of gold, so if you want to make the same enemy drop a different amount of gold, you will have to create a separate
# enemy. Gold can be spent in shops. current_commands are the commands you can use during battle(). The only 3 items that should be on that list are
# "attack", "ability", and "block". Each of those 3 items will be appended to that list along the story. "attack" is added once you pickup the first sword,
# "ability" is added once Flame Knight joins your team, and "block" is added once you have bought a wooden shield. Note that you can't start journey without
# getting a wooden shield. location is not too important. Check in with me if you want to do something with that. travel_commands are the commands
# you can use once you are in a certain town. They might change depending on the town too. journey is the current journey you are on. Once you finish a
# journey, it increases by 1 and you can start the next journey.
player_name = "Isa"
equipped_companion = 0
companions = []
player_max_hp = 20
player_hp = 20
weapon_type = 0
shield_type = 0
shield_boost = 0
gold = 0
current_commands = []
location = ""
travel_commands = []
travel_destinations = ["earth"]
journey = 1

text_speed_multiplier = 1
wait_speed_multiplier = 1

save_file = 0

# These are the enemy variables. They are all lists with 7 variables within. Name is a string, and it is the name of the enemy. It can be the same as another
# enemy too. HP is how much hp they have. Simple. minATK and maxATK are the damage vars. Each battle, it will choose a number between minATK and maxATK.
# ability is the enemy's ability. I have already preset some abilities already, as the abilities are quite tedious to make and require a bit of ctrl c + ctrl v
# dodgeChance is the chance that it might dodge your attack. After you use the command "attack", a number between 0 and 100 generates and if the number is
# bigger than dodgeChance, then your attack will miss. goldDrop is a flat number of gold that the enemy drops once defeated.
# enemy = ["Name", HP, minATK, maxATK, ability, dodgeChance, goldDrop]
worm = ["Worm", 10, 2, 2, 0, 0, 5]
earth_knight = ["Earth Knight", 20, 3, 4, 0, 0, 15]
dirt_elemental = ["Dirt Elemental", 15, 3, 3, 0, 0, 10]
earth_boar = ["Earth Boar", 30, 4, 6, 0, 5, 25]
rock_monster = ["Rock Monster", 75, 7, 10, 0, 0, 80]
giant_toad = ["Giant Toad", 100, 8, 10, 0, 0, 100]
sea_hydra = ["Sea Hydra", 150, 9, 13, 0, 0, 150]
flying_whale = ["Flying Whale", 300, 14, 16, 0, 2, 225]
minotaur = ["Minotaur", 40, 4, 6, 0, 0, 35]
impish_demon = ["Impish Demon", 35, 4, 7, 0, 3, 35]
galatigos_lackey = ["Galatigos Lackey", 50, 5, 6, 0, 0, 50]
lithosphere_mage = ["Lithosphere Mage", 100, 4, 4, 1, 5, 100]
saturn_marcher = ["Saturn Marcher", 120, 12, 16, 0, 2, 150]
universe_paladin = ["Universe Paladin", 150, 14, 20, 0, 3, 200]
planet_shaper = ["Planet Shaper", 200, 16, 21, 1, 3, 300]
universe_darkness = ["Universe Darkness", 275, 17, 20, 1, 3, 500]
mooncaster_pontifex = ["Mooncaster Pontifex", 400, 25, 25, 2, 3, 800]
demon_scout1 = ["Demon Scout", 300, 16, 20, 0, 5, 600]
demon_raider1 = ["Demon Raider", 350, 18, 24, 0, 6, 700]

# the dialogue method used in the storytesting.py file
story = open("gamestory.txt", "r")
indexing_char = "~"
filtering_count = "lol ok"
currently_accessing = 0

dialogue = {}
partition = ""

while filtering_count != " ":
    filtering_count = story.readline().replace("\n", "").strip()
    if indexing_char in filtering_count and filtering_count.find(indexing_char) == 0:
        partition = filtering_count.replace(indexing_char, "").strip()
        # print(partition)
        if partition == "end":
            filtering_count = " "
            break
        else:
            try:
                currently_accessing = filtering_count[1] + filtering_count[2] + filtering_count[3] + filtering_count[4]
            except IndexError:
                currently_accessing = filtering_count[1] + filtering_count[2]
            finally:
                dialogue[partition] = ""
    else:
        if dialogue[partition] == "":
            dialogue[partition] = filtering_count
        else:
            dialogue[partition] = dialogue[partition] + "\n" + filtering_count


def setup_name(saved):
    global player_name
    if not saved:
        print("Type your name. Leave blank for the default name.")
        player_name = input(">")
        if player_name.lower().strip() == "":
            player_name = "Isa"


# You made this for the start screen, so you don't need to change it. I made get_command() based on the play and quit command get.
# noinspection PyTypeChecker,PyTypeChecker
def title_screen():
    global save_file
    global player_name
    global equipped_companion
    global companions
    global player_max_hp
    global player_hp
    global weapon_type
    global shield_type
    global shield_boost
    global gold
    global current_commands
    global location
    global travel_commands
    global travel_destinations
    global journey
    print("█" * 16)
    print("█ Mini Fantasy █")
    print("█   Text Game  █")
    print("█" * 16)
    print("      /| _______________")
    print("O|===|* >_______________>")
    print("      \|")
    print("----------------")
    print("  .:New Game:.   ")
    print("  .:Load Game:.   ")
    print("  .:Settings:.   ")
    print("    .:Quit:.   ")
    # Allows the player to select menu options, which is case-sensitive.
    menu_commands = ["new game", "load game", "quit", "settings"]
    option = get_command(menu_commands)
    if option.lower() == "new game":
        if os.path.exists("save_file.txt"):
            os.remove("save_file.txt")
        setup_game(dialogue["t0"], 0.045, 1, 1)
    if option.lower() == "quit":
        sys.exit()
    if option.lower() == "load game":
        if os.path.exists("save_file.txt"):
            save_file = open("save_file.txt", "r")
            player_name = save_file.readline().replace("\n", "")
            equipped_companion = int(save_file.readline())
            companions = save_file.readline().replace("[", "").replace("]", "").replace("'", "").split()
            if len(companions) > 1:
                for a in range(len(companions)):
                    companions[a - 1] = int(companions[a - 1].replace(",", ""))
            if len(companions) == 1:
                companions[0] = int(companions[0])
            player_max_hp = int(save_file.readline())
            player_hp = int(save_file.readline())
            weapon_type = int(save_file.readline())
            shield_type = int(save_file.readline())
            shield_boost = int(save_file.readline())
            gold = int(save_file.readline())
            current_commands = save_file.readline().replace("[", "").replace("]", "").replace("'", "").split()
            if len(current_commands) > 1:
                for x in range(len(current_commands)):
                    current_commands[x - 1] = current_commands[x - 1].replace(",", "")
            location = save_file.readline()
            travel_commands = save_file.readline().replace("[", "").replace("]", "").replace("'", "").split()
            if len(travel_commands) > 1:
                for c in range(len(travel_commands)):
                    travel_commands[c - 1] = travel_commands[c - 1].replace(",", "")
            travel_destinations = save_file.readline().replace("[", "").replace("]", "").replace("'", "").split()
            if len(travel_destinations) > 1:
                for d in range(len(travel_destinations)):
                    travel_destinations[d - 1] = travel_destinations[d - 1].replace(',', '')
            journey = int(save_file.readline())
            save_file.close()
            setup_name(True)
            print("Load in which city?")
            print(travel_destinations)
            destination = get_command(travel_destinations)
            enter_city(destination.capitalize())
        else:
            setup_game(dialogue["t0"], 0.045, 1, 1)
    if option.lower() == "settings":
        global text_speed_multiplier
        global wait_speed_multiplier
        print("Text Speed Multiplier: x" + str(text_speed_multiplier))
        print("Wait Speed Multiplier: x" + str(wait_speed_multiplier))
        print("Change Text Speed Multiplier?")
        try:
            text_speed_multiplier = float(input("> "))
        except ValueError:
            print("Has been set to the default value.")
            text_speed_multiplier = 1
        print("Change Wait Speed Multiplier?")
        try:
            wait_speed_multiplier = float(input("> "))
        except ValueError:
            print("Has been set to the default value.")
            wait_speed_multiplier = 1
        print("Text Speed Multiplier is now " + str(text_speed_multiplier))
        print("Wait Speed Multiplier is now " + str(wait_speed_multiplier))
        time.sleep(1)
        os.system('cls')
        title_screen()


# setup_game() takes in 4 variables. The story, which is the story var you want to be reading through are the lists that I shown above. text_speed is the time
# in between each character which is typed out. The base speed is usually 0.05. wait_time is the time in between each line. You can increase this for a more
# dramatic effect. output is called upon at the end, and if the output is a certain number than the output might do different things.
def setup_game(story_x, text_speed, wait_time, output):
    global player_name
    global text_speed_multiplier
    global wait_speed_multiplier
    print("\n")
    current_dialogue = story_x.format(player_name)
    for char in current_dialogue:
        sys.stdout.write(char)
        sys.stdout.flush()
        if char == "\n":
            time.sleep(wait_time * wait_speed_multiplier)
        else:
            time.sleep(text_speed * text_speed_multiplier)
    sys.stdout.write("\n")
    # he said it couldn't be done
    if output == 1:
        print("█" * 25)
        print("█ The adventure begins! █")
        print("█" * 25)
        time.sleep(2)
        setup_game(dialogue["t1"], 0.06, 1.5, 2)
    if output == 2:
        global weapon_type
        print("Type \"Pickup\" to pickup the sword.")
        sword_check = input(">")
        if sword_check.lower() == "pickup":
            setup_game("You have picked up sword!\n It has automatically been equipped.", 0.04, 0.5, 0)
            current_commands.append("attack")
            weapon_type = 1
            setup_game(dialogue["t2"], 0.05, 0.75, 3)
        while sword_check.lower() != "pickup":
            print("Type \"Pickup\" to pickup the sword.")
            sword_check = input(">")
            if sword_check.lower() == "pickup":
                setup_game("You have picked up sword!\n It has automatically been equipped.", 0.04, 0.5, 0)
                current_commands.append("attack")
                weapon_type = 1
                setup_game(dialogue["t2"], 0.05, 0.75, 3)
    if output == 3:
        print("Tip: When using a command, make sure you spell the command properly. Or else nothing will happen.")
        enter_battle(worm, 1)
    if output == 4:
        setup_name(False)
        setup_game(dialogue["t4"], 0.05, 0.5, 5)
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
        print(
            "Welcome to Earth Kingdom! Take some time to settle in, hunt, and get better equipment. Start by going to the shop and buying a" +
            " wooden shield. It increases max health and gives the \"block\" command.")
        global location
        enter_city("Earth")
    if output == 7:
        directions = ["left", "right"]
        going = get_command(directions)
        if going == "left":
            setup_game(dialogue["j1pl"], 0.05, 0.5, 8)
        if going == "right":
            setup_game(dialogue["j1pr"], 0.05, 0.5, 9)
    if output == 8:
        enter_battle(minotaur, 4)
    if output == 9:
        enter_battle(impish_demon, 4)
    if output == 10:
        enter_battle(galatigos_lackey, 5)
    if output == 11:
        heal(50)
    if output == 12:
        enter_battle(galatigos_lackey, 6)
    if output == 13:
        enter_battle(lithosphere_mage, 7)
    if output == 14:
        enter_battle(saturn_marcher, 8)
    if output == 15:
        enter_battle(universe_paladin, 9)
    if output == 16:
        enter_battle(planet_shaper, 10)
    if output == 17:
        enter_battle(universe_darkness, 11)
    if output == 18:
        heal(1000)
        enter_battle(mooncaster_pontifex, 12)


# enter_city takes in only 1 var, which must be a string. If that string is a certain city's name then you will enter that city.
# for now, I only have Earth Kingdom. Check out the code on enter_city() a bit. You will understand more schematics of the game.
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
    global journey
    global shield_boost
    location = loc
    print("\nGold: " + str(gold) + "       Kingdom: " + location + "      Health: " + str(player_hp) + "/" + str(
        player_max_hp))
    if location == "Earth":
        travel_commands = ["shop", "medic", "hunt", "journey", "companions", "travel", "save"]
    if location == "Water":
        travel_commands = ["shop", "medic", "hunt", "journey", "companions", "travel", "save"]
    print("Commands:")
    print(travel_commands)
    command = get_command(travel_commands)
    if command.lower() == "shop":
        enter_shop(location)
    if command.lower() == "medic":
        heal("max")
        enter_city(location)
    if command.lower() == "hunt":
        begin_hunt(location)
    if command.lower() == "companions":
        swap_companions(location)
    if command.lower() == "journey":
        begin_journey()
        enter_city(location)
    if command.lower() == "travel":
        travel_to()
    if command.lower() == "save":
        save_game()
        print("Game has been saved!")
        enter_city(location)


# This is the journey command. You can call it whenever you are in a town. The reason I made it a command was to be able to access it regardless of whatever
# town you are in.
def begin_journey():
    global journey
    os.system('cls')
    if "block" not in current_commands:
        print("Buy a wooden shield before you start journeying!")
        return enter_city("Earth")
    if journey == 1:
        setup_game(dialogue["j1p1"], 0.04, 0.5, 7)
        print("You can now set Aqua Mage as your active companion.")
        companions.append(2)
        journey += 1
        return print("Journey Complete!")
    if journey == 2:
        setup_game(dialogue["j2p1"], 0.05, 0.5, 12)
        journey += 1
        print("You can now travel to Water Kingdom.")
        travel_destinations.append("water")
        return print("Journey Complete!")
    if journey == 3:
        setup_game(dialogue["j3p1"], 0.05, 0.5, 14)
        journey += 1
        print("You can now set Thunder Knight as your active companion.")
        companions.append(3)
        return print("Journey Complete!")
    if journey == 4:
        setup_game(dialogue["j4p1"], 0.05, 0.5, 16)
        journey += 1
        print("You have beaten Mooncaster Pontifex.")
        return print("Journey Complete!")
    if journey == 5:
        setup_game(dialogue["j5p1"], 0.05, 0.5, 19)
        journey += 1
        print("You can now set Inventor as your active companion.")
        companions.append(4)
        return print("Journey Complete!")


# Swaps companions. Same case as begin_journey(). current_city allows the command to exit once the command is done.
def swap_companions(current_city):
    global equipped_companion
    companion_names = ""
    if equipped_companion == 1:
        companion_names = "Flame Knight"
    if equipped_companion == 2:
        companion_names = "Aqua Mage"
    if equipped_companion == 3:
        companion_names = "Thunder Knight"
    if equipped_companion == 4:
        companion_names = "Oro"
    equipped_companion_name = companion_names
    print("Active companion: " + companion_names)
    print("Inactive companions: ")
    for i in range(len(companions)):
        if companions[i] == 1:
            companion_names = "Flame Knight"
        elif companions[i] == 2:
            companion_names = "Aqua Mage"
        elif companions[i] == 3:
            companion_names = "Thunder Knight"
        elif companions[i] == 4:
            companion_names = "Oro"
        print(str(i + 1) + ". " + companion_names)
    print("Type the number of the companion to set it active. Type anything else to close.")
    # i learn a new technique with every passing day
    try:
        swap = int(input("> "))
    except ValueError:
        return enter_city(current_city)
    if int(swap) <= len(companions) and int(swap) != 0:
        companions.append(equipped_companion)
        equipped_companion = companions[int(swap) - 1]
        companions.pop(int(swap) - 1)
        print(equipped_companion_name + " has been swapped out.")
    enter_city(current_city)


def begin_hunt(city):
    preys = []
    if city == "Earth":
        preys.append("dirt elemental")
        preys.append("earth boar")
        preys.append("rock monster")
    if city == "Water":
        preys.append("giant toad")
        preys.append("sea hydra")
        preys.append("flying whale")
    preys.append("leave")
    for x in range(len(preys)):
        print(str(x + 1) + " - " + str(preys[x]).title())
    prey = get_command(preys)
    if prey == "dirt elemental":
        enter_battle(dirt_elemental, 0)
    elif prey == "earth boar":
        enter_battle(earth_boar, 0)
    elif prey == "rock monster":
        enter_battle(rock_monster, 0)
    elif prey == "giant toad":
        enter_battle(giant_toad, 0)
    elif prey == "sea hydra":
        enter_battle(sea_hydra, 0)
    elif prey == "flying whale":
        enter_battle(flying_whale, 0)
    enter_city(city)


def travel_to():
    print("Travel to:")
    print(travel_destinations)
    destination = get_command(travel_destinations)
    enter_city(destination.capitalize())


class Item:
    def __init__(self, name, item_type, item_num, gold_cost, buy_phrase, bought_shield_boost, min_stat, max_stat):
        self.name = name
        self.item_type = item_type
        self.item_num = item_num
        self.gold_cost = gold_cost
        self.buy_phrase = buy_phrase
        self.bought_shield_boost = bought_shield_boost
        self.min_stat = min_stat
        self.max_stat = max_stat

    def do_shop(self):
        global weapon_type
        global shield_type
        global shield_boost
        global gold
        global player_hp
        global player_max_hp
        if gold >= self.gold_cost:
            prev_type = ""
            if self.item_type == "weapon":
                prev_type = "w"
            elif self.item_type == "shield":
                prev_type = "s"
            outcome = swap_item(prev_type, self.item_num)
            if outcome is True:
                print("You have bought " + self.name.title() + ".")
                print(self.buy_phrase)
                gold -= self.gold_cost
            elif not outcome:
                return
            if self.item_type == "weapon":
                weapon_type = self.item_num
            elif self.item_type == "shield":
                shield_type = self.item_num
                shield_boost = self.bought_shield_boost
                player_max_hp = shield_boost + 20
                player_hp = player_max_hp
                if "block" not in current_commands:
                    current_commands.append("block")
            else:
                print("item_type is neither!")
        else:
            print("You need more gold!")


# weapons and shields
default_buy_phrase = "It has been equipped."
s0 = Item("None", "shield", 0, 0, None, 0, 0, 0)
w1 = Item("Rusty Sword", "weapon", 1, 0, None, 0, 3, 5)
s1 = Item("Wooden Shield", "shield", 1, 10, default_buy_phrase, 30, 2, 4)
w2 = Item("Wooden Sword", "weapon", 2, 10, default_buy_phrase, 0, 5, 7)
w3 = Item("Iron Sword", "weapon", 3, 150, default_buy_phrase, 0, 8, 10)
s2 = Item("Iron Shield", "shield", 2, 150, default_buy_phrase, 55, 9, 11)
w4 = Item("Enchanted Staff", "weapon", 4, 350, "Let the power flow within you.", 0, 14, 19)
w5 = Item("Aqua Staff", "weapon", 5, 350, "Let the power flow within you.", 0, 15, 18)
s3 = Item("Heavy Shield", "shield", 3, 400, default_buy_phrase, 105, 14, 17)
w6 = Item("Bloody War Axe", "weapon", 6, 1000, default_buy_phrase, 0, 23, 29)
s4 = Item("Mighty Shield", "shield", 4, 1000, default_buy_phrase, 180, 16, 21)
w7 = Item("Spear of Water", "weapon", 7, 2000, "Drown your enemies out with it.", 0, 27, 37)
s5 = Item("Compound Shield", "shield", 5, 2000, "No enemy shall break this sturdy shield.", 280, 18, 23)


def enter_shop(city):
    global shield_type
    global shield_boost
    global weapon_type
    global player_hp
    global player_max_hp
    global gold
    items = ["wooden shield", "wooden sword"]
    if journey >= 2:
        items.append("iron sword")
        items.append("iron shield")
    if journey >= 3:
        if city == "Earth":
            items.append("enchanted staff")
        if city == "Water":
            items.append("aqua staff")
        items.append("heavy shield")
    if journey >= 4:
        items.append("bloody war axe")
        items.append("mighty shield")
    items.append("leave")
    print("Current items in stock:")
    print("Wooden Shield - 10 gold")
    print("Wooden Sword - 10 gold")
    if journey >= 2:
        print("Iron Sword - 150 gold")
        print("Iron Shield - 150 gold")
    if journey >= 3:
        if city == "Earth":
            print("Enchanted Staff - 350 gold")
        if city == "Water":
            print("Aqua Staff - 350 gold")
        print("Heavy Shield - 400 gold")
    if journey >= 4:
        print("Bloody War Axe - 1000 gold")
        print("Mighty Shield - 1000 gold")
    print("Type \"Leave\" to leave.")
    buy = get_command(items).lower()
    if buy == "wooden shield":
        s1.do_shop()
    if buy == "wooden sword":
        w2.do_shop()
    if buy == "iron sword":
        w3.do_shop()
    if buy == "iron shield":
        s2.do_shop()
    if buy == "enchanted staff":
        w4.do_shop()
    if buy == "aqua staff":
        w5.do_shop()
    if buy == "heavy shield":
        s3.do_shop()
    if buy == "bloody war axe":
        w6.do_shop()
    if buy == "mighty shield":
        s4.do_shop()
    if buy == items[-1]:
        print("Come again!")
    enter_city(city)


def swap_item(prev_type, swap_num):
    global weapon_type
    global shield_type
    global shield_boost
    prev_num = 0
    item_type = ""
    if prev_type == "w":
        prev_num = weapon_type
        item_type = "Attack"
    elif prev_type == "s":
        prev_num = shield_type
        item_type = "Block"
    exec("print(" + prev_type + str(prev_num) + ".name + ' => ' + " + prev_type + str(swap_num) + ".name)")
    exec("print('Min " + item_type + ": ' + str(" + prev_type + str(
        prev_num) + ".min_stat) + ' => ' + str(" + prev_type + str(swap_num) + ".min_stat))")
    exec("print('Max " + item_type + ": ' + str(" + prev_type + str(
        prev_num) + ".max_stat) + ' => ' + str(" + prev_type + str(swap_num) + ".max_stat))")
    if prev_type == "s":
        exec("print('Max Health: ' + str(int(" + prev_type + str(
            prev_num) + ".bought_shield_boost) + 20) + ' => ' + str(int(" + prev_type + str(
            swap_num) + ".bought_shield_boost) + 20))")
    # assume prev_type = s, prev_num = 1, swap_num = 2
    # print(s1.name + ' => ' + s2.name)
    # print('Min Block: ' + str(s1.min_stat) + ' => ' + str(s2.min_stat))
    # print('Max Block: ' + str(s1.max_stat) + ' => ' + str(s2.max_stat))
    # print('Max Health: ' + str(int(s1.bought_shield_boost) + 20) + ' => ' + str(int(s2.bought_shield_boost) + 20))
    commands = ["equip", "cancel"]
    print(commands)
    command = get_command(commands)
    if command == "equip":
        if prev_type == "w":
            weapon_type = swap_num
        if prev_type == "s":
            shield_type = swap_num
        return True
    elif command == "cancel":
        return False


# get_command() takes in a list. It will ask for a command, and if the command is in the list then it will return the command typed out. 2 rules when using
# the get_command() function. 1. Do not use this if you don't NEED to type a command. 2. Always set a var as this command, as it returns a string.
# ex: example_var = get_command(["yes", "no"])
# if example_var == "yes":
#   do_something()
def get_command(commands):
    command = input("> ")
    if command.lower() in commands:
        return command.lower()
    while command not in commands:
        print("Invalid Command!")
        command = input(">")
        if command.lower() in commands:
            return command.lower()


def save_game():
    global save_file
    global player_name
    if os.path.exists("save_file.txt"):
        os.remove("save_file.txt")
    save_file = open("save_file.txt", "w")
    save_file.write(
        player_name + "\n" + str(equipped_companion) + "\n" + str(companions) + "\n" + str(player_max_hp) + "\n" + str(
            player_hp) + "\n" +
        str(weapon_type) + "\n" + str(shield_type) + "\n" + str(shield_boost) + "\n" + str(gold) + "\n" + str(
            current_commands) + "\n" +
        location + "\n" + str(travel_commands) + "\n" + str(travel_destinations) + "\n" + str(journey))
    save_file.close()
    print(player_name)


# vars for battle()
minATK = 0
maxATK = 0
min_block = 0
max_block = 0
companion_name = ""
companion_ATK = 0
companion_ability = 0


# The battle() command is the most complicated of them all. First, it lists a bunch of variables. Then, it asks you for a command
# with command = get_command(current_commands). If a certain command is chosen, it will do certain things and then passes the turn to the enemy.
# During the enemy's turn, it will attack you once and use it's ability(I haven't coded much of it yet so maybe I'll do it later). Then it repeats if
# the player dies or the enemy dies. I haven't setup a system if the player dies yet, so for now, it just exits the game.
# ALSO DO NOTICE!!! DO NOT CALL OUT THIS COMMAND. THERE IS A COMMAND THAT DOES IT FOR YOU. CHECK THE COMMAND BELOW.
def battle(enemy, output):
    # all vars
    global player_hp
    global player_max_hp
    global current_commands
    global weapon_type
    global shield_type
    global equipped_companion
    global gold
    global minATK
    global maxATK
    global companion_ATK
    global companion_name
    global companion_ability
    print("\n")
    global min_block
    global max_block
    blocked_damage = 0
    companion_boost = 0
    ability_cooldown = 0
    current_cooldown = 0
    enemy_name = enemy[0]
    enemy_hp = enemy[1]
    enemy_minATK = enemy[2]
    enemy_maxATK = enemy[3]
    enemy_ability = enemy[4]
    enemy_dodge_chance = enemy[5]
    enemy_gold_drop = enemy[6]
    enemy_extra_damage = 0
    permanent_block = 0
    # weapons
    ATK_change = 'global minATK; global maxATK; minATK = w' + str(weapon_type) + '.min_stat\nmaxATK = w' + str(
        weapon_type) + '.max_stat'
    exec(ATK_change.strip())
    # shields
    if shield_type > 0:
        shield_change = "global min_block; global max_block; min_block=s" + str(
            shield_type) + ".min_stat\nmax_block=s" + str(shield_type) + ".max_stat"
        exec(shield_change)
    # companions
    companion_stats = ["companion_name = 'Flame Knight'\n"  # 1
                       "companion_ATK = 4\n"
                       "companion_ability = 1",
                       "companion_name = 'Aqua Mage'\n"  # 2
                       "companion_ATK = 18\n"
                       "companion_ability = 2",
                       "companion_name = 'Thunder Knight'\n"  # 3
                       "companion_ATK = 35\n"
                       "companion_ability = 3",
                       "companion_name = 'Oro'\n"  # 4
                       "companion_ATK = 0\n"
                       "companion_ability = 4"]
    if equipped_companion != 0:
        exec("global companion_name;global companion_ATK; global companion_ability;" + companion_stats[
            equipped_companion - 1])
        # print(companion_stats[equipped_companion - 1])
    combat_start = randint(1, 5)
    start_text = ""
    if combat_start == 1:
        start_text = enemy_name + " would like to fight!"
    if combat_start == 2:
        start_text = enemy_name + " challenges you to a fight!"
    if combat_start == 3:
        start_text = enemy_name + " will fight you!"
    if combat_start == 4:
        start_text = "Get ready to fight " + enemy_name + "!"
    if combat_start == 5:
        start_text = "You will fight " + enemy_name + "!"
    for char in start_text:
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
    if command.lower() == "block":
        blocked_damage = randint(min_block, max_block)
        print("You blocked " + str(blocked_damage) + " damage!")
    if command.lower() == "ability":
        if enemy_ability != 2:
            ability = ""
            dmg = 0
            if companion_ability == 1:
                print("Flame Enhancement!")
                companion_boost += 3
                ability = "ATK_boost"
            if companion_ability == 2:
                print("Aqua Surge!")
                heal(8)
            if companion_ability == 3:
                print("Lightning Strike!")
                enemy_hp -= 60
                ability = "Damage"
                dmg = 60
            if companion_ability == 4:
                using_ability = randint(0, 5)
                if using_ability == 0:
                    using_ability = randint(0, 5)
                    while using_ability == 0:
                        using_ability = randint(0, 5)
                if using_ability == 1:
                    print("Evolution Burst!")
                    companion_ATK += 10
                    ability = "companion_boost"
                elif using_ability == 2:
                    print("Disarm!")
                    permanent_block += 8
                    ability = "permanent_block_increase"
                elif using_ability == 3:
                    print("Influx!")
                    heal(30)
                elif using_ability == 4:
                    print("Pulse!")
                    if player_hp < 10:
                        print("You don't have enough health to use this ability!")
                        return
                    player_hp -= 10
                    print("You took 10 damage!")
                    companion_boost += 20
                    ability = "ATK_boost"
                elif using_ability == 5:
                    print("Power Gauntlet!")
                    enemy_hp -= 100
                    dmg = 100
                    ability = "Damage"
            current_cooldown = ability_cooldown + 1
            if ability == "ATK_boost":
                print(companion_name + " has boosted your attack by " + str(companion_boost) + "!")
            if ability == "Damage":
                print(companion_name + " dealt " + str(dmg) + " damage!")
            if ability == "companion_boost":
                print(companion_name + " boosted their own attack to " + str(companion_ATK) + "!")
            if ability == "permanent_block_increase":
                print(companion_name + " has crippled " + enemy_name + " by " + str(permanent_block))
        else:
            print(enemy_name + " has negated the ability's activation.")
    if enemy_hp <= 0:
        print("You have defeated " + enemy_name + "!")
        print("You earned " + str(enemy_gold_drop) + " gold.")
        gold += enemy_gold_drop
        return output
    while enemy_hp > 0:
        if enemy_ability == 1:
            enemy_extra_damage += 2
            print(enemy_name + " has boosted their attack by " + str(enemy_extra_damage))
        enemy_damage = (randint(enemy_minATK, enemy_maxATK) - blocked_damage - permanent_block) + enemy_extra_damage
        if enemy_damage < 0:
            enemy_damage = 0
        player_hp = player_hp - enemy_damage
        if current_cooldown > 0:
            current_cooldown -= 1
        print(enemy_name + " attacked you for " + str(enemy_damage) + " damage!")
        if player_hp <= 0:
            print("You have died!")
            time.sleep(2)
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
            if command.lower() == "block":
                blocked_damage = randint(min_block, max_block)
                print("You blocked " + str(blocked_damage) + " damage!")
            if command.lower() == "ability":
                if enemy_ability != 2 and current_cooldown == 0:
                    dmg = 0
                    ability = ""
                    if companion_ability == 1:
                        print("Flame Enhancement!")
                        companion_boost += 3
                        ability = "ATK_boost"
                    if companion_ability == 2:
                        print("Aqua Surge!")
                        heal(8)
                    if companion_ability == 3:
                        print("Lightning Strike!")
                        enemy_hp -= 60
                        dmg = 60
                        ability = "Damage"
                    if companion_ability == 4:
                        using_ability = randint(0, 5)
                        if using_ability == 0:
                            using_ability = randint(0, 5)
                            while using_ability == 0:
                                using_ability = randint(0, 5)
                        if using_ability == 1:
                            print("Evolution Burst!")
                            companion_ATK += 10
                            ability = "companion_boost"
                        elif using_ability == 2:
                            print("Disarm!")
                            permanent_block += 8
                            ability = "permanent_block_increase"
                        elif using_ability == 3:
                            print("Influx!")
                            heal(30)
                        elif using_ability == 4:
                            print("Pulse!")
                            if player_hp < 10:
                                print("You don't have enough health to use this ability!")
                                return
                            player_hp -= 10
                            print("You took 10 damage!")
                            companion_boost += 20
                            ability = "ATK_boost"
                        elif using_ability == 5:
                            print("Power Gauntlet!")
                            enemy_hp -= 100
                            dmg = 100
                            ability = "Damage"
                    if ability == "ATK_boost":
                        print(companion_name + " has boosted your attack by " + str(companion_boost) + "!")
                    current_cooldown = ability_cooldown + 1
                    if ability == "Damage":
                        print(companion_name + " dealt " + str(dmg) + " damage!")
                    if ability == "companion_boost":
                        print(companion_name + " boosted their own attack to " + str(companion_ATK) + "!")
                    if ability == "permanent_block_increase":
                        print(companion_name + " has crippled " + enemy_name + " by " + str(permanent_block))
                else:
                    if enemy_ability == 2:
                        print(enemy_name + " has negated the ability's activation.")
                    else:
                        print("Wait " + str(current_cooldown) + " more turns to use that ability!")
            if enemy_hp <= 0:
                print("You have defeated " + enemy_name + "!")
                print("You earned " + str(enemy_gold_drop) + " gold.")
                gold += enemy_gold_drop
                return output


# enter_battle() starts the battle and takes in 2 vars. The first var is the enemy that you will be attacking. The second is the output, which is the same
# as the setup_game() output, only it triggers once the battle is over. If you want to return to Earth Kingdom after battle, use output 3
def enter_battle(enemy, output):
    outcome = battle(enemy, output)
    if outcome == 1:
        setup_game(dialogue["t3"], 0.05, 0.5, 4)
    if outcome == 2:
        setup_game(dialogue["t5"], 0.05, 0.5, 6)
    if outcome == 3:
        enter_city("Earth")
    if outcome == 4:
        setup_game(dialogue["j1p2"], 0.05, 0.5, 10)
    if outcome == 5:
        setup_game(dialogue["j1p3"], 0.05, 0.5, 11)
    if outcome == 6:
        setup_game(dialogue["j2p2"], 0.05, 0.5, 13)
    if outcome == 7:
        setup_game(dialogue["j2p3"], 0.05, 0.5, 0)
    if outcome == 8:
        setup_game(dialogue["j3p2"], 0.05, 0.5, 15)
    if outcome == 9:
        setup_game(dialogue["j3p3"], 0.05, 0.5, 0)
    if outcome == 10:
        setup_game(dialogue["j4p2"], 0.05, 0.5, 17)
    if outcome == 11:
        setup_game(dialogue["j4p3"], 0.05, 0.5, 18)
    if outcome == 12:
        setup_game(dialogue["j4p4"], 0.05, 0.5, 0)


# heal() will heal you for a certain amount. player_hp cannot be bigger than player_max_hp.
def heal(healing):
    global player_max_hp
    global player_hp
    heal_statement = ""
    try:
        if int(healing) > 0:
            player_hp += healing
            if player_hp > player_max_hp:
                player_hp = player_max_hp
                heal_statement = "You have been healed " + str(healing) + " and are now at " + str(
                    player_hp) + " health.\n"
    except ValueError:
        if healing == "max":
            player_hp = player_max_hp
            heal_statement = "You have been fully healed and are now at " + str(player_hp) + " health.\n"
    for char in heal_statement:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.01)


title_screen()
time.sleep(100)
