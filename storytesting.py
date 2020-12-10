# import os

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
        print(partition)
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


# for x in dialogue:
#     print(dialogue[x])
# print(dialogue)
print(dialogue["t4"])


# lol[1][1] = "lol"
# print(lol)
# for player_name use {0} so that you can get the 1st argument in a .Format()
# maybe should try using dictionaries and assigning custom vars into that?
# day 2
# uh probably should try to sort out the p1 p2 stuff so its more flexible into the dictionary
# i kinda want to make sub dictionaries in this dictionary