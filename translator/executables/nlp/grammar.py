from translator.executables.nlp.components.component import *
from translator.executables.nlp.components.execution import *
from translator.executables.nlp.components.robot_commands import command
from translator.executables.nlp.substep import SubStep, ConditionSubStep, SelectByKeyState

__author__ = 'NBUCHINA'

gone_through = False
step_counter = 1
step_modifier = 0.01
unrecognised_enabled = True


def go_through(components):
    global step_counter
    global step_modifier
    global gone_through
    global unrecognised_enabled
    # unrecognised_enabled = False

    new_list = []
    gone_through = True

    i = -1
    while i < len(components) - 1:
        i += 1

        # Remove unrecognised if not allowed
        if (not unrecognised_enabled) and isinstance(components[i], unrecognised_component):
            gone_through = False
            new_list.extend(components[i + 1:])
            break

        ####### Grammar rules start here ############
        # 3-tuple #
        if i < len(components) - 2:

            if isinstance(components[i], command) \
                    and isinstance(components[i + 1], parallel) \
                    and isinstance(components[i + 2], command):
                new_step = SubStep()
                new_step.text_index_start = components[i].text_index_start
                new_step.tivipe_component_name = components[i].tivipe_component_name
                new_step.description = components[i].description + " " + components[i + 2].description
                new_step.ID = "%.2f" % step_counter
                new_step.commands.append(components[i])
                new_step.commands.append(components[i + 2])

                step_counter += step_modifier
                new_list.append(new_step)

                gone_through = False
                new_list.extend(components[i + 3:])
                break

            elif isinstance(components[i], SubStep) \
                    and isinstance(components[i + 1], parallel) \
                    and isinstance(components[i + 2], command):
                new_step = components[i]
                new_step.description = components[i].description + " " + components[i + 2].description
                new_step.commands.append(components[i])

                new_list.append(new_step)

                gone_through = False
                new_list.extend(components[i + 3:])
                break

            elif isinstance(components[i], command) \
                    and isinstance(components[i + 1], parallel) \
                    and isinstance(components[i + 2], SubStep):
                new_step = components[i + 2]
                new_step.text_index_start = components[i].text_index_start
                new_step.tivipe_component_name = components[i].tivipe_component_name
                new_step.description = components[i].description + " " + components[i + 2].description
                new_step.commands.append(components[i])

                new_list.append(new_step)

                gone_through = False
                new_list.extend(components[i + 3:])
                break

            elif isinstance(components[i], SubStep) \
                    and isinstance(components[i + 1], parallel) \
                    and isinstance(components[i + 2], SubStep):
                new_step = SubStep()
                new_step.text_index_start = components[i].text_index_start
                new_step.tivipe_component_name = components[i].tivipe_component_name
                new_step.description = components[i].description + " " + components[i + 2].description
                new_step.ID = components[i].ID
                new_step.commands.extend(components[i].commands)
                new_step.commands.extend(components[i + 2].commands)

                new_list.append(new_step)

                gone_through = False
                new_list.extend(components[i + 3:])
                break

            elif isinstance(components[i], SubStep) \
                    and isinstance(components[i + 1], sequence) \
                    and isinstance(components[i + 2], SubStep):
                step1 = components[i]
                step2 = components[i + 2]

                step1.next_ID = step2.ID

                new_list.append(step1)
                new_list.append(step2)

                gone_through = False
                new_list.extend(components[i + 3:])
                break

        # 2-tuple #
        if i < len(components) - 1:

            if isinstance(components[i], parallel) and isinstance(components[i + 1], sequence):
                new_list.append(components[i + 1])

                gone_through = False
                new_list.extend(components[i + 2:])
                break

            elif (isinstance(components[i], parallel) or isinstance(components[i], sequence)) \
                    and isinstance(components[i + 1], goto):
                new_list.append(components[i + 1])

                gone_through = False
                new_list.extend(components[i + 2:])
                break

            elif isinstance(components[i], unrecognised_component) \
                    and isinstance(components[i + 1], unrecognised_component):
                unrec1 = components[i]
                unrec2 = components[i + 1]
                new_list.append(
                    unrecognised_component.from_string(unrec1.description + " " + unrec2.description, unrec1.text_index_start))

                gone_through = False
                new_list.extend(components[i + 2:])
                break

            elif isinstance(components[i], condition) and isinstance(components[i + 1], goto):
                new_step = ConditionSubStep()
                new_step.text_index_start = components[i].text_index_start
                new_step.tivipe_component_name = components[i].tivipe_component_name
                new_step.description = components[i].description + " " + components[i + 1].description
                new_step.ID = "%.2f" % step_counter
                new_step.next_ID = "%.2f" % components[i + 1].params["where"]
                new_step.condition.append(components[i])

                step_counter += step_modifier
                new_list.append(new_step)

                gone_through = False
                new_list.extend(components[i + 2:])
                break

            elif isinstance(components[i], SubStep) and isinstance(components[i + 1], goto):
                new_step = components[i]
                goto_pointer = components[i + 1]

                new_step.next_ID = "%.2f" % goto_pointer.params["where"]
                new_list.append(new_step)

                gone_through = False
                new_list.extend(components[i + 2:])
                break

            elif isinstance(components[i], condition) and isinstance(components[i + 1], command):
                cond = components[i]
                action = components[i + 1]

                new_step = ConditionSubStep()
                new_step.text_index_start = cond.text_index_start
                new_step.tivipe_component_name = cond.tivipe_component_name
                new_step.description = cond.description + " " + action.description
                new_step.ID = "%.2f" % step_counter
                new_step.commands.append(action)
                new_step.condition.append(cond)

                step_counter += step_modifier
                new_list.append(new_step)

                gone_through = False
                new_list.extend(components[i + 2:])
                break

            elif isinstance(components[i], condition) and isinstance(components[i + 1], SubStep):
                cond = components[i]
                action = components[i + 1]

                new_step = ConditionSubStep()
                new_step.text_index_start = cond.text_index_start
                new_step.tivipe_component_name = cond.tivipe_component_name
                new_step.description = cond.description + " " + action.description
                new_step.ID = action.ID
                new_step.commands.extend(action.commands)
                new_step.condition.append(cond)

                new_list.append(new_step)

                gone_through = False
                new_list.extend(components[i + 2:])
                break

            elif (isinstance(components[i], SubStep)
                  and isinstance(components[i + 1], SubStep)) \
                    and components[i].next_ID == -1:

                step1 = components[i]
                step2 = components[i + 1]

                step1.next_ID = step2.ID

                new_list.append(step1)
                new_list.append(step2)

                gone_through = False
                new_list.extend(components[i + 2:])
                break

        # 1-tuple #
        if isinstance(components[i], command):
            new_step = SubStep()
            new_step.text_index_start = components[i].text_index_start
            new_step.tivipe_component_name = components[i].tivipe_component_name
            new_step.description = components[i].description
            new_step.ID = "%.2f" % step_counter
            new_step.commands.append(components[i])

            step_counter += step_modifier
            new_list.append(new_step)

            gone_through = False

            new_list.extend(components[i + 1:])
            break

        if isinstance(components[i], unrecognised_component):
            if (i > 0 and not isinstance(components[i - 1], unrecognised_component)) or i == 0:
                new_step = SubStep()
                new_step.text_index_start = components[i].text_index_start
                new_step.tivipe_component_name = components[i].tivipe_component_name
                new_step.description = components[i].description
                new_step.ID = "%.2f" % step_counter
                new_step.commands.append(components[i])

                step_counter += step_modifier
                new_list.append(new_step)

                gone_through = False

                new_list.extend(components[i + 1:])
                break

        new_list.append(components[i])
    ####### Grammar rules end here ############

    if gone_through:
        step_counter = 1

        new_new_list = []

        # Remove orphan controls, then go through once again
        orphans = 0
        for item in new_list:
            if not (isinstance(item, parallel) or isinstance(item, sequence)):
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
def unite_csteps(steps):
    first_step_id = -1

    for step in steps:
        if isinstance(step, ConditionSubStep):
            if first_step_id == -1:
                first_step_id = step.ID

            if step.ID != first_step_id:
                step.ID = first_step_id

    return first_step_id


def get_new_list_with_ksteps(steps):
    first_cstep_id = unite_csteps(steps)
    if first_cstep_id == -1:
        return steps

    select_key = SelectByKeyState()

    new_list = []

    for step in steps:
        if isinstance(step, ConditionSubStep):
            select_key.add_cstep(step)
            select_key.ID = step.ID
        else:
            new_list.append(step)

    new_list.append(select_key)

    return new_list
