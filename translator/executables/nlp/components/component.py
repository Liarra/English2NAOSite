class component(object):
    tags = []
    regexp = ""

    tivipe_component_name = ""
    name = ""
    description = ""
    summary = ""
    text_index_start = 0
    command = ""
    params = {}

    def __init__(self, **params):
        if self.params is None:
            self.params = {}

        if params is not None:
            for key, value in params.items():
                self.params[key] = value

    @classmethod
    def from_string(cls, string, index_in_text=0):
        string = string.strip()
        string = string.lower()

        ret = cls()
        ret.description = string
        ret.text_index_start = index_in_text

        return ret

    def __repr__(self):
        return self.command.format(**self.params)

    def parse_from_string(self, string):
        pass


class condition(component):
    pass


class button_press(condition):
    name = "Keyboard button press"
    tags = ["press", "button"]
    regexp = r"(press|type) ['\"]?(?P<button>.)['\"]?\W?$"

    params = {"button": ''}
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


class unrecognised_component(component):
    params = {"unrecognised_text": ''}
    tags = []
    regexp = ""
    command = "_UNRECOGNISED_[{unrecognised_text}]"

    @classmethod
    def from_string(cls, string, index_in_text=0):
        ret = super().from_string(string, index_in_text)
        ret.params["unrecognised_text"] = string
        return ret