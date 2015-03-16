from translator.executables.nlp.components.component import *
from translator.executables.nlp.components.execution import *
from translator.executables.nlp.components.robot_commands import command
from translator.executables.nlp.step import step, cstep

__author__ = 'NBUCHINA'

gone_through = False
step_counter = 1
step_modifier = 1


def go_through(components):
    global step_counter
    global step_modifier
    global gone_through

    new_list = []
    gone_through = True

    i = -1
    while i < len(components) - 1:
        i += 1

        ####3-tuple####
        if i < len(components) - 2:
            if isinstance(components[i], component) & isinstance(components[i + 1], parallel) & isinstance(
                    components[i + 2], component):
                new_step = step()
                new_step.text_index_start = components[i].text_index_start
                new_step.component_name = components[i].component_name
                new_step.description = components[i].description + " " + components[i + 2].description
                new_step.state_ID = step_counter
                new_step.commands.append(components[i])

                step_counter += step_modifier
                new_list.append(new_step)

                gone_through = False
                i += 2
                continue

            elif isinstance(components[i], step) & isinstance(components[i + 1], parallel) & isinstance(
                    components[i + 2], component):
                new_step = step()
                new_step.text_index_start = components[i].text_index_start
                new_step.component_name = components[i].component_name
                new_step.description = components[i].description + " " + components[i + 2].description
                new_step.state_ID = step_counter
                new_step.commands.append(components[i])

                step_counter += step_modifier
                new_list.append(new_step)

                gone_through = False
                i += 2
                continue

            elif isinstance(components[i], step) & isinstance(components[i + 1], parallel) & isinstance(
                    components[i + 2], step):
                new_step = step()
                new_step.text_index_start = components[i].text_index_start
                new_step.component_name = components[i].component_name
                new_step.description = components[i].description + " " + components[i + 2].description
                new_step.state_ID = components[i].state_ID
                new_step.commands.extend(components[i].commands)
                new_step.commands.extend(components[i + 2].commands)

                step_counter += step_modifier
                new_list.append(new_step)

                gone_through = False
                i += 2
                continue

        ####2-tuple####
        if i < len(components) - 1:

            if isinstance(components[i], parallel) & isinstance(components[i + 1], sequence):
                new_list.append(components[i + 1])

                gone_through = False
                i += 1
                continue

            elif isinstance(components[i], unrecognised_component) & isinstance(components[i + 1],
                                                                                unrecognised_component):
                unrec1 = components[i]
                unrec2 = components[i + 1]
                new_list.append(
                    unrecognised_component(unrec1.description + " " + unrec2.description, unrec1.text_index_start))

                gone_through = False
                i += 1
                continue

            elif isinstance(components[i], condition) & isinstance(components[i + 1], component):
                cond = components[i]
                action = components[i + 1]

                new_step = cstep()
                new_step.text_index_start = cond.text_index_start
                new_step.component_name = cond.component_name
                new_step.description = cond.description + " " + action.description
                new_step.state_ID = step_counter
                new_step.commands.append(action)
                new_step.condition.append(cond)

                step_counter += step_modifier
                new_list.append(new_step)

                gone_through = False
                i += 1
                continue

            elif isinstance(components[i], condition) & isinstance(components[i + 1], step):
                cond = components[i]
                action = components[i + 1]

                new_step = cstep()
                new_step.text_index_start = cond.text_index_start
                new_step.component_name = cond.component_name
                new_step.description = cond.description + " " + action.description
                new_step.state_ID = step.state_ID
                new_step.commands.extend(action.commands)
                new_step.condition.append(cond)

                step_counter += step_modifier
                new_list.append(new_step)

                gone_through = False
                i += 1
                continue


        if isinstance(components[i], command):
            new_step = step()
            new_step.text_index_start = components[i].text_index_start
            new_step.component_name = components[i].component_name
            new_step.description = components[i].description
            new_step.state_ID = step_counter
            new_step.commands.append(components[i])

            step_counter += step_modifier
            new_list.append(new_step)

            gone_through = False
            continue

        new_list.append(components[i])

    if gone_through:
        return new_list
    else:
        return go_through(new_list)