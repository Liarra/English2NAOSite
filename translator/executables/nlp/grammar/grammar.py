from collections import OrderedDict

__author__ = 'nina'


class GrammarRule:
    def __init__(self, names, things, transformation):
        self.things = things
        self.names = names
        self.transformation = transformation

    def is_applicable(self, object_list, index):
        rule_length = len(self.things)
        if len(object_list) - index < rule_length:
            return False

        for thing in self.things:
            if not isinstance(object_list[index], thing):
                return False
            index += 1

        return True

    def apply(self, object_list, index):
        new_list = object_list[0:index]
        argument_dict = {}

        for name in self.names:
            argument_dict[name] = object_list[index]
            index += 1

        new_items = self.transformation(**argument_dict)
        new_list.extend(new_items)
        new_list.extend(object_list[index:])

        return new_list


class Grammar:
    def __init__(self):
        self.rules = []

    def append_rule(self, input, transformation=None):
        names_array = []
        things_array = []
        for name, thing in input:
            names_array.append(name)
            things_array.append(thing)

        new_rule = GrammarRule(tuple(names_array), tuple(things_array), transformation)
        self.rules.append(new_rule)

    def process(self, objects_list):
        went_through = False
        working_list = objects_list[:]

        while not went_through:
            i = 0
            while i < len(working_list):
                for rule in self.rules:
                    if rule.is_applicable(working_list, i):
                        went_through = False
                        new_list = rule.apply(working_list, i)
                        working_list = new_list
                        i = -1
                        break
                    went_through = True
                i += 1

        return working_list