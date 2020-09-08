

import sys
from os import path, mkdir, makedirs
import warnings
warnings.simplefilter("always")
from functools import reduce
from glob import glob
try:
    from collections.abc import Sequence
except:
    # python2 version
    from collections import Sequence


def split(flatpath, count=9999999):
    parts = []
    while flatpath:
        flatpath, child = path.split(flatpath)
        parts.insert(0, child)
    return parts


def naturaljoin(sequence, sep=", ", last_sep=' or ', repr=str):
    result = sep.join(repr(item) for item in sequence[:-1])
    if sequence[-1:]:
        result += last_sep + repr(sequence[-1])
    return result


class PathTree(list):

    MODE_STRICT = "strict"
    MODE_WARN = "warning"
    MODE_CREATE = "create"
    MODE_IGNORE = "test-only"

    _parent = None

    @property
    def parent(self):
        return self._parent
    
    _children = None

    @property
    def children(self):
        return self._children.values()

    _mode = None
    
    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, mode):
        if mode not in PATHTREE_MODES:
            raise ValueError("mode must be {:}"
                             .format(naturaljoin(PATHTREE_MODES, repr=repr)))
        self._mode = mode

    def __init__(self, *flatpath_list, parent=None, mode=None):
        self._parent = parent
        self._children = {}
        self.mode = __class__.MODE_IGNORE if mode is None else mode
        self.extend(flatpath_list)

    def __delitem__(self, key):
        raise TypeError("'PathTree' object doesn't support item deletion")

    def __getitem__(self, key):
        current = self
        for k in self.__key__(key):
            if type(k) is str:
                if k == '.':
                    current = self
                elif k == '..':
                    current = self._parent
                else:
                    current = self._children[k]
            else:
                current = super().__getitem__(k)
        return current

    def __index__(self, index):
        if isinstance(index, str):
            try:
                return self.index(index)
            except ValueError as ve:
                raise KeyError(repr(index))
        elif index is None:
            return len(self)
        return index

    def __key__(self, key):
        if not isinstance(key, tuple):
            key = (key,)
        return tuple('.' if k is None else k for k in key)

    def __setitem__(self, key, child):
        raise TypeError("'PathTree' object does not support item assignment")

    def extend(self, flatpath_list):
        for flatpath in flatpath_list:
            self.append(flatpath)

    def insert(self, index, flatpath):
        cls, mode = self.__class__, self._mode
        folder = []
        current = folder
        upper = split(flatpath)
        lower = upper.pop(0)
        if not lower:
            raise KeyError(repr(lower))
        if not path.exists(flatpath) and mode != cls.MODE_IGNORE:
            message = "{:} doesn't exist".format(flatpath)
            if mode == cls.MODE_WARN:
                warnings.warn("Warning, " + message)
            elif mode ==  cls.MODE_WARN:
                raise ValueError(message)
        if lower not in self:
            super().insert(self.__index__(index), lower)
        if upper:
            child = path.sep.join(upper)
            if path.isfile(flatpath):
                raise ValueError("Warning, {:} of {:} is not a directory"
                      .format(child, lower))
            self._children[lower] = PathTree(child, parent=self)

    def append(self, flatpath):
        return self.insert(None, flatpath)


PATHTREE_MODES = tuple(getattr(PathTree, name) for name in dir(PathTree)
                       if name.startswith("MODE_"))


