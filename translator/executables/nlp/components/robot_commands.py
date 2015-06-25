from translator.executables.nlp.components.component import Component, Condition


class Command(Component):
    pass


class say_command(Command):
    tags = ["say", "tell", "ask"]
    regexp = r"(say|tell|ask)(s|ing)? ['\"“](?P<what>.+)['\"”]"
    default_params = {"text": ''}
    command = "[say({text})]"
    tivipe_component_name = "CommandState2"
    name = "Say something"
    summary = "This command makes the robot say the specified text."

    @classmethod
    def from_string(cls, string, index_in_text=0):
        ret = super().from_string(string, index_in_text)

        import re

        p = re.compile(cls.regexp, re.IGNORECASE)
        string = string.strip()
        string = string.lower()

        m = p.search(string)
        if m is None:
            return
        say_what = m.group('what').replace(' ', '_')
        ret.params["text"] = say_what
        return ret


class wait_command(Command):
    tags = ["wait"]
    regexp = r"waits?.* (?P<number>\d{1,3}) (?P<units>second|minute|ms|sec|min|millisecond)s?"
    tivipe_component_name = "CommandState2"
    command = "wait({ms})"
    default_params = {"ms": 0}
    name = "Wait"

    @classmethod
    def from_string(cls, string, index_in_text=0):
        ret = super().from_string(string, index_in_text)

        import re

        p = re.compile(cls.regexp, re.IGNORECASE)
        string = string.strip()
        string = string.lower()

        m = p.search(string)
        if m is None:
            return
        number = m.group('number')
        units = m.group('units')

        if units in ["second", "sec"]:
            number_ms = int(number) * 1000
        elif units in ["minute", "min"]:
            number_ms = int(number) * 60000
        # Assuming it's in milliseconds
        else:
            number_ms = int(number)

        ret.params["ms"] = number_ms
        return ret


"""
This command is a bit different from others. Here, text is checked not against class, but against the instance.
"""
class move_command(Command):
    tags = []
    regexp = r"(?!x)x"  # A regex that never matches
    command = "[[stiff (1, 500, 0)] & [posture({base_pose})] & [{move}] & [posture({base_pose})] & [stiff (0, 500, 0)]]"
    default_params = {"name": "", "move": '', "base_pose": 'Crouch'}

    def from_string(self, string, index_in_text=0):
        ret = super().from_string(string, index_in_text)
        ret.tivipe_component_name = "CommandState2"

        ret.params = self.params
        ret.regexp = self.regexp
        ret.command = self.command
        ret.tags = self.tags

        return ret


class button_press(Condition):
    name = "Keyboard button press"
    tags = ["press", "button"]
    regexp = r"(press|type) ['\"]?(?P<button>.)['\"]?\W?$"

    default_params = {"button": ''}
    command = "key[{button}]->"
    tivipe_component_name = "CommandStateSelectByKey"

    @classmethod
    def from_string(cls, string, index_in_text=0):
        ret = super().from_string(string, index_in_text)

        import re

        p = re.compile(ret.regexp, re.IGNORECASE)
        string = string.strip()
        string = string.lower()
        m = p.search(string)
        if m is None:
            return
        button = m.group('button')
        ret.params["button"] = button
        return ret