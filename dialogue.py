#!python

try:
    import yaml
except:
    pass

import sys
import itertools

class EndException(Exception):
    pass

class DialogueEngine(object):
    def __init__(self, *args, **kwargs):
        if kwargs.get("tree"):
            callbacks = args[0]
            self.tree = kwargs.get('tree')
        else:
            (filename, callbacks) = args
            self.tree = yaml.load(file(filename))
        self.callbacks = callbacks

    def run(self):
        start_section = self.tree['START']
        try:
            self.run_section(start_section)
        except EndException:
            # we stopped talking to the NPC
            return

    def get_section(self, section_name):
        return self.tree['SECTIONS'][section_name]

    def run_section(self, section_name):
        tree = self.tree
        for command in itertools.cycle(self.get_section(section_name)):
            if isinstance(command, str):
                if command == "end":
                    # indicate we"d like to stop talking
                    raise EndException
                elif command == "back":
                    return
                else:
                    raise Exception("Unknown command %s" % (command,))
            elif isinstance(command, dict):
                if command.get("say"):
                    self.callbacks["say"](command["say"])
                elif command.get("responses"):
                    section = self.callbacks["responses"](command.get("responses"))
                    if section == "back": return
                    self.run_section(section)
                elif command.get("start_quest"):
                    self.callbacks["quest"](command.get("start_quest"))
                else:
                    raise Exception("Unknown command %s" % (command,))
            else:
                raise Exception("Invalid command %s" % (command,))
