import dialogue

def main():
    state = {
        'quests': {},
        'say_log': [],
    }

    # set up some closures
    def say_cb(text):
        print "NPC says:", text
        state['say_log'].append(text)

    def responses_cb(responses):
        for i, response in enumerate(responses):
            print "%d. %s" % (i, response[0])
        print "\nChoose a response: ",
        val = int(sys.stdin.readline().strip())
        print "you picked %s" % (val,)
        return responses[val][1]

    def quest_cb(name):
        print "You've picked up the '%s' quest!" % (name,)
        state['quests'][name] = 1
        print state

    callbacks = {
        "say_cb": say_cb,
        "responses_cb": responses_cb,
        "quest_cb": quest_cb
    }

    dialog = dialogue.DialogueEngine('demo.yaml', callbacks)

if __name__ == "__main__":
    main()
