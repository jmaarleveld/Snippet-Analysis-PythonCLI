"""Utility functions for converting parsed JSON data to
a form which is easier to work with.

Main feature: Rascal exports maps as an array of [key, value]
                pairs when keys are not string. This module
                allows conversion to dictionary.
"""

import abc
import json


class Node(abc.ABC):

    @abc.abstractmethod
    def from_rascal(self, obj):
        pass


class List(Node):

    def __init__(self, items: Node):
        self.__items = items

    def from_rascal(self, obj):
        return [self.__items.from_rascal(x) for x in obj]


class Object(Node):

    def __init__(self, *, allow_empty=False, **fields):
        self.__fields = fields
        self.__allow_empty = allow_empty

    def from_rascal(self, obj):
        if self.__allow_empty and not obj:
            return obj
        if isinstance(obj, dict):
            return {x: y.from_rascal(obj[x]) for (x, y) in self.__fields.items()}
        return {k: y.from_rascal(v)
                for (x, y), (k, v) in zip(self.__fields.items(), obj)}


class Dict(Node):

    def __init__(self, key_type, value_type):
        self.__key = key_type
        self.__value = value_type

    def from_rascal(self, obj):
        if isinstance(obj, dict):
            return {self.__key.from_rascal(k): self.__value.from_rascal(v)
                    for k, v in obj.items()}
        return {self.__key.from_rascal(k): self.__value.from_rascal(v)
                for k, v in obj}


class Tuple(Node):

    def __init__(self, *fields):
        self.__fields = fields

    def from_rascal(self, obj):
        return tuple(typ.from_rascal(x) for typ, x in zip(self.__fields, obj))


class String(Node):
    def from_rascal(self, obj):
        return obj


class Number(Node):
    def from_rascal(self, obj):
        return obj


class Bool(Node):
    def from_rascal(self, obj):
        return obj


def read_json(file, structure: Node):
    """Parse the content of the given file and makes sure
    it adheres to the specified structure.
    """
    return structure.from_rascal(json.load(file))


