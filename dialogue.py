
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
        self.__dict__.update(callbacks)

    def run(self):
        start_section = self.tree['START']
        print "Start section is ", start_section
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
