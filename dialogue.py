#!python

try:
    import yaml
except:
    pass

import logging
import sys
import itertools

class EndException(Exception):
    pass

class ResponseException(Exception):
    pass

class BackException(Exception):
    pass

class DialogueEngine(object):
    def __init__(self, obj, callbacks={}, state={}):
        """A very simple dialogue engine for a game.
           d = DialogueEngine(tree, callbacks)
           d = DialogueEngine('screenplay.yaml', callbacks)"""

        if isinstance(obj, dict):
            self.tree = obj
        elif isinstance(obj, str):
            self.tree = yaml.load(file(obj))

        logging.basicConfig(level=logging.INFO)

        self.callbacks = callbacks
        self.state = state

    def run(self):
        """Start running the dialogue engine.
        @returns: list of lists (if requesting a response)
        @returns: None (if at the end of the script)"""
        start_section = self.tree['START']
        self.section_stack = []

        try:
            self.run_section(start_section)
        except EndException:
            # we stopped talking to the NPC
            return
        except ResponseException, e:
            return e.message
        except BackException, e:
            self.section_stack.pop(-1)
            try:
                self.run_section(self.section_stack[-1])
                return e
            except ResponseException, e:
                return e.message

    def get_section(self, section_name):
        """Return a section object.
        @type section_name: string
        @param section_name: The section to get
        @return: dict"""
        return self.tree['SECTIONS'][section_name]

    def reply(self, choice):
        """After being prompted to provide a response, reply is called to
           submit a response.
           @type choice: int
           @param choice: the index of the response to submit
           @return: list of lists (if requesting a response)
           @return: None (if at the end of the script)"""
        while True:
            try:
                self.run_section(self.section_stack[-1], choice)
            except ResponseException, e:
                logging.debug("Got response exception %s" % (e.message, ))
                return e.message
            except BackException, e:
                self.section_stack.pop(-1)
                choice = None
                continue
            except EndException:
                logging.debug("Reached the end")
                return

    def run_section(self, section_name, choice=None):
        """Run a section, or reply to a previously run section
           @type section_name: string
           @param section_name: The section to run
           @type choice: int
           @param choice: Index of desired reply, if replying (None by default)
           @return: None
           @raises: EndException on end of script
           @raises: BackException on "back" reply"""

        state = self.state
        tree = self.tree

        if choice is None:
            self.section_stack.append(section_name)

        if len(self.section_stack) > 1:
            if self.section_stack[-1] == self.section_stack[-2]:
                self.section_stack.pop(-1)

        logging.debug("In run_section %s %s" % (section_name, self.section_stack,))
        for command in itertools.cycle(self.get_section(section_name)):
            if command.get("say"):
                if choice is None and self.callbacks.get('say'):
                    self.callbacks["say"](state, command["say"])

            elif command.get("responses"):
                responses = []
                for response in command.get('responses'):
                    cond = response[2:]
                    if not cond or eval(cond[0], state, {}):
                        responses.append(response)
                if choice is None:
                    if self.callbacks.get("responses"):
                        self.callbacks["responses"](state, responses)

                    raise ResponseException(responses)

                else:
                    section = responses[choice][1]
                    logging.debug("User chose %s" % (section,))

                    if section == "back":
                        raise BackException()
                    elif section == "end":
                        raise EndException()
                    self.run_section(section)

            elif command.get("start_quest"):
                self.callbacks["start_quest"](state, command.get("start_quest"))

            elif command.get("complete_quest"):
                self.callbacks["complete_quest"](state, command.get("complete_quest"))

            elif command.get("dialogue"):
                command = command.get("dialogue")
                if command == "end":
                    # indicate we"d like to stop talking
                    raise EndException
                elif command == "back":
                    raise BackException()
                else:
                    raise Exception("Unknown command %s" % (command,))

            else:
                raise Exception("Unknown command %s" % (command,))
