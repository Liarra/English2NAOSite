from translator.executables.nlp.components.component import component


class command(component):
    pass


class say_command(command):
    tags = ["say", "tell", "ask"]
    regexp = r"(say|tell|ask)(s|ing)? ['\"“](?P<what>.+)['\"”]"

    command = "say({text})"

    @classmethod
    def from_string(cls, string, index_in_text=0):
        ret = super().from_string(string, index_in_text)
        ret.tivipe_component_name = "CommandState2"

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


class wait_command(command):
    tags = ["wait"]
    regexp = r"waits?.* (?P<number>\d{1,3}) (?P<units>second|minute|ms|sec|min|millisecond)s?"

    ms = 0

    def __init__(self, string, index_in_text=0):
        super().__init__(string, index_in_text)
        self.tivipe_component_name = "CommandState2"

        import re

        p = re.compile(self.regexp, re.IGNORECASE)
        string = string.strip()
        string = string.lower()

        m = p.search(string)
        if (m == None):
            return
        number = m.group('number')
        units = m.group('units')

        number_ms = 0
        if units in ["second", "sec"]:
            number_ms = int(number) * 1000
        elif units in ["minute", "min"]:
            number_ms = int(number) * 60000
        # Assuming it's in milliseconds
        else:
            number_ms = int(number)

        self.ms = number_ms
        self.command = "wait(%d)" % self.ms


from os import listdir
from os.path import isfile, join, splitext
import xml.etree.ElementTree as ET


class move_command(command):
    tags = []
    regexp = r"(?!x)x"  # A regex that never matches
    params={"move":''}
    command = "stiff (1, 500, 0) & {move} & stiff (0, 500, 0)"

    @classmethod
    def from_string(cls, string, index_in_text=0):
        ret = super().from_string(string, index_in_text)
        ret.tivipe_component_name = "CommandState2"

        max = 0
        for move_file in move_command.files_to_tags:
            s = 0
            move_tags = move_command.files_to_tags[move_file]
            for tag in move_tags:
                if tag in ret.description:
                    s += 1

            if s > max:
                max = s
                ret.params["move"] = move_command.files_to_moves[move_file].replace('\n', '').replace('\r', '')
        return ret


moves_folder = "moves"

import os

dir = os.path.dirname(__file__)
moves_folder = os.path.join(dir, moves_folder)

move_files = [f for f in listdir(moves_folder) if isfile(join(moves_folder, f))]

move_tags = {}
move_codes = {}
for m in move_files:
    file = join(moves_folder, m)

    tree = ET.parse(file)
    tags = [tag.text for tag in tree.findall('tag')]
    move = tree.find('move').text

    move_tags[splitext(m)] = tags
    move_codes[splitext(m)] = move

    move_command.tags.extend(tags)

# move_command.tags = move_regex.keys()
move_command.files_to_tags = move_tags
move_command.files_to_moves = move_codes