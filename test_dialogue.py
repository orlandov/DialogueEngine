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
                    { "say": "say1" },
                    { "responses": [
                        ["response1", "resp1"],
                        ["response2", "resp2"],
                        ["response3", "end"],
                    ] }
                ],
                'resp1': [
                    { "say": "hello" },
                    'end'
                ]

            }
        }
        # record actions in state
        self.state = { "say": [], "responses": [] }

        def say_cb(text):
            self.state['say'].append(text)

        def responses_cb(responses):
            print "I WAS CALLED"
            self.state['responses'].append(responses)
            return "resp1"

        callbacks = {
            "say": say_cb,
            "responses": responses_cb
        }
        self.dialogue = dialogue.DialogueEngine(callbacks, tree=self.tree)

    def tearDown(self):
        pass

    def test_simple(self):
        print self.state
        print self.tree
        self.dialogue.run()

if __name__ == "__main__":
    unittest.main()
