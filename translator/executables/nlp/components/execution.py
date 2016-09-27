from translator.executables.nlp.components.component import Component

__author__ = 'NBUCHINA'


class Sequence(Component):
    tags = {"after", "then", "next"}
    command = " & "

    @classmethod
    def from_string(cls, string, index_in_text=0):
        ret = super().from_string(string, index_in_text)
        return ret


class Parallel(Component):
    tags = {"same time", "and", "while"}
    command = " | "

    @classmethod
    def from_string(cls, string, index_in_text=0):
        ret = super().from_string(string, index_in_text)
        return ret


class GoTo(Component):
    tags = {}
    regexp = r"go to ((sub)?(step|state|point|line)) (?P<number>\d{1,5}\.?\d{0,2})"
    where = float(-1)
    default_params = {"where": -1}
    command = "goto[{where}]"

    @classmethod
    def from_string(cls, string, index_in_text=0):
        ret = super().from_string(string, index_in_text)

        import re

        p = re.compile(cls.regexp, re.IGNORECASE)
        string = string.strip()
        string = string.lower()

        m = p.search(string)
        if m == None:
            return

        number = m.group('number')
        if len(number) < 3:
            number = int(number) * 100

        ret.params["where"] = int(number)
        return ret
