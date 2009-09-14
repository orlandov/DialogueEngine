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
                        ["This one toggles", "toggles", "show == True"],
                        ["Always display this one", "display", "True and True"],
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
        # record actions in test_vars
        test_vars = { "say": None, "responses": [] }

        def say_cb(state, text):
            print "npc said", text
            state["say"] = text

        self.replies = ["resp1", "back", "stop"]

        def responses_cb(state, responses):
            print "responses", responses
            state['responses'] = responses

        callbacks = {
            "say": say_cb,
            "responses": responses_cb
        }

        self.dialogue = dialogue.DialogueEngine(self.tree, callbacks, test_vars)

    def assert_say(self, text):
        self.assertEqual(text, self.dialogue.state['say'])

    def assert_responses(self, responses):
        self.assertEqual(responses, self.dialogue.state['responses'])

    def test_simple(self):
        self.dialogue.state['show'] = False
        print self.dialogue.run()

        self.assert_say('Greetings stranger')
        self.assert_responses([
            ["Hi, can you tell me where I am?", "friendly"],
            ["Watch your words", "aggro"],
            ["Always display this one", "display", "True and True"],
            ["response3", "stop"],
        ])
        print self.dialogue.reply(0)

        self.assert_say('You sure are lost')
        self.assert_responses([
            ["Thanks, I know", "thanks"],
            ["Wait what did you say before?", "back"]
        ])
        self.dialogue.state['show'] = True
        print self.dialogue.reply(1)

        self.assert_say('Greetings stranger')
        self.assert_responses([
            ["Hi, can you tell me where I am?", "friendly"],
            ["Watch your words", "aggro"],
            ["This one toggles", "toggles", "show == True"],
            ["Always display this one", "display", "True and True"],
            ["response3", "stop"],
        ])
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
