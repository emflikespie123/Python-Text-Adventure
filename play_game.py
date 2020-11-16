import json, time, os, random
begin = time.time()

def main():
    # TODO: allow them to choose from multiple JSON files?
    x = os.listdir()
    y = 0
    list1 = []
    print("What game do you want to run?")
    for file in x:
        if ".json" in file:
            print ("  {}. {}".format(y+1, file))
            y +=1
            list1.append(file)
        else:
            pass
    option1 = input(">").lower().strip()
    num = int(option1) - 1
    selected = list1[num]
    with open(str(selected)) as fp:
        game = json.load(fp)
    if selected == "spooky_mansion.json":
        print_instructions()
        play(game)
    elif selected == "adventure.json":
        print_instructions()
        print("You are about to play '{}'! Good luck!".format(game['__metadata__']['title']))
        print("")
        play(game)


def play(rooms):
    # Where are we? Look in __metadata__ for the room we should start in first.
    current_place = rooms['__metadata__']['start']
    # The things the player has collected.
    stuff = []
    removed_items = []
    cat_start = 'classroom'
    while True:
        # Figure out what room we're in -- current_place is a name.
        here = rooms[current_place]
        # Print the description.
        print(here["description"])

        # TODO: print any available items in the room...
        # e.g., There is a Mansion Key.
        if len(here['items']) > 0:
            print ("You have found" , here['items'])
            
            
        # Is this a game-over?
        if here.get("ends_game", False):
            break

        # Allow the user to choose an exit:
        usable_exits = find_usable_exits(here, stuff)
        # Print out numbers for them to choose:
        for i, exit in enumerate(usable_exits):
            print("  {}. {}".format(i+1, exit['description']))

        # See what they typed:
        action = input("> ").lower().strip()

        # If they type any variant of quit; exit the game.
        if current_place == cat_start:
            print("There is a black cat here!")
        
        if "time" in action:
            time1()
            continue
        if "help" in action:
            print_instructions()
            continue
        if "stuff" in action:
            if len(stuff) == 0:
                print ("You have nothing")
            else:
                print (stuff)
            continue
        if "take" in action:
            stuff.extend(here['items'])
            print("You have taken" , here['items'])
            here['items'].clear()
            continue
    
            
        if action in ["quit", "escape", "exit", "q"]:
            print("You quit.")
            break
        if action == "search":
            for exit in here ['exits']:
                exit['hidden']=False
            continue
        if action == "drop":
            for n, i in enumerate(stuff):
                print(n,i)
            option = int(input("What do you want to drop?"))
            x = stuff.pop(option)
            here['items'].append(x)
            continue
                
            
        if action in ["check time"] :
            print ("You have been stuck here for" , timer)
        
        if random.randint(0,2) == 0:
            cat_in_room = rooms[cat_start]
            exit_cat = random.choice(cat_in_room['exits'])
            cat_start = exit_cat['destination']
            
        # TODO: if they type "stuff", print any items they have (check the stuff list!)
        # TODO: if they type "take", grab any items in the room.
        # TODO: if they type "search", or "find", look through any exits in the room that might be hidden, and make them not hidden anymore!
        
        # Try to turn their action into an exit, by number.
        try:
            num = int(action) - 1
            selected = usable_exits[num]
            current_place = selected['destination']
            print("...")
        except:
            print("I don't understand '{}'...".format(action))
        
    print("")
    print("")
    print("=== GAME OVER ===")

def find_usable_exits(room, stuff):
    """
    Given a room, and the player's stuff, find a list of exits that they can use right now.
    That means the exits must not be hidden, and if they require a key, the player has it.

    RETURNS
     - a list of exits that are visible (not hidden) and don't require a key!
    """
    usable = []
    for exit in room['exits']:
        if exit.get("hidden", False):
            continue
        if "required_key" in exit:
            if exit["required_key"] in stuff:
                usable.append(exit)
            continue
        usable.append(exit)
    return usable

def time1():
    endtimer = input ("Hit enter if you want to see how long you have been stuck here.")
    end = time.time()
    elapsed = end - begin
    print ("You have been stuck here for" , elapsed, "seconds")
def print_instructions():
    print("=== Instructions ===")
    print(" - Type a number to select an exit.")
    print(" - Type 'stuff' to see what you're carrying.")
    print(" - Type 'take' to pick up an item.")
    print(" - Type 'quit' to exit the game.")
    print(" - Type 'search' to take a deeper look at a room.")
    print("=== Instructions ===")
    print("")

if __name__ == '__main__':
    main()
