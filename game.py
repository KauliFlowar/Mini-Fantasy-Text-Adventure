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
minotaur = ["Minotaur", 40, 4, 6, 0, 0, 35]
impish_demon = ["Impish Demon", 35, 4, 7, 0, 3, 35]
galatigos_lackey = ["Galatigos Lackey", 50, 5, 6, 0, 0, 50]
lithosphere_mage = ["Lithosphere Mage", 100, 4, 4, 1, 5, 100]
saturn_marcher = ["Saturn Marcher", 120, 12, 16, 0, 2, 150]
universe_paladin = ["Universe Paladin", 150, 14, 20, 0, 3, 200]
planet_shaper = ["Planet Shaper", 150, 12, 17, 1, 3, 300]
universe_darkness = ["Universe Darkness", 200, 14, 17, 1, 3, 500]
mooncaster_pontifex = ["Mooncaster Pontifex", 300, 21, 21, 2, 3, 800]

# These are the story lists. Each list has a story, and each line of the story is split into different instances in the list, divided by commas to make another
# line. All stories including the var of player_name must be copy and pasted onto the setup_name() command, so that the name can change. By default the name
# is Isa. Y A  B O I
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
journey1_part1 = []
journey1_part1left = ["\"Let's go left.\", I say. \"I have a good feeling it's this way.\"",
                      "Nadrus nods and walks ahead to the left road.",
                      "A giant Minotaur walks in front of us. \"You chose the wrong way\", it said."]
journey1_part1right = ["\"Right is always the right way\", I say. \"I just have a feeling it's this way.\"",
                       "Nadrus nods and walks ahead to the right road",
                       "Suddenly, a impish demon pounces on us. \"I might be small, but I pack a punch\", it says as it gnaws on Nadrus's right foot.",
                       "He kicks it off. \"Then show us what you got!\""]
journey1_part2 = []
journey1_part3 = []
journey1_part4 = ["\"Alright then\", I say. \"We should head back to Earth Kingdom.\""]
journey2_part1 = []
journey2_part2 = ["Aurus looks at me. \"Jeez, what's his problem?\"",
                  "Nadrus picks up the Galatigos lackey by his neck. \"Don't mess with us again.\" He quickly nods.",
                  "Nadrus throws him to the ground. \"Alright let's start heading to Water Kingdom.\"\n",
                  "We head to Water Kingdom, only to be stopped by a brigade of Galatigos soldiers and mages.",
                  "There was a short mage at the head of the brigade, who held a ginormous stave, disproportionate to her petit size.",
                  "We head up to the brigade, and all the soldiers turn their heads towards us.",
                  "\"Halt!\", the tiny mage calls out. \"You may not enter Water Kingdom. Now turn back and leave!\"",
                  "Aurus takes a step forward. \"Not a chance!\", he yells.",
                  "The mage looks impatient. \"I am Lithosphere Mage, the 22nd Mooncaster. Turn back now or die under my power.\"",
                  "Nadrus also takes a step forward. \"You heard the man! We are not turning back!\"",
                  "The mage follows Nadrus's gaze. \"Very well then...\""]
journey2_part3 = ["The mage falls to her knees. \"I underestimated your power.\"",
                  "The Galatigos soldiers looked shocked at their squadron leader's defeat.",
                  "Aurus looks at all the soldiers' faces and smiles at the mage. \"At least you fought fairly.\"",
                  "The mage looked a little angered at Aurus and stands up.",
                  "\"Consider this a tactical retreat. Be warned of the threats that are coming.\"",
                  "She makes a hand gesture, and all the Galatigos soldiers leave the field.",
                  "The people of Water Kingdom look outside their kingdom gates and looked surprised that the Galatigos have retreated.",
                  "Aurus looks at me. \"Well what are you waiting for? Go inside our amazing kingdom!\""]
journey3_part1 = []
journey3_part2 = ["Nadrus grabs the Mooncaster by her neck and looks at her with murderous intent.",
                  "\"Tell us where the Pontifex is NOW.\"",
                  "\"I don't know, I swear I don't know.\", she struggles.",
                  "Aurus looks intently at her. \"She is telling the truth.\"",
                  "Nadrus knocks her out. \"Come on, let's see if anyone inside knows.\"",
                  "We head on inside and a man gets up from what looks to be a throne and another man tied to a chair.",
                  "\"Do you know where the Pontifex is?\", Aurus asks.",
                  "\"Of course I do\", he says.",
                  "\"As the second hand of the Pontifex, I will not fail.\""]
journey3_part3 = []
journey4_part1 = ["We head to the shrine Universe Paladin told us about.",
                  "\"We need a plan, there are about 20 guards holed up there.\" said Rayden.",
                  "\"I'll make a distraction, so that you guys can break in\", said Aurus.",
                  "\"Ok,\" I said. \"Let's do it.\"",
                  "Aurus went to distract the guards while we waited until the guards left.",
                  "We went to the shrine, ready to take on whatever the Pontifex has in store.",
                  "Until one of the guards came back to guard the shrine.",
                  "\"Hey you! You're the people who Saturn Marcher told me about. You guys need to be executed!\"",
                  "\"Hey! I'm back!\", Aurus said as he was running toward us. \"Oh, a stray. Let's pummel him!\"",
                  "\"I'd like to see you try!\" said the guard."]
journey4_part2 = ["We walk ahead into the chamber, ready to take on the Pontifex.",
                  "Nadrus busts the door open and we walk into a dark and spacious room.",
                  "\"For centuries no one has found this place\", said a voice. \"Well done on that behalf.\"",
                  "Rayden walks forward. \"Pontifex! Give me back my family which you enslaved.\"",
                  "\"I wouldn't say enslaved, dear.\", she responded. \"I simply opened their eyes.\"",
                  "Rayden clenched his fists."
                  "\"Well aren't you looking for a fight.\", she said. \"And let me guess...\"",
                  "\"You want to know about the crystal thief?\"",
                  "She smiled. \"The Galatigos play by the rules. We like to settle things once and for all.\"",
                  "\"If you can beat me, I will free your family, and tell you all I know about the crystal thief. Lose, and you join us.\"",
                  "\"Very well\", Rayden said.",
                  "She snaps her fingers and a faceless soldier appears in front of her.",
                  "\"Bring it on!\", Nadrus shouts."]
journey4_part3 = []
journey4_part4 = []


# setup_name() is only called upon once, so not much need to worry about it. If you are adding a story with the var player_name, then you must copy and paste
# the list into this command so that the name changes.
def setup_name(saved):
    global player_name
    global tutorial_story4
    global tutorial_story5
    global journey1_part1
    global journey1_part2
    global journey1_part3
    global journey2_part1
    global journey3_part1
    global journey3_part3
    global journey4_part3
    global journey4_part4
    if not saved:
        print("Type your name. Leave blank for the default name.")
        player_name = input(">")
        if player_name.lower().strip() == "":
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
                      "I smile. \"It's a pleasure to meet you, Aurus.\"\n",
                      "He shakes your hand and gives a serious face. \"I'll help you.\"",
                      "He sees your wounds on your body. \"You're wounded. I'll heal you up.\""]
    journey2_part1 = ["Aurus sits at the table and looks me.",
                      "\"I'm going to be completely honest\" he says. \"What if " + player_name + " was just some kid who called themself " + player_name + "?\"",
                      "Nadrus puts his hand on Aurus's. \"I know you're on edge because all the Kingdoms have fallen, but we have to trust " + player_name + ".\"",
                      "Nadrus looks at me. \"I never doubted you even since the time we met.\"",
                      "I sigh in relief. \"Alright, what's are next plan of action?\", I ask.",
                      "Aurus sits up straight. \"Maybe we should free Water Kingdom from the control of the Galatigos.\"",
                      "\"What even are the Galatigos?\", I ask.",
                      "Aurus looks at me. \"Well...\"\n",
                      "The Galatigos are a group of organised cultists who try to spread their religion across Isuren.",
                      "They worship the stars, planets, and galaxies above them. It's a fine religion, but they spread it in the wrong ways.",
                      "The Galatigos bend the galaxy to their will, using the magic of the universe.",
                      "Anyone who dares refuse to convert, they will attack them.",
                      "Their Pontifex is the most powerful of them all. No one knows her location, so she remains mysterious.\n",
                      "\"Alright then, let's free Water Kingdom then.\", Nadrus says.",
                      "We start walking towards Water Kingdom.",
                      "A person starts walking up to our group.",
                      "\"You'll pay for what you did to me last time\", he says.",
                      "\"Rats!\", Nadrus curses. \"I knew we should have killed him.\"",
                      "\"I'll end you once in for all!\", he says."]
    journey3_part1 = ["Aurus looked distressed and turns to me.",
                      "\"We better hurry\", says Aurus. \"They're going to force the people to join their religion, and it would be chaos.\"",
                      "\"Wait, why today?\", I ask. Aurus crosses his arms. \"Two reasons.\"",
                      "\"One, I know the Pontifex knows something about the crystal thief.\"",
                      "\"Two, They already do this practice, every. Single. Day.\"\n",
                      "Without question, we head out to a Galatigos church in order to gain answers.",
                      "\"I'm so mad at them. So much of my people have suffered...\", Aurus grunts."
                      "\"Hey chill out Aurus, they'll notice us!\", said Nadrus.",
                      "I give Nadrus a \"thank you\" nod, and he nods back.",
                      "And, as if on cue, sadly, the Galatigos noticed us.",
                      "\"You three! Stop right there!\", said a mage leading the group.",
                      "Nadrus stands firmly. \"Eh we ain't stopping without a fight.",
                      "The Mage laughs. \"I am the 5th Mooncaster, Saturn Marcher. What thinks you can stop me?\"",
                      "Nadrus counters her. \"And what makes you think if you're 5th, you're stronger?\"",
                      "The Mage stops laughing. \"Shaddup! Let's fight and see who's stronger!\"",
                      "\"Alright " + player_name + ", let's cream this guy!\" says Nadrus."]
    journey3_part3 = ["\"I have failed. I deserve to die. I have failed you, my lord.\"",
                      "Aurus helps him up. \"Now tell us where the Pontifex is.\"",
                      "He takes a pencil and circles a part on Aurus's map.",
                      "\"This is a shrine of the Galatigos. We have about 20 Galatigos guarding the place. That's all I know.\"",
                      "\"You are a true gentleman.\", Aurus says. \"Thank you.\"",
                      "We release the guy tied to the chair.",
                      "He points to me. \"I know you already.\"",
                      "\"" + player_name + ", right? The prophecy?\"",
                      "\"Yeah...\", I said.",
                      "\"I'm Rayden, the Thunder Knight. Please let me join you. I need to get a burden off my chest.\"",
                      "\"If you say so.\", I said. \"Good to have you on the team.\""]
    journey4_part3 = ["The soldier explodes into pieces and Aurus is knocked down by the impact.",
                      "\"My oh my.\", the Pontifex said. \"Your healer has already fallen. Looks like I've won.\"",
                      "\"Don't get too cocky...\", Aurus said as he crawled on the floor.",
                      "Everyone turns towards Aurus, who is miraculously alive.",
                      "\"" + player_name + "! I will heal you with the rest of my power!\"",
                      "He grabs my leg and sends healing magic through my body.",
                      "I get up and look at the Pontifex. \"We will win!\", I yelled.",
                      "She smiles. \"Your magic is useless. Show me everything you've got.\""]
    journey4_part4 = ["\"I... I lost\", said the Pontifex. She gets up and looks at me.",
                      "\"You are simply more powerful than me. You have earned my respect.\"",
                      "Nadrus stand firmly. \"Now tell us what you know about the crystal thief\"",
                      "\"Alright\", she said.\n",
                      "One quiet evening I stumbled upon a girl who came to my shrine covered in dirt and demonic ectoplasm.",
                      "I brought her in, as another new member to Galatigos is always welcome.",
                      "She never said anything. And I could easily tell that she was 9 years, 8 months, and 16 days old.",
                      "She didn't know her name either. It was so strange."
                      "As I tried to touch her, some energy shocked me, burned me, and suffocated me all at the same time.",
                      "As I backed off, she smiled at me, and stood in place as she waited for me to get up.",
                      "I let her stay at my shrine and she trained alongside some of my strongest lackeys.",
                      "Time passed quickly, and she easily learned how to absorb magic like me.",
                      "About 3 months later, on the day of her birthday, she mysteriously snuck out of the shrine without any guards knowing.",
                      "If trained well, I knew she would surpass the strongest one day.\n",
                      "\"That was several years ago.\", she said. \"I have no doubt that's who you are looking for.\"",
                      "\"Thank you Pontifex\", I said.",
                      "She turns to Rayden. \"You have some people waiting for you at home.\"",
                      "Rayden smiles. \"Thank you so much...\"",
                      "Rayden's look becomes stern. \"" + player_name + ". Although my family are at home waiting for me,\"",
                      "\"I will fight alongside you until the end.\"",
                      "I smile and Rayden smiles back.",
                      "\"This is only the beginning of our adventure...\""]


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
        setup_game(intro_story, 0.045, 1, 1)
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
            setup_game(intro_story, 0.045, 1, 1)
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
def setup_game(story, text_speed, wait_time, output):
    global player_name
    global text_speed_multiplier
    global wait_speed_multiplier
    print("\n")
    story_num = int(len(story))
    story_current = 0
    while story_current < story_num:
        for char in story[story_current]:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(text_speed * text_speed_multiplier)
        time.sleep(wait_time * wait_speed_multiplier)
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
        setup_name(False)
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
        print("Commands:")
        print(travel_commands)
        command = get_command(travel_commands)
        if command.lower() == "shop":
            enter_shop("Earth")
        if command.lower() == "medic":
            heal("max")
            enter_city("Earth")
        if command.lower() == "hunt":
            begin_hunt("Earth")
        if command.lower() == "companions":
            swap_companions(location)
        if command.lower() == "journey":
            begin_journey()
            enter_city("Earth")
        if command.lower() == "travel":
            travel_to()
        if command.lower() == "save":
            save_game()
            print("Game has been saved!")
            enter_city("Earth")
    if location == "Water":
        travel_commands = ["companions", "travel", "journey", "shop"]
        print("Commands:")
        print(travel_commands)
        command = get_command(travel_commands)
        if command.lower() == "companions":
            swap_companions(location)
        if command.lower() == "journey":
            begin_journey()
            enter_city("Water")
        if command.lower() == "travel":
            travel_to()
        if command.lower() == "shop":
            enter_shop("Water")


# This is the journey command. You can call it whenever you are in a town. The reason I made it a command was to be able to access it regardless of whatever
# town you are in.
def begin_journey():
    global journey
    os.system('cls')
    if "block" not in current_commands:
        print("Buy a wooden shield before you start journeying!")
        return enter_city("Earth")
    if journey == 1:
        setup_game(journey1_part1, 0.04, 0.5, 7)
        print("You can now set Aqua Mage as your active companion.")
        companions.append(2)
        journey += 1
        return print("Journey Complete!")
    if journey == 2:
        setup_game(journey2_part1, 0.05, 0.5, 12)
        journey += 1
        print("You can now travel to Water Kingdom.")
        travel_destinations.append("water")
        return print("Journey Complete!")
    if journey == 3:
        setup_game(journey3_part1, 0.05, 0.5, 14)
        journey += 1
        print("You can now set Thunder Knight as your active companion.")
        companions.append(3)
        return print("Journey Complete!")
    if journey == 4:
        setup_game(journey4_part1, 0.05, 0.5, 16)
        journey += 1
        print("You have beaten Mooncaster Pontifex.")
        return print("Journey Complete!")


# Swaps companions. Same case as begin_journey(). current_city allows the command to exit once the command is done.
def swap_companions(current_city):
    global equipped_companion
    companion_name = ""
    if equipped_companion == 1:
        companion_name = "Flame Knight"
    if equipped_companion == 2:
        companion_name = "Aqua Mage"
    if equipped_companion == 3:
        companion_name = "Thunder Knight"
    equipped_companion_name = companion_name
    print("Active companion: " + companion_name)
    print("Inactive companions: ")
    for i in range(len(companions)):
        if companions[i] == 1:
            companion_name = "Flame Knight"
        elif companions[i] == 2:
            companion_name = "Aqua Mage"
        elif companions[i] == 3:
            companion_name = "Thunder Knight"
        print(str(i + 1) + ". " + companion_name)
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
    for x in range(len(preys)):
        print(str(x + 1) + " - " + str(preys[x]).title())
    prey = get_command(preys)
    if prey == "dirt elemental":
        enter_battle(dirt_elemental, 0)
    elif prey == "earth boar":
        enter_battle(earth_boar, 0)
    elif prey == "rock monster":
        enter_battle(rock_monster, 0)
    enter_city(city)


def travel_to():
    print("Travel to:")
    print(travel_destinations)
    destination = get_command(travel_destinations)
    cap = destination.capitalize()
    enter_city(cap)


class Item:
    def __init__(self, name, item_type, item_num, gold_cost, buy_phrase, bought_shield_boost):
        self.name = name
        self.item_type = item_type
        self.item_num = item_num
        self.gold_cost = gold_cost
        self.buy_phrase = buy_phrase
        self.bought_shield_boost = bought_shield_boost

    def do_shop(self):
        global weapon_type
        global shield_type
        global shield_boost
        global gold
        global player_hp
        global player_max_hp
        if gold >= self.gold_cost:
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
            print("You have bought " + self.name.title() + ".")
            print(self.buy_phrase)
            gold -= self.gold_cost
        else:
            print("You need more gold!")


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
        items.append("enchanted staff")
        items.append("aqua staff")
        items.append("heavy shield")
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
    print("Type \"Leave\" to leave.")
    default_buy_phrase = "It has been automatically equipped."
    s1 = Item("Wooden Shield", "shield", 1, 10, default_buy_phrase, 30)
    w2 = Item("Wooden Sword", "weapon", 2, 10, default_buy_phrase, None)
    w3 = Item("Iron Sword", "weapon", 3, 150, default_buy_phrase, None)
    s2 = Item("Iron Shield", "shield", 2, 150, default_buy_phrase, 55)
    w4 = Item("Enchanted Staff", "weapon", 4, 350, "Let the power flow within you.", None)
    w5 = Item("Aqua Staff", "weapon", 5, 350, "Let the power flow within you.", None)
    s3 = Item("Heavy Shield", "shield", 3, 400, default_buy_phrase, 105)
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
    if buy == items[-1]:
        print("Come again!")
    enter_city(city)


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
    if weapon_type == 3:
        minATK = 8
        maxATK = 10
    if weapon_type == 4:
        minATK = 14
        maxATK = 19
    if weapon_type == 5:
        minATK = 15
        maxATK = 18
    # shields
    if shield_type == 1:
        min_block = 2
        max_block = 4
    if shield_type == 2:
        min_block = 9
        max_block = 11
    if shield_type == 3:
        min_block = 14
        max_block = 17
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
    if equipped_companion == 3:
        companion_name = "Thunder Knight"
        companion_ATK = 35
        companion_ability = 3
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
            current_cooldown = ability_cooldown + 1
            if ability == "ATK_boost":
                print(companion_name + " has boosted your attack by " + str(companion_boost) + "!")
            if ability == "Damage":
                print(companion_name + " dealt " + str(dmg) + " damage!")
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
        enemy_damage = (randint(enemy_minATK, enemy_maxATK) - blocked_damage) + enemy_extra_damage
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
                    if ability == "ATK_boost":
                        print(companion_name + " has boosted your attack by " + str(companion_boost) + "!")
                    current_cooldown = ability_cooldown + 1
                    if ability == "Damage":
                        print(companion_name + " dealt " + str(dmg) + " damage!")
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
        setup_game(tutorial_story3, 0.05, 0.5, 4)
    if outcome == 2:
        setup_game(tutorial_story5, 0.05, 0.5, 6)
    if outcome == 3:
        enter_city("Earth")
    if outcome == 4:
        setup_game(journey1_part2, 0.05, 0.5, 10)
    if outcome == 5:
        setup_game(journey1_part3, 0.05, 0.5, 11)
    if outcome == 6:
        setup_game(journey2_part2, 0.05, 0.5, 13)
    if outcome == 7:
        setup_game(journey2_part3, 0.05, 0.5, 0)
    if outcome == 8:
        setup_game(journey3_part2, 0.05, 0.5, 15)
    if outcome == 9:
        setup_game(journey3_part3, 0.05, 0.5, 0)
    if outcome == 10:
        setup_game(journey4_part2, 0.05, 0.5, 17)
    if outcome == 11:
        setup_game(journey4_part3, 0.05, 0.5, 18)
    if outcome == 12:
        setup_game(journey4_part4, 0.05, 0.5, 0)


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
