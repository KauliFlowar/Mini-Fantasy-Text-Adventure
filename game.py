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
shield_boost = 0
gold = 0
current_commands = []
location = ""
travel_commands = []
journey = 0

# enemy = ["Name", HP, minATK, maxATK, ability, dodgeChance, gold drop]
worm = ["Worm", 10, 2, 2, 0, 0, 5]
earth_knight = ["Earth Knight", 20, 3, 4, 0, 0, 15]
dirt_elemental = ["Dirt Elemental", 15, 3, 3, 0, 0, 10]
earth_boar = ["Earth Boar", 30, 4, 6, 0, 5, 25]
rock_monster = ["Rock Monster", 75, 7, 10, 0, 0, 80]
minotaur = ["Minotaur", 40, 4, 6, 0, 0, 35]
impish_demon = ["Impish Demon", 35, 4, 7, 0, 3, 35]
galatigos_lackey = ["Galatigos Lackey", 50, 5, 6, 0, 0, 50]

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
                   "I look at Flame Knight and Smile."
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
journey1_part1 = ["\"Hey " + player_name + ".\", said Nadrus.",
                  "I look at Nadrus as he holds a piece of paper, smiling.",
                  "\"What's up?\", I respond.",
                  "He smirks and looks at me. \"I think we need more allies, don't you think?\"",
                  "\"Yeah I guess so...\"",
                  "\"I know a friend who can help us. He is from the Water Kingdom.\"",
                  "\"Well we should go get him. No one is willing to leave the Kingdom walls ever since the crystal was stolen, right?\"",
                  "He sighs and looks at the floor. \"You're right. Let's go. Even if there's a chance to die, we need to go.\"\n",
                  "We make our way to a crossroad. Which direction should we go? (Left or Right)"]
journey1_part1left = ["\"Let's go left.\", I say. \"I have a good feeling it's this way.\"",
                      "Nadrus nods and walks ahead to the left road.",
                      "A giant Minotaur walks in front of us. \"You chose the wrong way\", it said."]
journey1_part1right = ["\"Right is always the right way\", I say. \"I just have a feeling it's this way.\"",
                       "Nadrus nods and walks ahead to the right road",
                       "Suddenly, a impish demon pounces on us. \"I might be small, but I pack a punch\", it says as it gnaws on Nadrus's right foot.",
                       "He kicks it off. \"Then show us what you got!\""]
journey1_part2 = ["It fell to the floor and fainted. We pushed it's corpse away and continued along the road.",
                  "\"" + player_name + "!\", Nadrus called out. \"You picked the right way. There's Water Kingdom.\"",
                  "\"Soon you'll meet my friend, Aurus. He is the Aqua Mage.\"",
                  "Aqua Mage? If he is the Aqua Mage, then we would have a healer. I turn to Nadrus.",
                  "\"I'm sure he will be of use.\", I say.\n",
                  "\"Too bad you wont be able to see him\", a figure calls out.",
                  "It walks up to us. It was a person who held a staff of the night sky.",
                  "\"We, the Galatigos, have secured the Water Kingdom.\", he smiles.",
                  "\"Surrender now or beg for mercy from our Pontifex.\"",
                  "Nadrus stands in front of me. \"We have no idea what the Galatigos are, but we are on an important mission, so stay out of our way.\"",
                  "\"I'm afraid I can't do that.\"",
                  "Nadrus pushes him back. \"Then we will fight.\"",
                  "He spins his staff in place. \"Very well then.\""]
journey1_part3 = ["He collapses onto the floor. \"Y-You'll hear from our Pontifex soon enough.\"",
                  "Nadrus pushes him aside and walks into the Water Kingdom.",
                  "\"Aurus, are you out here?\", he calls out.",
                  "A man with eyes of blue steps out of an alley.",
                  "\"Nadrus?\", he calls out. \"It's been a while.\"",
                  "Nadrus nods. \"We need your help. I'm with " + player_name + ". He might be able to help us.\"",
                  "He gasps. \"" + player_name + "? The chosen one?\"",
                  "I smile. \"It's a pleasure to meet you, Aurus.\"",
                  "He shakes your hand and gives a serious face. \"I'll help you.\"",
                  "He sees your wounds on your body. \"You're wounded. I'll heal you up.\""]
journey1_part4 = ["\"Alright then\", I say. \"We should head back to Earth Kingdom.\""]


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
        print(
            "Welcome to Earth Kingdom! Take some time to settle in, hunt, and get better equipment. Start by going to the shop and buying a" +
            " wooden shield. It increases max health and gives the \"block\" command.")
        global location
        enter_city("Earth")
    if output == 7:
        directions = ["left", "right"]
        going = get_command(directions)
        if going == "left":
            setup_game(journey1_part1left, 0.05, 0.5, 8)
        if going == "right":
            setup_game(journey1_part1right, 0.05, 0.5, 9)
    if output == 8:
        enter_battle(minotaur, 4)
    if output == 9:
        enter_battle(impish_demon, 4)
    if output == 10:
        enter_battle(galatigos_lackey, 5)
    if output == 11:
        heal(50)


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
    print("\nGold: " + str(gold) + "       Kingdom:" + location)
    if location == "Earth":
        travel_commands = ["shop", "medic", "hunt", "journey", "companions"]
        print("Commands:")
        print(travel_commands)
        command = get_command(travel_commands)
        if command.lower() == "shop":
            items = ["wooden shield", "wooden sword"]
            if journey >= 1:
                items.append("iron sword")
                items.append("iron shield")
            items.append("leave")
            print("Current items in stock:")
            print("Wooden Shield - 10 gold")
            print("Wooden Sword - 10 gold")
            if journey >= 1:
                print("Iron Sword - 150 gold")
                print("Iron Shield - 150 gold")
            print("Type \"Leave\" to leave.")
            buy = get_command(items).lower()
            if buy == items[0]:
                if gold >= 10:
                    shield_type = 1
                    shield_boost = 30
                    player_max_hp = shield_boost + 20
                    player_hp += shield_boost
                    if "block" not in current_commands:
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
            if buy == "iron sword":
                if gold >= 150:
                    weapon_type = 3
                    print("You have bought Iron Sword.")
                    print("It has been automatically equipped.")
                    gold -= 150
                else:
                    print("You need more gold!")
            if buy == "iron shield":
                if gold >= 150:
                    shield_type = 2
                    shield_boost = 55
                    player_max_hp = shield_boost + 20
                    player_hp += shield_boost
                    if "block" not in current_commands:
                        current_commands.append("block")
                    print("You have bought Iron Shield.")
                    print("It has been automatically equipped.")
                    gold -= 150
                else:
                    print("You need more gold!")
            if buy == items[-1]:
                print("Come again!")
            enter_city("Earth")
        if command.lower() == "medic":
            heal(1000000)
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
            equipped_companion_name = companion_name
            print("Active companion: " + companion_name)
            print("Inactive companions: ")
            length = len(companions)
            for i in range(length):
                if companions[i] == 1:
                    companion_name = "Flame Knight"
                elif companions[i] == 2:
                    companion_name = "Aqua Mage"
                print(str(i + 1) + ". " + companion_name)
            print("Type the number of the companion to set it active. Type anything else to close.")
            swap = ""
            # i learn a new technique with every passing day
            try:
                swap = int(input("> "))
            except ValueError:
                enter_city("Earth")
            if int(swap) <= length:
                companions.append(equipped_companion)
                equipped_companion = companions[int(swap) - 1]
                companions.pop(int(swap) - 1)
                print(equipped_companion_name + " has been swapped out.")
            enter_city("Earth")
        if command.lower() == "journey":
            os.system('cls')
            if "block" not in current_commands:
                print("Buy a wooden shield before you start journeying!")
                return enter_city("Earth")
            journey += 1
            if journey == 1:
                setup_game(journey1_part1, 0.04, 0.5, 7)
                print("You can now set Aqua Mage as your active companion.")
                companions.append(2)
            print("Journey Complete!")
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
        ability_cooldown = 1
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
            current_cooldown = ability_cooldown + 1
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
        if current_cooldown > 0:
            current_cooldown -= 1
        print(enemy_name + " attacked you for " + str(enemy_damage) + " damage!")
        if player_hp <= 0:
            print("You have died!")
            time.sleep(50)
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
                if enemy_ability != 2 and current_cooldown == 0:
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
                    if enemy_ability == 2:
                        print(enemy_name + " has negated the ability's activation.")
                    else:
                        print("Wait " + str(current_cooldown) + " more turns to use that ability!")


def enter_battle(enemy, output):
    outcome = battle(enemy, output)
    if outcome == 1:
        setup_game(tutorial_story3, 0.05, 0.5, 4)
    if outcome == 2:
        setup_game(tutorial_story5, 0.05, 0.5, 6)
    if outcome == 3:
        enter_city("Earth")
    if outcome == 4:
        setup_game(journey1_part2, 0.05, 0.5, 10)
    if outcome == 5:
        setup_game(journey1_part3, 0.05, 0.5, 11)


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
    global journey1_part1
    global journey1_part2
    global journey1_part3
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
                       "I look at Flame Knight and Smile."
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
    journey1_part1 = ["\"Hey " + player_name + ".\", said Nadrus.",
                      "I look at Nadrus as he holds a piece of paper, smiling.",
                      "\"What's up?\", I respond.",
                      "He smirks and looks at me. \"I think we need more allies, don't you think?\"",
                      "\"Yeah I guess so...\"",
                      "\"I know a friend who can help us. He is from the Water Kingdom.\"",
                      "\"Well we should go get him. No one is willing to leave the Kingdom walls ever since the crystal was stolen, right?\"",
                      "He sighs and looks at the floor. \"You're right. Let's go. Even if there's a chance to die, we need to go.\"\n",
                      "We make our way to a crossroad. Which direction should we go? (Left or Right)"]
    journey1_part2 = ["It fell to the floor and fainted. We pushed it's corpse away and continued along the road.",
                      "\"" + player_name + "!\", Nadrus called out. \"You picked the right way. There's Water Kingdom.\"",
                      "\"Soon you'll meet my friend, Aurus. He is the Aqua Mage.\"",
                      "Aqua Mage? If he is the Aqua Mage, then we would have a healer. I turn to Nadrus.",
                      "\"I'm sure he will be of use.\", I say.\n",
                      "\"Too bad you wont be able to see him\", a figure calls out.",
                      "It walks up to us. It was a person who held a staff of the night sky.",
                      "\"We, the Galatigos, have secured the Water Kingdom.\", he smiles.",
                      "\"Surrender now or beg for mercy from our Pontifex.\"",
                      "Nadrus stands in front of me. \"We have no idea what the Galatigos are, but we are on an important mission, so stay out of our way.\"",
                      "\"I'm afraid I can't do that.\"",
                      "Nadrus pushes him back. \"Then we will fight.\"",
                      "He spins his staff in place. \"Very well then.\""]
    journey1_part3 = ["He collapses onto the floor. \"Y-You'll hear from our Pontifex soon enough.\"",
                      "Nadrus pushes him aside and walks into the Water Kingdom.",
                      "\"Aurus, are you out here?\", he calls out.",
                      "A man with eyes of blue steps out of an alley.",
                      "\"Nadrus?\", he calls out. \"It's been a while.\"",
                      "Nadrus nods. \"We need your help. I'm with " + player_name + ". He might be able to help us.\"",
                      "He gasps. \"" + player_name + "? The chosen one?\"",
                      "I smile. \"It's a pleasure to meet you, Aurus.\"",
                      "He shakes your hand and gives a serious face. \"I'll help you.\"",
                      "He sees your wounds on your body. \"You're wounded. I'll heal you up.\""]


# some commands are commented out to skip ahead in progression.
current_commands.append("attack")
current_commands.append("block")
current_commands.append("ability")
weapon_type = 2
shield_type = 2
equipped_companion = 1
player_hp = 50
player_max_hp = 50
# gold = 20
# companions.append(1)
enter_city("Earth")
# enter_battle(worm, 1)
# title_screen()
time.sleep(100)
