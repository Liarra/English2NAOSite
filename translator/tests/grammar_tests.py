from unittest import TestCase

from translator.executables.nlp.components.component import *
from translator.executables.nlp.components.execution import Parallel, Sequence, GoTo
from translator.executables.nlp.components.moves.demo_moves import *
from translator.executables.nlp.components.robot_commands import say_command, move_command, button_press
from translator.executables.nlp.states import grammar
from translator.executables.nlp.states.state import State, ConditionState


__author__ = 'NBUCHINA'


class GrammarTests(TestCase):
    def test_transform_many_unrecognised(self):
        components = [
            UnrecognisedComponent.from_string("This is not recognised"),
            UnrecognisedComponent.from_string("This too"),
            UnrecognisedComponent.from_string("NOPE"),
            UnrecognisedComponent.from_string("NOPE"),
            UnrecognisedComponent.from_string("hahaha almost there"),
            UnrecognisedComponent.from_string("Man, this recognition function really sucks"),
        ]

        new_components = grammar.transform(components)
        self.assertEquals(len(new_components), 1)


    def test_transform_conditions(self):
        components = [
            button_press(button="A"),
            say_command(text="say 'hello'"),

            button_press.from_string("press B"),
            # button_press(button='B'),
            say_command.from_string("say 'bye'"),

            button_press(button="C"),
            say_command(text="say 'OMG'")
        ]

        new_components = grammar.transform(components)
        self.assertEquals(len(new_components), 3)

        for i in range(0, len(new_components)):
            print(new_components[i].description)
            self.assertEquals(isinstance(new_components[i], State), True)


    def test_transform_conditions_and_unrecognised(self):
        components = [
            button_press(button="A"),
            say_command(text="say 'hello'"),

            UnrecognisedComponent(unrecognised_text="This is not recognised"),
            UnrecognisedComponent(unrecognised_text="This too"),
            UnrecognisedComponent.from_string("This too"),

            button_press(button="B"),
            say_command(text="say 'bye'"),

            UnrecognisedComponent.from_string("hahaha almost there"),

            button_press(button="C"),
            say_command.from_string("say 'OMG'")
        ]

        new_components = grammar.transform(components)

        self.assertEquals(len(new_components), 5)


    def test_transform_many_parallel(self):
        components = [
            say_command(text="say 'hello'"),
            Parallel(),
            say_command.from_string("say 'OMG'"),
            Parallel(),
            say_command.from_string("say 'OooooIoooooooo'"),
            Parallel(),
            say_command.from_string("say 'Owow'")
        ]

        new_components = grammar.transform(components)
        self.assertEquals(len(new_components), 1)

    def test_transform_many_individual_commands(self):
        components = [
            say_command(text="say 'hello'"),
            say_command(text="say 'OMG'"),
            say_command(text="say 'OooooIoooooooo'"),
            say_command(text="say 'Owow'")
        ]

        new_components = grammar.transform(components)
        self.assertEquals(len(new_components), 4)


    def test_handshake_and_nice_to_meet_you(self):
        components = [
            handshake.from_string("handshake"),
            Parallel(),
            say_command.from_string("say 'OooooIoooooooo'"),
        ]

        new_components = grammar.transform(components)
        self.assertEquals(len(new_components), 1)


    def test_goto(self):
        components = [
            handshake.from_string("handshake"),
            Parallel(),
            say_command.from_string("say 'OooooIoooooooo'"),
            Sequence.from_string("then"),
            GoTo.from_string("go to state 3")
        ]

        new_components = grammar.transform(components)
        self.assertEquals(len(new_components), 1)

        only_state = new_components[0]
        self.assertEquals("3.00", only_state.next_ID)


    def test_transform_order_of_nonrecognised(self):
        components = [
            UnrecognisedComponent.from_string("Cry"),
            UnrecognisedComponent.from_string("again."),
            say_command.from_string("say 'Life has no meaning'"),
        ]

        new_components = grammar.transform(components)
        self.assertEquals(len(new_components), 2)

    def test_transform_keypress_goto(self):
        components = [
            button_press(button="y"),
            GoTo.from_string("Go to step 3.01"),
        ]

        new_components = grammar.transform(components)
        self.assertEquals(len(new_components), 1)

        first_state = new_components[0]
        self.assertEquals("3.01", first_state.next_ID)

    def test_transform_only_steps(self):
        components = [
            button_press(button="A"),
            say_command.from_string("say 'hello'"),

            Parallel(),
            Parallel(),
            Parallel(),
            Sequence(),

            UnrecognisedComponent.from_string("This is not recognised"),
            UnrecognisedComponent.from_string("This too"),
            UnrecognisedComponent.from_string("This too"),

            button_press(button="B"),
            Parallel(),
            Sequence(),
            Sequence(),
            Sequence(),
            Sequence(),
            say_command.from_string("say 'bye'"),

            UnrecognisedComponent.from_string("hahaha almost there"),

            button_press(button="C"),
            Sequence(),
            Sequence.from_string("then"),
            say_command.from_string("say 'OMG'")
        ]

        new_components = grammar.transform(components)
        print([x.description for x in new_components])

        for x in new_components:
            if isinstance(x, ConditionState):
                print([x.condition])
            print([x.commands])
        self.assertEquals(len(new_components), 5)
        self.assertTrue(all([isinstance(x, State) for x in new_components]))


    def test_many_ands(self):
        components = [
            wave,
            Parallel(),
            nod,
            Parallel(),
            handshake,
            Parallel(),
            wave,
        ]

        new_components = grammar.transform(components)
        self.assertEquals(1, len(new_components))

        commands = new_components[0].commands
        self.assertTrue(all(isinstance(x, move_command) for x in commands))