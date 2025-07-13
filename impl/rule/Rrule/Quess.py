#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# @Time    : 2025/06/29 05:15
# @Author  : Wu_RH
# @FileName: Quess.py

from abs.Rrule import AbstractClueRule, ValueQuess
from abs.board import AbstractBoard
from utils.impl_obj import VALUE_QUESS


class RuleQuess(AbstractClueRule):
    name = "?"

    def fill(self, board: 'AbstractBoard') -> 'AbstractBoard':
        for pos, _ in board("N"):
            board.set_value(pos, VALUE_QUESS)
        return board

    def clue_class(self):
        return ValueQuess


