from translator.executables.nlp import commons
from translator.executables.nlp.commons import class_for_name
from translator.executables.nlp.states.state import ConditionState, State, MetaState


__author__ = 'NBUCHINA'


def update_states(states_list, state_id, actions_to_add=None, conditions_to_add=None, actions_to_remove=None,
                  conditions_to_remove=None, change_actions=None, change_conditions=None, change_next_id=None):
    if not conditions_to_remove:
        conditions_to_remove = []
    if not change_actions:
        change_actions = []
    if not actions_to_add:
        actions_to_add = []
    if not actions_to_remove:
        actions_to_remove = []
    if not conditions_to_add:
        conditions_to_add = []
    if not change_conditions:
        change_conditions = []

    conditions_to_remove = set(conditions_to_remove)
    actions_to_remove = set(actions_to_remove)

    new_states = states_list
    for states_for_step in new_states:
        for state in states_for_step:
            if isinstance(state, MetaState):
                for sub_state in state.states:
                    if hasattr(sub_state, 'uID'):
                        state_unique_id = sub_state.uID
                    else:
                        state_unique_id = sub_state.ID

                    if state_unique_id == state_id:
                        update_state(sub_state, actions_to_add, conditions_to_add, actions_to_remove, conditions_to_remove,
                                     change_actions, change_conditions, change_next_id)

            else:
                if hasattr(state, 'uID'):
                    state_unique_id = state.uID
                else:
                    state_unique_id = state.ID

                if state_unique_id == state_id:
                    update_state(state, actions_to_add, conditions_to_add, actions_to_remove, conditions_to_remove,
                                 change_actions, change_conditions, change_next_id)

    return new_states


def update_state(state, actions_to_add=None, conditions_to_add=None, actions_to_remove=None,
                 conditions_to_remove=None, change_actions=None, change_conditions=None, change_next_id=None):
    for i in range(0, len(change_actions)):
        action_params = change_actions[i]
        state.commands[i].load_params(action_params)

    for i in range(0, len(change_conditions)):
        if not hasattr(state, 'condition'):
            break
        condition_params = change_conditions[i]
        state.condition[i].load_params(condition_params)

    if change_next_id and not change_next_id == 0:
        state.next_ID = change_next_id

    # Then remove stuff
    for action_index in actions_to_remove:
        action_index = int(action_index) - 1
        del state.commands[action_index]

    for condition_index in conditions_to_remove:
        if not hasattr(state, 'condition'):
            break
        condition_index = int(condition_index) - 1
        del state.condition[condition_index]
        if len(state.condition) == 0:
            state.__class__ = State

    # Finally, add new stuff
    for action in actions_to_add:
        action_params = action
        action_class_name = action_params["class"]
        action_instance = commons.get_component_by_ref_id(action_class_name)
        action_instance.load_params(action_params["params"])
        state.commands.append(action_instance)

    for condition in conditions_to_add:
        condition_params = condition
        condition_class_name = condition_params["class"]
        condition_instance = commons.get_component_by_ref_id(condition_class_name)
        condition_instance.load_params(condition_params["params"])

        if not hasattr(state, 'condition'):
            state.condition = []
        state.__class__ = ConditionState
        state.condition.append(condition_instance)