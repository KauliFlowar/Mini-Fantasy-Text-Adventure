import time
import sys
print("\n")
story = ["Once upon a time, there was a world named Isuren, which was home to many amazing creatures.\n", "Isuren was divided into various kingdoms, each with their own element.\n", "Each kingdom's power rests in an elemental crystal, sealed within the kingdom.\n", "One day, an elemental crystal was stolen and the kingdom's power slowly faded away.\n", "Within a few years, multiple different elemental crystals were stolen and their kingdoms fell.\n", "Soon enough, every single kingdom had lost their elemental crystal.\n", "Then, a prophecy has been spoken about a young hero, who can find and return the crystals from the thief.\n", "Isuren will be saved one day...\n"]
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
