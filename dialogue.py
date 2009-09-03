#!python

try:
    import yaml
except:
    pass

import sys
import itertools

class EndException(Exception):
    pass

class ResponseException(Exception):
    pass

class BackException(Exception):
    pass

class DialogueEngine(object):
    def __init__(self, *args, **kwargs):
        """A very simple dialogue engine for a game.
           d = DialogueEngine(tree, callbacks)
           d = DialogueEngine('screenplay.yaml', callbacks)
           d.run() -> runs script until next responses prompt and then fires calls 
                      the respsonses callback
           d.reply(1) -> replies with the desired response"""

        (obj, callbacks) = args
        if isinstance(obj, dict):
            self.tree = obj
        elif instance(obj, str):
            self.tree = yaml.load(file(filename))

        self.callbacks = callbacks

    def run(self):
        start_section = self.tree['START']
        self.section_stack = []

        try:
            self.run_section(start_section)
        except EndException:
            # we stopped talking to the NPC
            return
        except ResponseException, e:
            return e
        except BackException, e:
            self.section_stack.pop(-1)
            try:
                self.run_section(self.section_stack[-1])
                return e
            except ResponseException, e:
                return e

    def get_section(self, section_name):
        return self.tree['SECTIONS'][section_name]

    def reply(self, choice):
        try:
            self.run_section(self.section_stack[-1], choice)
        except ResponseException, e:
            print "got response exception", e
            return e
        except BackException, e:
            self.section_stack.pop(-1)
            try:
                print "Trying to run ", self.section_stack[-1]
                self.run_section(self.section_stack[-1])
                return e
            except ResponseException, e:
                return e

    def run_section(self, section_name, choice=None):
        tree = self.tree
        print "run_section", section_name, self.section_stack

        if choice is None:
            self.section_stack.append(section_name)

        if len(self.section_stack) > 1:
            if self.section_stack[-1] == self.section_stack[-2]:
                self.section_stack.pop(-1)

        for command in itertools.cycle(self.get_section(section_name)):
            # a simple string command
            if isinstance(command, str):
                if command == "end":
                    # indicate we"d like to stop talking
                    raise EndException
                elif command == "back":
                    raise BackException()
                else:
                    raise Exception("Unknown command %s" % (command,))
            # a hash command
            elif isinstance(command, dict):
                if command.get("say"):
                    if choice is None:
                        self.callbacks["say"](command["say"])
                elif command.get("responses"):
                    if choice is None:
                        self.callbacks["responses"](command.get("responses"))
                        raise ResponseException(command.get("responses"))
                    else:
                        section = command.get('responses')[choice][1]
                        print "section was", section
                        if section == "back":
                            raise BackException()
                        elif section == "end":
                            raise EndException()
                        self.run_section(section)
                elif command.get("start_quest"):
                    self.callbacks["quest"](command.get("start_quest"))
                else:
                    raise Exception("Unknown command %s" % (command,))
            else:
                raise Exception("Invalid command %s" % (command,))
