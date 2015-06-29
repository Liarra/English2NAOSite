from unittest import TestCase
from translator.executables.nlp.components.execution import Parallel
from translator.executables.nlp.components.moves.demo_moves import dance
from translator.executables.nlp.components.robot_commands import *
from translator.executables.nlp.grammar import id_pool
from translator.executables.nlp.grammar.grammar import Grammar
from translator.executables.nlp.states.state import State

__author__ = 'nina'


class GrammarTests(TestCase):
    def test_translate_general(self):
        gr = Grammar()

        def rule(first, second, third):
            new_step = State()
            new_step.text_index_start = first.text_index_start
            new_step.tivipe_component_name = first.tivipe_component_name
            new_step.description = first.description + " " + third.description
            new_step.ID = "%.2f" % id_pool.get_float_id()
            new_step.commands.append(first)
            new_step.commands.append(third)

            return [new_step]

        gr.append_rule(
            input=[("first", Command), ("second", Parallel), ("third", Command)],
            transformation=rule
        )

        new_sequence = gr.process([say_command.from_string("Say 'hi'"), Parallel(), dance])

        self.assertIsInstance(new_sequence[0], State)

    def test_add_new_rule(self):
        gr = Grammar()

        def rule(first, second, third, step_counter):
            new_step = State()
            new_step.text_index_start = first.text_index_start
            new_step.tivipe_component_name = first.tivipe_component_name
            new_step.description = first.description + " " + third.description
            new_step.ID = "%.2f" % step_counter
            new_step.commands.append(first)
            new_step.commands.append(third)

            return [new_step]

        gr.append_rule(
            input=[("first", Command), ("second", Parallel), ("third", Command)],
            transformation=rule
        )

        self.assertEquals(rule, gr.rules[0].transformation)