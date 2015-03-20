__author__ = 'NBUCHINA'


def getCSVFromSteps(steps):
    import csv

    with open('result.csv', 'w', newline='') as csvfile:
        step_writer = csv.writer(csvfile, delimiter=',',
                                 quotechar='"', quoting=csv.QUOTE_MINIMAL)
        step_writer.writerow(['Component name', 'Dunno', 'Description', 'State ID', 'Command', 'Next ID'])
        for step in steps:
            step_commands = ("|").join([str(x) for x in step.commands])
            step_writer.writerow(
                [step.component_name, '1', step.description, int(float(step.state_ID)*100), step_commands, int(float(step.next_state_ID)*100)])
