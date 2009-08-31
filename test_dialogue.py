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
                        ["response3", "stop"],
                    ] }
                ],
                'resp1': [
                    { "say": "hello" },
                    { "responses": [
                        ["response4", "resp4"],
                        ["response5", "back"],
                    ] }
                ],
                'stop': [
                    'end'    
                ]

            }
        }
        # record actions in state
        self.state = { "say": [], "responses": [] }

        def say_cb(text):
            self.state["say"].append(text)

        self.replies = ["resp1", "back", "stop"]

        def responses_cb(responses):
            self.state['responses'].append([ response[0] for response in responses ])
            resp = self.replies.pop(0)
            return resp

        callbacks = {
            "say": say_cb,
            "responses": responses_cb
        }
        self.dialogue = dialogue.DialogueEngine(callbacks, tree=self.tree)

    def test_simple(self):
        self.dialogue.run()
        self.assertEqual(self.state,
            {
                "say": ["say1", "hello", "say1"],
                "responses": [
                    ["response1", "response2", "response3"],
                    ["response4", "response5"],
                    ["response1", "response2", "response3"],
                ]
            }
        )

if __name__ == "__main__":
    unittest.main()
