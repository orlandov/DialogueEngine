#!/usr/bin/python

import sys
import pprint
import unittest
import dialogue

class TestDialogue(unittest.TestCase):
    def setUp(self):
        tree = {
            'START': 'main',
            'SECTIONS': {
                'main': [
                    { "say": "say1" },
                    { "responses": [
                        ["response1", "resp1"],
                        ["response2", "resp2"],
                        ["response3", "end"],
                    ] }
                ]
            }
        }
        # record actions in state
        self.state = { "say": [], "responses": [] }

        def say_cb(text):
            self.state['say'].append(text)

        def responses_cb(responses):
            self.state['responses'].append(responses)

        callbacks = {
            "say_cb": say_cb,
            "responses_cb": responses_cb
        }
        self.dialogue = dialogue.DialogueEngine(callbacks, tree=tree)

    def tearDown(self):
        pass

    def testSimple(self):
        self.dialogue.run()
        print self.state

if __name__ == "__main__":
    unittest.main()
