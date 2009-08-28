#!/usr/bin/python

import sys
import yaml
import pprint
import optparse

class EndException(Exception):
    pass

class DialogEngine(object):
    def __init__(self, filename, callbacks):
        self.state = state
        self.tree = yaml.load(file(filename))
        self.__dict__.update(callbacks)

    def run(self):
        start_section = self.tree['START']
        try:
            self.run_section(start_section)
        except EndException:
            # we stopped talking to the NPC
            pass
        
    def run_section(self, section_name):
        tree = self.tree
        while True:
            for command in tree['SECTIONS'][section_name]:
                if isinstance(command, str):
                    if command == "end":
                        # indicate we'd like to stop talking
                        raise EndException
                    elif command == "pause":
                        print "Press any key to continue"
                        sys.stdin.readline()
                    elif command == "back":
                        return
                    else:
                        raise Exception("Unknown command %s" % (command,))
                elif isinstance(command, dict):
                    if command.get("say"):
                        self.say_cb(command['say'])
                    elif command.get("responses"):
                        section = self.responses_cb(command.get("responses"))
                        if section == 'back':
                            return
                        self.run_section(section)
                    elif command.get("start_quest"):
                        self.quest_cb(command.get("start_quest"))
                else:
                    raise Exception("Invalid command %s" % (command,))

state = {
    'quests': {},
    'say_log': [],
}

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


parser = optparse.OptionParser()
parser.add_option("-d", "--demo",
    action="store_true",
    dest="demo",
    help="try out the dialogue engine",
    metavar="DEMO",
    default=True)

(options, args) = parser.parse_args()

print options, args
dialog = DialogEngine('dialog', callbacks)
dialog.run()
