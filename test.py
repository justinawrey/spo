import spo.api as api

while True:
    inp = input("Enter a command: ")
    if inp == "prev":
        api.prev_song()
    elif inp == "next":
        api.next_song()
    elif inp == "play":
        api.play()
    elif inp == "pause":
        api.pause()
    elif inp == "show":
        api.curr_song()
    elif inp == "replay":
        api.replay()
    elif inp == "save":
        api.save()
    elif inp == "delete":
        api.delete()
    else:
        inp = inp.split()
        if inp[0] == "vol":
            if inp[1] == "up":
                api.volume(True, inp[2])
            elif inp[1] == "down":
                api.volume(False, inp[2])
        elif inp[0] == "shuffle":
            if inp[1] == "on":
                api.shuffle(True)
            else:
                api.shuffle(False)
        elif inp[0] == "repeat":
            if inp[1] == "on":
                api.repeat(True)
            else:
                api.repeat(False)
        elif inp[0] == "recent":
            api.recent(inp[1])
        elif inp[0] == "search":
            search_terms = inp[2:]
            api.search(inp[1], *search_terms)
