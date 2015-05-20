import json
from unittest import TestCase
from translator.executables.nlp import translator, ProgramEditor
from translator.executables.nlp.substep import SubStep, ConditionSubStep

__author__ = 'NBUCHINA'


class ProgramEditorTests(TestCase):
    def getSampleSteps(self):
        steps = [
            translator.translate("When I press Y, say 'Yes'. Then wait for 1 second, then say 'Maybe' and go to step 2",
                                 1),
            translator.translate("When I press Y, say 'Yes'. When I press N, say 'No'. Go to step 3", 2),
            translator.translate("shake and say 'I dont know who I am anymore'", 3),
        ]

        return steps

    def test_update_substep_no_input_steps_stay_the_same(self):
        sample_steps = self.getSampleSteps()
        new_steps = ProgramEditor.update_substep(sample_steps, '1.00', [], [], [], [], [], [])
        self.assertEqual(sample_steps, new_steps)

        new_steps = ProgramEditor.update_substep(sample_steps, '1.01', [], [], [], [], [], [])
        self.assertEqual(sample_steps, new_steps)

        new_steps = ProgramEditor.update_substep(sample_steps, '1.02', [], [], [], [], [], [])
        self.assertEqual(sample_steps, new_steps)

        new_steps = ProgramEditor.update_substep(sample_steps, '2.00', [], [], [], [], [], [])
        self.assertEqual(sample_steps, new_steps)

        new_steps = ProgramEditor.update_substep(sample_steps, '2.01', [], [], [], [], [], [])
        self.assertEqual(sample_steps, new_steps)

        new_steps = ProgramEditor.update_substep(sample_steps, '3.00', [], [], [], [], [], [])
        self.assertEqual(sample_steps, new_steps)

    def test_update_substep_remove_action(self):
        sample_steps = self.getSampleSteps()
        new_steps = ProgramEditor.update_substep(sample_steps, '1.00', actions_to_remove=[0])
        new_commands = new_steps[0][0].commands
        self.assertTrue(len(new_commands) == 0)

        new_steps = ProgramEditor.update_substep(sample_steps, '1.01', actions_to_remove=[0])
        new_commands = new_steps[0][1].commands
        self.assertTrue(len(new_commands) == 0)

        new_steps = ProgramEditor.update_substep(sample_steps, '2.01', actions_to_remove=[0])
        new_commands = new_steps[1][1].commands
        not_affected_commands = new_steps[1][0].commands
        self.assertTrue(len(new_commands) == 0)
        self.assertTrue(len(not_affected_commands) == 1)

        new_steps = ProgramEditor.update_substep(sample_steps, '3.00', actions_to_remove=[0])
        new_commands = new_steps[2][0].commands
        self.assertTrue(len(new_commands) == 1)


    def test_update_substep_remove_condition(self):
        sample_steps = self.getSampleSteps()
        new_steps = ProgramEditor.update_substep(sample_steps, '1.00', conditions_to_remove=[0])
        new_substep = new_steps[0][0]
        self.assertIsInstance(new_substep, SubStep)
        self.assertNotIsInstance(new_substep, ConditionSubStep)

        new_steps = ProgramEditor.update_substep(sample_steps, '2.01', conditions_to_remove=[0])
        new_substep = new_steps[1][1]
        self.assertIsInstance(new_substep, SubStep)
        self.assertNotIsInstance(new_substep, ConditionSubStep)

    def test_update_substep_change_actions(self):
        sample_steps = self.getSampleSteps()
        new_action = {"text": "Omg Yes Yes Yes"}
        new_action_json = json.dumps(new_action)

        change_actions = [new_action_json]

        new_steps = ProgramEditor.update_substep(sample_steps, '1.00', change_actions=change_actions)
        new_command = new_steps[0][0].commands
        self.assertEquals(1, len(new_command))
        self.assertEquals('say(Omg Yes Yes Yes)', str(new_command[0]))

        new_steps = ProgramEditor.update_substep(sample_steps, '2.01', change_actions=change_actions)
        new_command = new_steps[1][1].commands
        self.assertEquals(1, len(new_command))
        self.assertEquals('say(Omg Yes Yes Yes)', str(new_command[0]))

        new_steps = ProgramEditor.update_substep(sample_steps, '1.01', change_actions=change_actions)
        new_command = new_steps[0][1].commands
        self.assertEquals(1, len(new_command))
        self.assertEquals('wait(1000)', str(new_command[0]))

    def test_update_substep_change_conditions(self):
        sample_steps = self.getSampleSteps()
        new_condition = {"button": "b"}
        new_condition_json = json.dumps(new_condition)

        change = [new_condition_json]

        new_steps = ProgramEditor.update_substep(sample_steps, '1.00', change_conditions=change)
        new_condition = new_steps[0][0].condition
        self.assertEquals(1, len(new_condition))
        self.assertEquals('key[b]->', str(new_condition[0]))

        new_steps = ProgramEditor.update_substep(sample_steps, '2.01', change_conditions=change)
        new_condition = new_steps[1][1].condition
        self.assertEquals(1, len(new_condition))
        self.assertEquals('key[b]->', str(new_condition[0]))

    def test_update_substep_add_actions(self):
        sample_steps = self.getSampleSteps()
        # new_action = {"class": "say_command", "text":"I wish i knew..."}
        new_action = {"class": "say_command", "text": "I wish i knew..."}
        new_action_json = json.dumps(new_action)
        addition = [new_action_json]

        new_steps = ProgramEditor.update_substep(sample_steps, '1.01', actions_to_add=addition)
        new_command = new_steps[0][1].commands
        self.assertEquals(2, len(new_command))
        self.assertEquals('say(I wish i knew...)', str(new_command[1]))