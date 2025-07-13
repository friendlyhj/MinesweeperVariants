#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Time    : 2025/06/07 13:45
# @Author  : Wu_RH
# @FileName: impl_obj.py

import os
import sys
import importlib.util
from pathlib import Path

from utils.impl_obj import VALUE_QUESS, MINES_TAG

from abs.rule import AbstractValue, AbstractRule
from abs.board import AbstractBoard
from abs.Lrule import AbstractMinesRule
from abs.Mrule import AbstractMinesClueRule, AbstractMinesValue
from abs.Rrule import AbstractClueRule, AbstractClueValue

from impl.board import version1, version2
from impl import rule

TOTAL = -1
board = [version2, version1]


class ModelGenerateError(Exception):
    """模型求解器错误"""


def recursive_import(module):
    base_path = Path(module.__file__).parent
    base_name = module.__name__

    for dirpath, _, filenames in os.walk(base_path):
        for f in filenames:
            if f.endswith('.py') and f != '__init__.py':
                full_path = Path(dirpath) / f
                rel = full_path.relative_to(base_path).with_suffix('')
                mod_name = base_name + '.' + '.'.join(rel.parts)
                if mod_name in sys.modules:
                    continue
                spec = importlib.util.spec_from_file_location(str(mod_name), str(full_path))
                if not spec or not spec.loader:
                    continue
                mod = importlib.util.module_from_spec(spec)
                sys.modules[mod_name] = mod
                spec.loader.exec_module(mod)


def set_total(total: int):
    global TOTAL
    TOTAL = total


def get_all_subclasses(cls):
    subclasses = set()
    direct_subs = cls.__subclasses__()
    subclasses.update(direct_subs)
    for sub in direct_subs:
        subclasses.update(get_all_subclasses(sub))
    return subclasses


def get_board(name=None) -> type | None:
    if name is None:
        v = -1
        b = None
        for i in AbstractBoard.__subclasses__():
            if v < i.version:
                v = i.version
                b = i
        return b
    else:
        for i in AbstractBoard.__subclasses__():
            if i.name == name:
                return i


def get_rule(name: str) -> type | None:
    for i in get_all_subclasses(AbstractRule):
        if i in [
            AbstractClueRule,
            AbstractMinesClueRule,
            AbstractMinesRule
        ]:
            continue
        if i.name == name:
            return i
    raise ValueError(f"未找到规则[{name}]")


def get_value(pos, code):
    code = code.split(b"|", 1)
    if code[0] == b"?":
        return VALUE_QUESS
    if code[0] == b"F":
        return MINES_TAG
    for i in get_all_subclasses(AbstractValue):
        if i in [
            AbstractValue,
            AbstractClueValue,
            AbstractMinesValue
        ]:
            continue
        if i.type() == code[0]:
            return i(pos=pos, code=code[1])
    return None


for pkg in [rule] + board:
    recursive_import(pkg)
