from unittest import TestCase
from translator.executables.nlp.components.execution import parallel
from translator.executables.nlp.components.moves.demo_moves import dance
from translator.executables.nlp.components.robot_commands import *
from translator.executables.nlp.grammar.grammar import Grammar
from translator.executables.nlp.substep import SubStep

__author__ = 'nina'


class GrammarTests(TestCase):
    def test_translate_general(self):
        gr = Grammar()

        def rule(first, second, third, step_counter):
            new_step = SubStep()
            new_step.text_index_start = first.text_index_start
            new_step.tivipe_component_name = first.tivipe_component_name
            new_step.description = first.description + " " + third.description
            new_step.ID = "%.2f" % step_counter
            new_step.commands.append(first)
            new_step.commands.append(third)

            return new_step

        gr.appendRule(
            input={"first": command, "second": parallel, "third": command},
            transformation=rule
        )

        new_sequence = gr.process([say_command.from_string("Say 'hi'"), parallel(), dance])

        self.assertIsInstance(new_sequence[0], SubStep)
