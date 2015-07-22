class Component(object):
    tags = []
    regexp = ""

    tivipe_component_name = ""
    name = ""
    description = ""
    summary = ""
    text_index_start = 0
    command = ""
    default_params = {}

    def __init__(self, **params):
        self.params = self.default_params.copy()

        self.load_params(params)

    def load_params(self, params):
        if params is not None:
            for key, value in params.items():
                # Ignore params that do not belong to the class.
                if key in self.__class__.default_params.keys() or key in self.params:
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


class Condition(Component):
    pass


class UnrecognisedComponent(Component):
    default_params = {"unrecognised_text": ''}
    tags = []
    regexp = r"(?!x)x"  # A regex that never matches
    command = "_UNRECOGNISED_[{unrecognised_text}]"

    @classmethod
    def from_string(cls, string, index_in_text=0):
        ret = super().from_string(string, index_in_text)
        ret.params["unrecognised_text"] = string
        return ret


class IgnoredComponent(UnrecognisedComponent):
    tags = [
        "if", "or",
        "i", "robot",
        "the", "a",
    ]

    default_params = {"ignored_text": ''}

    command = "_IGNORED_[{ignored_text}]"

    @classmethod
    def from_string(cls, string, index_in_text=0):
        ret = super().from_string(string, index_in_text)
        ret.params["ignored_text"] = string
        return ret