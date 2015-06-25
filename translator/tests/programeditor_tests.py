from unittest import TestCase

from translator.executables.nlp.states import program_editor

from translator.executables.nlp.translation import translator
from translator.executables.nlp.states.state import State, ConditionState


__author__ = 'NBUCHINA'


class ProgramEditorTests(TestCase):
    def getSampleStates(self):
        steps = [
            translator.translate("When I press Y, say 'Yes'. Then wait for 1 second, then say 'Maybe' and go to step 2",
                                 1),
            translator.translate("When I press Y, say 'Yes'. When I press N, say 'No'. Go to step 3", 2),
            translator.translate("shake and say 'I dont know who I am anymore'", 3),
            translator.translate("when I press z, dance and say 'Naah whatever'", 4),
        ]

        return steps

    def test_update_state_no_input_states_stay_the_same(self):
        sample_states = self.getSampleStates()
        new_states = program_editor.update_state(sample_states, '1.00', [], [], [], [], [], [])
        self.assertEqual(sample_states, new_states)

        new_states = program_editor.update_state(sample_states, '1.01', [], [], [], [], [], [])
        self.assertEqual(sample_states, new_states)

        new_states = program_editor.update_state(sample_states, '1.02', [], [], [], [], [], [])
        self.assertEqual(sample_states, new_states)

        new_states = program_editor.update_state(sample_states, '2.00', [], [], [], [], [], [])
        self.assertEqual(sample_states, new_states)

        new_states = program_editor.update_state(sample_states, '2.01', [], [], [], [], [], [])
        self.assertEqual(sample_states, new_states)

        new_states = program_editor.update_state(sample_states, '3.00', [], [], [], [], [], [])
        self.assertEqual(sample_states, new_states)

    def test_update_state_remove_action(self):
        sample_states = self.getSampleStates()
        new_states = program_editor.update_state(sample_states, '1.00', actions_to_remove=[0])
        new_commands = new_states[0][0].commands
        self.assertTrue(len(new_commands) == 0)

        new_states = program_editor.update_state(sample_states, '1.01', actions_to_remove=[0])
        new_commands = new_states[0][1].commands
        self.assertTrue(len(new_commands) == 0)

        new_states = program_editor.update_state(sample_states, '2.01', actions_to_remove=[0])
        new_commands = new_states[1][1].commands
        not_affected_commands = new_states[1][0].commands
        self.assertTrue(len(new_commands) == 0)
        self.assertTrue(len(not_affected_commands) == 1)

        new_states = program_editor.update_state(sample_states, '3.00', actions_to_remove=[0])
        new_commands = new_states[2][0].commands
        self.assertTrue(len(new_commands) == 1)


    def test_update_state_remove_condition(self):
        sample_states = self.getSampleStates()
        new_states = program_editor.update_state(sample_states, '1.00', conditions_to_remove=[0])
        new_state = new_states[0][0]
        self.assertIsInstance(new_state, State)
        self.assertNotIsInstance(new_state, ConditionState)

        new_states = program_editor.update_state(sample_states, '2.01', conditions_to_remove=[0])
        new_state = new_states[1][1]
        self.assertIsInstance(new_state, State)
        self.assertNotIsInstance(new_state, ConditionState)

    def test_update_state_change_actions(self):
        sample_states = self.getSampleStates()
        new_action = {"text": "Omg Yes Yes Yes"}
        #new_action_json = json.dumps(new_action)

        change_actions = [new_action]

        new_states = program_editor.update_state(sample_states, '1.00', change_actions=change_actions)
        new_command = new_states[0][0].commands
        self.assertEquals(1, len(new_command))
        self.assertEquals('[say(Omg Yes Yes Yes)]', str(new_command[0]))

        new_states = program_editor.update_state(sample_states, '2.01', change_actions=change_actions)
        new_command = new_states[1][1].commands
        self.assertEquals(1, len(new_command))
        self.assertEquals('[say(Omg Yes Yes Yes)]', str(new_command[0]))

        new_states = program_editor.update_state(sample_states, '1.01', change_actions=change_actions)
        new_command = new_states[0][1].commands
        self.assertEquals(1, len(new_command))
        self.assertEquals('wait(1000)', str(new_command[0]))

    def test_update_state_change_conditions(self):
        sample_states = self.getSampleStates()
        new_condition = {"button": "b"}
        #new_condition_json = json.dumps(new_condition)

        change = [new_condition]

        new_states = program_editor.update_state(sample_states, '1.00', change_conditions=change)
        new_condition = new_states[0][0].condition
        self.assertEquals(1, len(new_condition))
        self.assertEquals('key[b]->', str(new_condition[0]))

        new_states = program_editor.update_state(sample_states, '2.01', change_conditions=change)
        new_condition = new_states[1][1].condition
        self.assertEquals(1, len(new_condition))
        self.assertEquals('key[b]->', str(new_condition[0]))

    def test_update_state_add_actions(self):
        sample_states = self.getSampleStates()
        # new_action = {"class": "say_command", "text":"I wish i knew..."}
        new_action = {"class": "say_command", "params": {"text": "I wish i knew..."}}
        #new_action_json = json.dumps(new_action)
        addition = [new_action]

        new_states = program_editor.update_state(sample_states, '1.01', actions_to_add=addition)
        new_command = new_states[0][1].commands
        self.assertEquals(2, len(new_command))
        self.assertEquals('[say(I wish i knew...)]', str(new_command[1]))


    def test_update_state_add_conditions(self):
        sample_states = self.getSampleStates()
        # new_action = {"class": "say_command", "text":"I wish i knew..."}
        new_condition = {"class": "button_press", "params":{"button": "A"}}
        #new_condition_json = json.dumps(new_condition)
        addition = [new_condition]

        new_states = program_editor.update_state(sample_states, '3.00', conditions_to_add=addition)
        new_state = new_states[2][0]
        self.assertIsInstance(new_state, ConditionState)
        self.assertEquals(1, len(new_state.condition))
        self.assertEquals('key[A]->', str(new_state.condition[0]))

        new_states = program_editor.update_state(sample_states, '1.00', conditions_to_add=addition)
        new_state = new_states[0][0]
        self.assertIsInstance(new_state, ConditionState)
        self.assertEquals(2, len(new_state.condition))
        self.assertEquals('key[A]->', str(new_state.condition[1]))


    def test_update_state_mixed_change(self):
        sample_states = self.getSampleStates()

        # Add press A condition and cry action
        new_action = {"class": "move_command", "params": { "name": "Cry"}}
        new_condition = {"class": "button_press", "params": {"button": "A"}}

        action_addition = [new_action]
        condition_addition = [new_condition]

        # Remove press z condition and dance action
        remove_actions = [0]
        remove_conditions = [0]

        #Change a say action
        change_action = {"text": "No"}
        change_actions = [{}, change_action]

        new_states = program_editor.update_state(sample_states, '4.00',
                                                actions_to_add=action_addition, conditions_to_add=condition_addition,
                                                actions_to_remove=remove_actions,
                                                conditions_to_remove=remove_conditions,
                                                change_actions=change_actions)

        new_state = new_states[3][0]
        self.assertIsInstance(new_state, ConditionState)
        self.assertEquals(1, len(new_state.condition))
        self.assertEquals(2, len(new_state.commands))
        self.assertEquals('key[A]->', str(new_state.condition[0]))
        self.assertEquals('[say(No)]', str(new_state.commands[0]))
        self.assertEquals('Cry', str(new_state.commands[1].params["name"]))