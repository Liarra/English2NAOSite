from translator.executables.nlp import grammar
from translator.executables.nlp.components.component import *
from unittest import *
from translator.executables.nlp.components.execution import parallel, sequence, goto
from translator.executables.nlp.components.robot_commands import say_command, move_command
from translator.executables.nlp.step import step

__author__ = 'NBUCHINA'


class GrammarTests(TestCase):
    def test_go_through_many_unrecognised(self):
        components = [
            unrecognised_component("This is not recognised"),
            unrecognised_component("This too"),
            unrecognised_component("NOPE"),
            unrecognised_component("NOPE"),
            unrecognised_component("hahaha almost there"),
            unrecognised_component("Man, this recognition function really sucks"),
        ]

        new_components = grammar.go_through(components)
        print(new_components)
        self.assertEquals(len(new_components), 1)


    def test_go_through_conditions(self):
        components = [
            button_press("A"),
            say_command("say 'hello'"),

            button_press("B"),
            say_command("say 'bye'"),

            button_press("C"),
            say_command("say 'OMG'")
        ]

        new_components = grammar.go_through(components)
        self.assertEquals(len(new_components), 3)

        for i in range(0, len(new_components)):
            # print(new_components[i].description)
            self.assertEquals(isinstance(new_components[i], step), True)


    def test_go_through_conditions_and_unrecognised(self):
        components = [
            button_press("A"),
            say_command("say 'hello'"),

            unrecognised_component("This is not recognised"),
            unrecognised_component("This too"),
            unrecognised_component("This too"),

            button_press("B"),
            say_command("say 'bye'"),

            unrecognised_component("hahaha almost there"),

            button_press("C"),
            say_command("say 'OMG'")
        ]

        new_components = grammar.go_through(components)
        print([x.description for x in new_components])
        self.assertEquals(len(new_components), 5)


    def test_go_through_many_parallel(self):
        components = [
            say_command("say 'hello'"),
            parallel("and"),
            say_command("say 'OMG'"),
            parallel("and"),
            say_command("say 'OooooIoooooooo'"),
            parallel("and"),
            say_command("say 'Owow'")
        ]

        new_components = grammar.go_through(components)
        self.assertEquals(len(new_components), 1)

    def test_go_through_many_individual_commands(self):
        components = [
            say_command("say 'hello'"),
            say_command("say 'OMG'"),
            say_command("say 'OooooIoooooooo'"),
            say_command("say 'Owow'")
        ]

        new_components = grammar.go_through(components)
        self.assertEquals(len(new_components), 4)


    def test_handshake_and_nice_to_meet_you(self):
        components = [
            move_command("handshake"),
            parallel("and"),
            say_command("say 'OooooIoooooooo'"),
        ]

        new_components = grammar.go_through(components)
        self.assertEquals(len(new_components), 1)


    def test_goto(self):
        components = [
            move_command("handshake"),
            parallel("and"),
            say_command("say 'OooooIoooooooo'"),
            goto("go to state 3")
        ]

        new_components = grammar.go_through(components)
        self.assertEquals(len(new_components), 1)

        only_state = new_components[0]
        self.assertEquals(only_state.next_state_ID, 3)


    def test_go_through_order_of_nonrecognised(self):
        components = [
            unrecognised_component("Cry"),
            unrecognised_component("again."),
            say_command("say 'Life has no meaning'"),
        ]

        new_components = grammar.go_through(components)
        self.assertEquals(len(new_components), 2)

        first_state = new_components[0]
        print(first_state.commands[0])
        print(first_state.state_ID)
        print(first_state.next_state_ID)