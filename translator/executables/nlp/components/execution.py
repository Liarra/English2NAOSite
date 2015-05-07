from translator.executables.nlp.components.component import component

__author__ = 'NBUCHINA'


class sequence(component):
    tags = ["after", "then", "next"]
    regexp = r"(then|next)$"
    command = " & "

    @classmethod
    def from_string(cls, string, index_in_text=0):
        ret=super().from_string(string, index_in_text)
        return ret


class parallel(component):
    tags = ["same time"]
    regexp = r"^\ ?(and|while)$"
    command = " | "

    @classmethod
    def from_string(cls, string, index_in_text=0):
        ret=super().from_string(string, index_in_text)
        return ret


class goto(component):
    tags = []
    regexp = r"go to ((sub)?(step|state|point)) (?P<number>\d{1,5}\.?\d{0,2})"
    where = float(-1)
    params={"where":-1}
    command = "goto[{where}]"

    @classmethod
    def from_string(cls, string, index_in_text=0):
        ret=super().from_string(string, index_in_text)

        import re

        p = re.compile(cls.regexp, re.IGNORECASE)
        string = string.strip()
        string = string.lower()

        m = p.search(string)
        if (m == None):
            return
        ret.params["where"] = float(m.group('number'))
        return ret

