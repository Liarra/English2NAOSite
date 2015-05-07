import csv
from io import StringIO

__author__ = 'NBUCHINA'


def writeCSVFromSteps(steps, csvfile):
    step_writer = csv.writer(csvfile, delimiter=',',
                             quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for step in steps:
        step_commands = "|".join([str(x) for x in step.commands])
        ID = int(float(step.ID) * 100)
        next_ID = "" if float(step.next_ID) < 0 else int(float(step.next_ID) * 100)

        step_writer.writerow(
            [step.tivipe_component_name, '1', step.description, ID, step_commands, next_ID])
        # print(csvfile.getvalue())


def initCSV():
    with StringIO() as csvfile:
        step_writer = csv.writer(csvfile, delimiter=',',
                                 quotechar='"', quoting=csv.QUOTE_MINIMAL)
        step_writer.writerow(['Component name', 'Dunno', 'Description', 'State ID', 'Command', 'Next ID'])
        step_writer.writerow(['-' * 10, '-' * 3, '-' * 10, '-' * 8, '-' * 10, '-' * 5])

    return csvfile