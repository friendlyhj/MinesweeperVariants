#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# @Time    : 2025/08/20 14:12
# @Author  : Wu_RH
# @FileName: 2#.py
"""
[2#]: 包含以下规则:[V][2X][2D][2P][2M][2A]
"""
from typing import List, Tuple, Optional

from minesweepervariants.abs.board import AbstractBoard
from minesweepervariants.abs.rule import AbstractRule
from minesweepervariants.impl.summon.solver import Switch
from ..sharp import RuleSharp
from minesweepervariants.abs.Rrule import AbstractClueRule
from minesweepervariants.impl.impl_obj import get_rule


class Rule2sharp(AbstractClueRule):
    name = ["2#", "标签", "sharp"]

    def __init__(self, board: "AbstractBoard" = None, data=None) -> None:
        super().__init__(board, data)
        rule_list = [get_rule(name)(board=board, data=None)
                     for name in ["V", "2X", "2D", "2P", "2M", "2A"]]
        self.shape_rule = RuleSharp(board=board, data=rule_list)

    def fill(self, board: 'AbstractBoard') -> 'AbstractBoard':
        return self.shape_rule.fill(board=board)

    def init_board(self, board: 'AbstractBoard'):
        return self.shape_rule.init_board(board=board)

    def init_clear(self, board: 'AbstractBoard'):
        return self.shape_rule.init_clear(board=board)

    def combine(self, rules: List[Tuple['AbstractRule', Optional[str]]]):
        return self.shape_rule.combine(rules=rules)

    def create_constraints(self, board: 'AbstractBoard', switch: 'Switch'):
        return self.shape_rule.create_constraints(board=board, switch=switch)

    def suggest_total(self, info: dict):
        return self.shape_rule.suggest_total(info=info)


