#!/usr/bin/python

import sys
import pprint
import unittest
import dialogue

class TestDialogue(unittest.TestCase):
    def setUp(self):
        self.tree = {
            'START': 'main',
            'SECTIONS': {
                'main': [
                    { "say": "Greetings stranger" },
                    { "responses": [
                        ["Hi, can you tell me where I am?", "friendly"],
                        ["Watch your words", "aggro"],
                        ["response3", "stop"],
                    ] }
                ],
                'friendly': [
                    { "say": "You sure are lost" },
                    { "responses": [
                        ["Thanks, I know", "thanks"],
                        ["Wait what did you say before?", "back"],
                    ] }
                ],
                'thanks': [
                    { "say": "We haven't seen one of your kind in ages" },
                    { "responses": [
                        ["Blah blah blah", "foo"],
                        ["Say the other thing again", "back"],
                    ] }
                ],
            }
        }
        # record actions in state
        self.state = { "say": None, "responses": [] }

        def say_cb(text):
            print "npc said", text
            self.state["say"] = text

        self.replies = ["resp1", "back", "stop"]

        def responses_cb(responses):
            pass

        callbacks = {
            "say": say_cb,
            "responses": responses_cb
        }
        self.dialogue = dialogue.DialogueEngine(self.tree, callbacks)

    def assert_say(self, text):
        self.assertEqual(text, self.state['say'])

    def test_simple(self):
        print self.dialogue.run()

        self.assert_say('Greetings stranger')
        print self.dialogue.reply(0)

        self.assert_say('You sure are lost')
        print self.dialogue.reply(1)

        self.assert_say('Greetings stranger')
        print self.dialogue.reply(0)

        self.assert_say('You sure are lost')
        print self.dialogue.reply(1)

        self.assert_say('Greetings stranger')
        print self.dialogue.reply(0)

        self.assert_say('You sure are lost')
        print self.dialogue.reply(0)

        self.assert_say("We haven't seen one of your kind in ages")
        print self.dialogue.reply(1)

        self.assert_say('You sure are lost')
        print self.dialogue.reply(1)

        self.assert_say('Greetings stranger')

if __name__ == "__main__":
    unittest.main()
