from translator.executables.nlp import grammar
from translator.executables.nlp.components.component import *
from unittest import *
from translator.executables.nlp.components.execution import parallel, sequence, goto
from translator.executables.nlp.components.robot_commands import say_command, move_command
from translator.executables.nlp.substep import SubStep, ConditionSubStep

__author__ = 'NBUCHINA'


class GrammarTests(TestCase):
    def test_go_through_many_unrecognised(self):
        components = [
            unrecognised_component.from_string("This is not recognised"),
            unrecognised_component.from_string("This too"),
            unrecognised_component.from_string("NOPE"),
            unrecognised_component.from_string("NOPE"),
            unrecognised_component.from_string("hahaha almost there"),
            unrecognised_component.from_string("Man, this recognition function really sucks"),
        ]

        new_components = grammar.go_through(components)
        # print(new_components)
        self.assertEquals(len(new_components), 1)


    def test_go_through_conditions(self):
        components = [
            button_press(button="A"),
            say_command(text="say 'hello'"),

            button_press.from_string("when I press B"),
            # button_press(button='B'),
            say_command.from_string("say 'bye'"),

            button_press(button="C"),
            say_command(text="say 'OMG'")
        ]

        new_components = grammar.go_through(components)
        self.assertEquals(len(new_components), 3)

        for i in range(0, len(new_components)):
            print(new_components[i].description)
            self.assertEquals(isinstance(new_components[i], SubStep), True)


    def test_go_through_conditions_and_unrecognised(self):
        components = [
            button_press(button="A"),
            say_command(text="say 'hello'"),

            unrecognised_component(unrecognised_text="This is not recognised"),
            unrecognised_component(unrecognised_text="This too"),
            unrecognised_component.from_string("This too"),

            button_press(button="B"),
            say_command(text="say 'bye'"),

            unrecognised_component.from_string("hahaha almost there"),

            button_press.from_string("press C"),
            say_command.from_string("say 'OMG'")
        ]

        new_components = grammar.go_through(components)

        self.assertEquals(len(new_components), 5)


    def test_go_through_many_parallel(self):
        components = [
            say_command(text="say 'hello'"),
            parallel(),
            say_command.from_string("say 'OMG'"),
            parallel(),
            say_command.from_string("say 'OooooIoooooooo'"),
            parallel(),
            say_command.from_string("say 'Owow'")
        ]

        new_components = grammar.go_through(components)
        self.assertEquals(len(new_components), 1)

    def test_go_through_many_individual_commands(self):
        components = [
            say_command(text="say 'hello'"),
            say_command(text="say 'OMG'"),
            say_command(text="say 'OooooIoooooooo'"),
            say_command(text="say 'Owow'")
        ]

        new_components = grammar.go_through(components)
        self.assertEquals(len(new_components), 4)


    def test_handshake_and_nice_to_meet_you(self):
        components = [
            move_command.from_string("handshake"),
            parallel(),
            say_command.from_string("say 'OooooIoooooooo'"),
        ]

        new_components = grammar.go_through(components)
        self.assertEquals(len(new_components), 1)


    def test_goto(self):
        components = [
            move_command.from_string("handshake"),
            parallel(),
            say_command.from_string("say 'OooooIoooooooo'"),
            sequence.from_string("then"),
            goto.from_string("go to state 3")
        ]

        new_components = grammar.go_through(components)
        self.assertEquals(len(new_components), 1)

        only_state = new_components[0]
        self.assertEquals("3.00", only_state.next_ID)


    def test_go_through_order_of_nonrecognised(self):
        components = [
            unrecognised_component.from_string("Cry"),
            unrecognised_component.from_string("again."),
            say_command.from_string("say 'Life has no meaning'"),
        ]

        new_components = grammar.go_through(components)
        self.assertEquals(len(new_components), 2)

    def test_go_through_keypress_goto(self):
        components = [
            button_press.from_string("press Y"),
            goto.from_string("Go to step 3.01"),
        ]

        new_components = grammar.go_through(components)
        self.assertEquals(len(new_components), 1)

        first_state = new_components[0]
        self.assertEquals("3.01", first_state.next_ID)

    def test_go_through_only_steps(self):
        components = [
            button_press(button="A"),
            say_command.from_string("say 'hello'"),

            parallel(),
            parallel(),
            parallel(),
            sequence(),

            unrecognised_component.from_string("This is not recognised"),
            unrecognised_component.from_string("This too"),
            unrecognised_component.from_string("This too"),

            button_press(button="B"),
            parallel(),
            sequence(),
            sequence(),
            sequence(),
            sequence(),
            say_command.from_string("say 'bye'"),

            unrecognised_component.from_string("hahaha almost there"),

            button_press(button="C"),
            sequence(),
            sequence.from_string("then"),
            say_command.from_string("say 'OMG'")
        ]

        new_components = grammar.go_through(components)
        print([x.description for x in new_components])

        for x in new_components:
            if isinstance(x, ConditionSubStep):
                print([x.condition])
            print([x.commands])
        self.assertEquals(len(new_components), 5)
        self.assertTrue(all([isinstance(x, SubStep) for x in new_components]))

