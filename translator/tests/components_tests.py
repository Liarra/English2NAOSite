from unittest import TestCase

from translator.executables.nlp.components.execution import GoTo
from translator.executables.nlp.components.robot_commands import *
from translator.executables.nlp.components.robot_commands import button_press


__author__ = 'NBUCHINA'


class ComponentsTests(TestCase):
    def test_create_wait(self):
        wait_params = wait_command(ms=2000)

        wait_text_seconds = wait_command.from_string("Wait for 4 seconds")
        wait_text_sec = wait_command.from_string("Wait for 4 sec.")

        wait_text_minutes = wait_command.from_string("Wait for 1 minute")
        wait_text_min = wait_command.from_string("Wait for 1 min.")

        wait_text_milliseconds = wait_command.from_string("Wait for 1 millisecond")
        wait_text_ms = wait_command.from_string("Wait for 1 ms")

        self.assertIsInstance(wait_text_milliseconds, wait_command)
        self.assertIsInstance(wait_text_ms, wait_command)
        self.assertIsInstance(wait_text_minutes, wait_command)
        self.assertIsInstance(wait_text_min, wait_command)
        self.assertIsInstance(wait_text_seconds, wait_command)
        self.assertIsInstance(wait_text_sec, wait_command)

        self.assertEquals(2000, wait_params.params["ms"])
        self.assertEquals(4000, wait_text_seconds.params["ms"])
        self.assertEquals(4000, wait_text_sec.params["ms"])
        self.assertEquals(60 * 1000, wait_text_minutes.params["ms"])
        self.assertEquals(60 * 1000, wait_text_min.params["ms"])
        self.assertEquals(1, wait_text_milliseconds.params["ms"])
        self.assertEquals(1, wait_text_ms.params["ms"])

    def test_create_say(self):
        say_params = say_command(text="Hello")
        say_text_say = say_command.from_string("say 'Goodbye'")
        say_text_tell = say_command.from_string("tell 'Goodbye'")
        say_text_ask = say_command.from_string("ask 'Goodbye'")
        say_text_ask_spaces = say_command.from_string("ask 'Are you ok?'")

        self.assertEquals('Hello', say_params.params["text"])
        self.assertEquals('goodbye', say_text_say.params["text"])
        self.assertEquals('goodbye', say_text_tell.params["text"])
        self.assertEquals('goodbye', say_text_ask.params["text"])
        self.assertEquals('are_you_ok?', say_text_ask_spaces.params["text"])


    def create_move(self):
        pass


    def test_create_goto(self):
        goto_params = GoTo(where=2.00)
        goto_text = GoTo.from_string("Go to state 2")

        self.assertEquals(2.00, goto_params.params["where"])
        self.assertEquals(2.00, goto_text.params["where"])

    def test_create_button_press(self):
        button_press_params = button_press(button='A')
        button_press_text = button_press.from_string("I press A")

        self.assertEquals('A', button_press_params.params["button"])
        self.assertEquals('a', button_press_text.params["button"])