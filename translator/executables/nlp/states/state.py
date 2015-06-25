__author__ = 'NBUCHINA'


class State(object):
    tivipe_component_name = ""
    commands = []

    description = ""
    text_index_start = 0

    ID = -1
    next_ID = -1

    def __init__(self):
        self.component_name = ""
        self.commands = []

        self.description = ""
        self.text_index_start = 0

        self.ID = -1
        self.next_ID = -1


class ConditionState(State):
    def __init__(self):
        super().__init__()
        self.condition = []
        self.uID = -1


class SelectByKeyState(State):
    keys = []
    states = []
    tivipe_component_name = "CommandStateSelectByKey"

    def __init__(self):
        self.keys = []
        self.states = []

    def add_cstep(self, new_cstep):
        key = new_cstep.condition[0].params["button"]
        commands = new_cstep.commands
        state = new_cstep.next_ID

        new_commands_step = None

        if len(commands) > 0:
            new_commands_step = State()
            new_commands_step.commands = commands
            new_commands_step.tivipe_component_name = "CommandState2"
            new_commands_step_id = float((self.states[-1] + 1) / 1000) if len(self.states) > 0 else float(
                new_cstep.ID) + 0.001
            new_commands_step.ID = "%.3f" % new_commands_step_id
            new_commands_step.description = ". ".join([x.description for x in commands])
            if float(state) > 0:
                new_commands_step.next_ID = state
            state = new_commands_step_id

        self.keys.append(key)
        self.states.append(int(str(state).replace(".", "")))
        self.reconstruct_description()

        return new_commands_step

    def reconstruct_description(self):
        if len(self.keys) == 1:
            self.description = "Key selection. press " + self.keys[0]
        else:
            self.description = "Key selection. press " + ','.join(self.keys[:-1]) + " or " + self.keys[-1]
        self.commands = ["[][%s][%s]" % (",".join(self.keys), ",".join([str(x) for x in self.states]))]