#!/usr/bin/python

import dialogue
import yaml
import sys

class Player(object):
    """
    Mock player object that always has complete quests
    """
    def __init__(self):
        self.current_quests = set()
        self.finished_quests = set()

    def canAcceptQuest(self, quest):
        return     quest not in self.finished_quests \
               and quest not in self.current_quests

    def hasSatisfiedQuest(self, quest):
        return quest in self.current_quests

    def startQuest(self, quest):
        if quest in self.current_quests:
            raise RuntimeError("Already have quest, %s" % quest)
        self.current_quests.add(quest)

    def completeQuest(self, quest):
        self.finished_quests.add(quest)
        self.current_quests.remove(quest)

def main():

    # set up some closures
    def say_cb(state, text):
        print "NPC says:", text

    def get_reply(responses):
        for i, response in enumerate(responses):
            print "%d. %s" % (i, response)
        print "\nChoose a response: ",
        val = int(sys.stdin.readline().strip())
        print "you picked %s" % (val,)
        return val

    def start_quest(state, quest):
        print "You've picked up the '%s' quest!" % quest,
        state['pc'].startQuest(quest)

    def complete_quest(state, quest):
        print "You've finished the '%s' quest" % quest
        state['pc'].completeQuest(quest)

    callbacks = {
        "say": say_cb,
        "start_quest": start_quest,
        "complete_quest": complete_quest
    }

    pc = Player()

    state = {
        'quests': {},
        'pc': pc
    }

    dialog = dialogue.DialogueEngine('demo.yaml', callbacks, state)
    responses = dialog.run()
    while responses:
        choice = get_reply(responses)
        responses = dialog.reply(choice)

if __name__ == "__main__":
    main()
