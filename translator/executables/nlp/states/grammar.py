from translator.executables.nlp.components.component import *
from translator.executables.nlp.components.execution import *
from translator.executables.nlp.components.robot_commands import Command
from translator.executables.nlp.states.state import State, ConditionState, SelectByKeyState

__author__ = 'NBUCHINA'

gone_through = False
state_counter = 1
state_modifier = 0.01
unrecognised_enabled = True


def go_through(components_list):
    global state_counter
    global state_modifier
    global gone_through
    global unrecognised_enabled
    # unrecognised_enabled = False

    new_list = []
    gone_through = True

    i = -1
    while i < len(components_list) - 1:
        i += 1

        # Remove unrecognised if not allowed
        if (not unrecognised_enabled) and isinstance(components_list[i], UnrecognisedComponent):
            gone_through = False
            new_list.extend(components_list[i + 1:])
            break

        # ========  Grammar rules start here =======  #
        # 3-tuple #
        if i < len(components_list) - 2:

            if isinstance(components_list[i], Command) \
                    and isinstance(components_list[i + 1], Parallel) \
                    and isinstance(components_list[i + 2], Command):
                new_state = State()
                new_state.text_index_start = components_list[i].text_index_start
                new_state.tivipe_component_name = components_list[i].tivipe_component_name
                new_state.description = components_list[i].description + " " + components_list[i + 2].description
                new_state.ID = "%.2f" % state_counter
                new_state.commands.append(components_list[i])
                new_state.commands.append(components_list[i + 2])

                state_counter += state_modifier
                new_list.append(new_state)

                gone_through = False
                new_list.extend(components_list[i + 3:])
                break

            elif isinstance(components_list[i], State) \
                    and isinstance(components_list[i + 1], Parallel) \
                    and isinstance(components_list[i + 2], Command):
                new_state = components_list[i]
                new_state.description = components_list[i].description + " " + components_list[i + 2].description
                new_state.commands.append(components_list[i + 2])

                new_list.append(new_state)

                gone_through = False
                new_list.extend(components_list[i + 3:])
                break

            elif isinstance(components_list[i], Command) \
                    and isinstance(components_list[i + 1], Parallel) \
                    and isinstance(components_list[i + 2], State):
                new_state = components_list[i + 2]
                new_state.text_index_start = components_list[i].text_index_start
                new_state.tivipe_component_name = components_list[i].tivipe_component_name
                new_state.description = components_list[i].description + " " + components_list[i + 2].description
                new_state.commands.append(components_list[i])

                new_list.append(new_state)

                gone_through = False
                new_list.extend(components_list[i + 3:])
                break

            elif isinstance(components_list[i], State) \
                    and isinstance(components_list[i + 1], Parallel) \
                    and isinstance(components_list[i + 2], State):
                new_state = State()
                new_state.text_index_start = components_list[i].text_index_start
                new_state.tivipe_component_name = components_list[i].tivipe_component_name
                new_state.description = components_list[i].description + " " + components_list[i + 2].description
                new_state.ID = components_list[i].ID
                new_state.commands.extend(components_list[i].commands)
                new_state.commands.extend(components_list[i + 2].commands)

                new_list.append(new_state)

                gone_through = False
                new_list.extend(components_list[i + 3:])
                break

            elif isinstance(components_list[i], State) \
                    and isinstance(components_list[i + 1], Sequence) \
                    and isinstance(components_list[i + 2], State):
                step1 = components_list[i]
                step2 = components_list[i + 2]

                step1.next_ID = step2.ID

                new_list.append(step1)
                new_list.append(step2)

                gone_through = False
                new_list.extend(components_list[i + 3:])
                break

        # ==== 2-tuple ===== #
        if i < len(components_list) - 1:

            if isinstance(components_list[i], Parallel) and isinstance(components_list[i + 1], Sequence):
                new_list.append(components_list[i + 1])

                gone_through = False
                new_list.extend(components_list[i + 2:])
                break

            elif (isinstance(components_list[i], Parallel) or isinstance(components_list[i], Sequence)) \
                    and isinstance(components_list[i + 1], GoTo):
                new_list.append(components_list[i + 1])

                gone_through = False
                new_list.extend(components_list[i + 2:])
                break

            elif isinstance(components_list[i], UnrecognisedComponent) \
                    and isinstance(components_list[i + 1], UnrecognisedComponent):
                unrec1 = components_list[i]
                unrec2 = components_list[i + 1]
                new_list.append(
                    UnrecognisedComponent.from_string(unrec1.description + " " + unrec2.description,
                                                       unrec1.text_index_start))

                gone_through = False
                new_list.extend(components_list[i + 2:])
                break

            elif isinstance(components_list[i], Condition) and isinstance(components_list[i + 1], GoTo):
                new_state = ConditionState()
                new_state.text_index_start = components_list[i].text_index_start
                new_state.tivipe_component_name = components_list[i].tivipe_component_name
                new_state.description = components_list[i].description + " " + components_list[i + 1].description
                new_state.ID = "%.2f" % state_counter
                new_state.uID = "%.2f" % state_counter
                new_state.next_ID = "%.2f" % components_list[i + 1].params["where"]
                new_state.condition.append(components_list[i])

                state_counter += state_modifier
                new_list.append(new_state)

                gone_through = False
                new_list.extend(components_list[i + 2:])
                break

            elif isinstance(components_list[i], State) and isinstance(components_list[i + 1], GoTo):
                new_state = components_list[i]
                goto_pointer = components_list[i + 1]

                new_state.next_ID = "%.2f" % goto_pointer.params["where"]
                new_list.append(new_state)

                gone_through = False
                new_list.extend(components_list[i + 2:])
                break

            elif isinstance(components_list[i], Condition) and isinstance(components_list[i + 1], Command):
                cond = components_list[i]
                action = components_list[i + 1]

                new_state = ConditionState()
                new_state.text_index_start = cond.text_index_start
                new_state.tivipe_component_name = cond.tivipe_component_name
                new_state.description = cond.description + " " + action.description
                new_state.ID = "%.2f" % state_counter
                new_state.uID = "%.2f" % state_counter
                new_state.commands.append(action)
                new_state.condition.append(cond)

                state_counter += state_modifier
                new_list.append(new_state)

                gone_through = False
                new_list.extend(components_list[i + 2:])
                break

            elif isinstance(components_list[i], Condition) and isinstance(components_list[i + 1], State):
                cond = components_list[i]
                action = components_list[i + 1]

                new_state = ConditionState()
                new_state.text_index_start = cond.text_index_start
                new_state.tivipe_component_name = cond.tivipe_component_name
                new_state.description = cond.description + " " + action.description
                new_state.ID = action.ID
                new_state.uID = action.ID
                new_state.commands.extend(action.commands)
                new_state.condition.append(cond)

                new_list.append(new_state)

                gone_through = False
                new_list.extend(components_list[i + 2:])
                break

            elif (isinstance(components_list[i], State)
                  and isinstance(components_list[i + 1], State)) \
                    and components_list[i].next_ID == -1:

                step1 = components_list[i]
                step2 = components_list[i + 1]

                step1.next_ID = step2.ID

                new_list.append(step1)
                new_list.append(step2)

                gone_through = False
                new_list.extend(components_list[i + 2:])
                break

        # ==== 1-tuple ==== #
        if isinstance(components_list[i], Command):
            new_state = State()
            new_state.text_index_start = components_list[i].text_index_start
            new_state.tivipe_component_name = components_list[i].tivipe_component_name
            new_state.description = components_list[i].description
            new_state.ID = "%.2f" % state_counter
            new_state.commands.append(components_list[i])

            state_counter += state_modifier
            new_list.append(new_state)

            gone_through = False

            new_list.extend(components_list[i + 1:])
            break

        if isinstance(components_list[i], UnrecognisedComponent):
            if (i > 0 and not isinstance(components_list[i - 1], UnrecognisedComponent)) or i == 0:
                new_state = State()
                new_state.text_index_start = components_list[i].text_index_start
                new_state.tivipe_component_name = components_list[i].tivipe_component_name
                new_state.description = components_list[i].description
                new_state.ID = "%.2f" % state_counter
                new_state.commands.append(components_list[i])

                state_counter += state_modifier
                new_list.append(new_state)

                gone_through = False

                new_list.extend(components_list[i + 1:])
                break

        new_list.append(components_list[i])
    # ======== Grammar rules end here ======== #

    if gone_through:
        state_counter = 1

        new_new_list = []

        # Remove orphan controls, then go through once again
        orphans = 0
        for item in new_list:
            if not (isinstance(item, Parallel) or isinstance(item, Sequence)):
                new_new_list.append(item)
            else:
                orphans += 1

        if orphans > 0:
            return go_through(new_new_list)
        else:
            return new_new_list

    else:
        return go_through(new_list)


# TODO: Only unite keys?
def unite_condition_states(states_list):
    first_condition_state_id = -1

    disappearing_states = []
    for state in states_list:
        if isinstance(state, ConditionState):
            if first_condition_state_id == -1:
                first_condition_state_id = state.ID

            if state.ID != first_condition_state_id:
                disappearing_states.append(state.ID)
                state.ID = first_condition_state_id

    for state in states_list:
        if state.next_ID in disappearing_states:
            state.next_ID = -1

    return first_condition_state_id


def get_new_list_with_keypress_states(states):
    global state_counter
    first_cstate_id = unite_condition_states(states)
    if first_cstate_id == -1:
        return states

    select_key = SelectByKeyState()

    new_list = []

    for state in states:
        if isinstance(state, ConditionState) and len(state.condition) > 0:
            orphan_state = select_key.add_cstep(state)
            select_key.ID = state.ID

            if orphan_state is not None:
                new_list.append(orphan_state)

        else:
            new_list.append(state)

    new_list.append(select_key)

    return new_list
