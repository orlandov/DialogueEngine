#!/usr/bin/python

import dialogue
import yaml
import sys

def main():
    state = {
        'quests': {},
    }

    # set up some closures
    def say_cb(text):
        print "NPC says:", text

    def get_reply(responses):
        for i, response in enumerate(responses):
            print "%d. %s" % (i, response)
        print "\nChoose a response: ",
        val = int(sys.stdin.readline().strip())
        print "you picked %s" % (val,)
        return val

    def quest_cb(name):
        print "You've picked up the '%s' quest!" % (name,)
        state['quests'][name] = 1

    callbacks = {
        "say": say_cb,
        "quest": quest_cb
    }

    dialog = dialogue.DialogueEngine('demo.yaml', callbacks)
    responses = dialog.run()
    while responses:
        choice = get_reply(responses)
        responses = dialog.reply(choice)

    print "State was", state

if __name__ == "__main__":
    main()
