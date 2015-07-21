from translator.executables.nlp.components.component import *
from translator.executables.nlp.components.execution import *
from translator.executables.nlp.components.robot_commands import Command
from translator.executables.nlp.states import id_pool
from translator.executables.nlp.Type0py.grammar import Grammar
from translator.executables.nlp.states.state import State, ConditionState, SelectByKeyState

__author__ = 'NBUCHINA'

state_counter = 1
unrecognised_enabled = True


def remove_unrecognised(unrecognised):
    return []


def parallel_commands(c1, p, c2):
    new_state = State()
    new_state.text_index_start = c1.text_index_start
    new_state.tivipe_component_name = c1.tivipe_component_name
    new_state.description = c1.description + ", " + c2.description
    new_state.ID = "%.2f" % id_pool.get_float_id(state_counter)
    new_state.commands.append(c1)
    new_state.commands.append(c2)

    return [new_state]


def command_parallel_state(c1, p, s2):
    new_state = s2
    new_state.text_index_start = c1.text_index_start
    new_state.tivipe_component_name = c1.tivipe_component_name
    new_state.description = c1.description + " " + s2.description
    new_state.commands.append(c1)

    return [new_state]


def state_parallel_command(s1, p, c2):
    new_state = s1
    new_state.description = s1.description + ", " + c2.description
    new_state.commands.append(c2)

    return [new_state]


def state_parallel_state(s1, p, s2):
    new_state = State()
    new_state.text_index_start = s1.text_index_start
    new_state.tivipe_component_name = s1.tivipe_component_name
    new_state.description = s1.description + ", " + s2.description
    new_state.ID = s1.ID
    new_state.commands.extend(s1.commands)
    new_state.commands.extend(s2.commands)

    return [new_state]


def state_sequence_state(s1, s, s2):
    step1 = s1
    step2 = s2

    step1.next_ID = step2.ID

    return [step1, step2]


def parallel_sequence(p, s):
    return [s]


def parallel_goto(p, g):
    return [g]


def define_two_unrecognised(u1, u2):
    return [UnrecognisedComponent.from_string(u1.description + ", " + u2.description, u1.text_index_start)]


def condition_goto(c, g):
    new_state = ConditionState()
    new_state.text_index_start = c.text_index_start
    new_state.tivipe_component_name = c.tivipe_component_name
    new_state.description = c.description + ", " + g.description
    new_state.ID = new_state.uID = "%.2f" % id_pool.get_float_id(state_counter)
    new_state.next_ID = "%.2f" % g.params["where"]
    new_state.condition.append(c)

    return [new_state]


def state_goto(s, g):
    new_state = s
    new_state.next_ID = "%.2f" % g.params["where"]

    return [new_state]


def condition_command(cnd, c):
    new_state = ConditionState()
    new_state.text_index_start = cnd.text_index_start
    new_state.tivipe_component_name = cnd.tivipe_component_name
    new_state.description = cnd.description + ", " + c.description
    new_state.ID = new_state.uID = "%.2f" % id_pool.get_float_id(state_counter)
    new_state.commands.append(c)
    new_state.condition.append(cnd)

    return [new_state]


def condition_state(cnd, s):
    new_state = ConditionState()
    new_state.text_index_start = cnd.text_index_start
    new_state.tivipe_component_name = cnd.tivipe_component_name
    new_state.description = cnd.description + ", " + s.description
    new_state.ID = s.ID
    new_state.uID = s.ID
    new_state.commands.extend(s.commands)
    new_state.condition.append(cnd)

    return [new_state]


def command(c):
    new_state = State()
    new_state.text_index_start = c.text_index_start
    new_state.tivipe_component_name = c.tivipe_component_name
    new_state.description = c.description
    new_state.ID = "%.2f" % id_pool.get_float_id(state_counter)
    new_state.commands.append(c)

    return [new_state]


def transform(components_list):
    id_pool.reset()

    ret_list = grammar_transform(components_list)
    ret_list = remove_orphans(ret_list)
    arrange_identifiers(ret_list)

    return ret_list


def grammar_transform(components_list):
    gr = Grammar()
    gr.append_rule(input=[("unrecognised", IgnoredComponent)], transformation=remove_unrecognised)

    gr.append_rule(input=[("c1", Command), ("p", Parallel), ("c2", Command)], transformation=parallel_commands)
    gr.append_rule(input=[("c1", Command), ("p", Parallel), ("s2", State)], transformation=command_parallel_state)
    gr.append_rule(input=[("s1", State), ("p", Parallel), ("c2", Command)], transformation=state_parallel_command)
    gr.append_rule(input=[("s1", State), ("p", Parallel), ("s2", State)], transformation=state_parallel_state)

    gr.append_rule(input=[("s1", State), ("s", Sequence), ("s2", State)], transformation=state_sequence_state)
    gr.append_rule(input=[("s1", State), ("s", Sequence), ("s2", State)], transformation=state_sequence_state)
    gr.append_rule(input=[("p", Parallel), ("s", Sequence)], transformation=parallel_sequence)

    gr.append_rule(input=[("p", Parallel), ("g", GoTo)], transformation=parallel_goto)
    gr.append_rule(input=[("c", Condition), ("g", GoTo)], transformation=condition_goto)
    gr.append_rule(input=[("s", State), ("g", GoTo)], transformation=state_goto)

    gr.append_rule(input=[("cnd", Condition), ("c", Command)], transformation=condition_command)
    gr.append_rule(input=[("cnd", Condition), ("s", State)], transformation=condition_state)
    gr.append_rule(input=[("c", Command)], transformation=command)

    gr.append_rule(input=[("u1", UnrecognisedComponent), ("u2", UnrecognisedComponent)],
                   transformation=define_two_unrecognised)
    gr.append_rule(input=[("c", UnrecognisedComponent)], transformation=command)

    new_states_list = gr.process(components_list)

    return new_states_list


def remove_orphans(states_list):
    new_list = []

    # Remove orphan controls, then go through once again
    orphans = 0
    for item in states_list:
        if not (isinstance(item, Parallel) or isinstance(item, Sequence)):
            new_list.append(item)
        else:
            orphans += 1

    # If there are orphans - go through the grammar again
    if orphans > 0:
        return grammar_transform(new_list)
    else:
        return new_list


def arrange_identifiers(states_list):
    for i in range(0, len(states_list) - 1):
        if isinstance(states_list[i], State) and isinstance(states_list[i + 1], State) and states_list[i].next_ID == -1:
            states_list[i].next_ID = states_list[i + 1].ID



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
