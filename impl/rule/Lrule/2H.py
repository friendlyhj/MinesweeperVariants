#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# @Time    : 2025/07/07 17:37
# @Author  : Wu_RH
# @FileName: 2H.py
"""
[2H] 横向 (Horizontal)：所有雷必须存在横向相邻的雷
"""
from abs.Lrule import AbstractMinesRule
from abs.board import AbstractBoard
from utils.solver import get_model


class Rule2H(AbstractMinesRule):
    name = "2H"
    subrules = [
        [True, "[2H]横向"]
    ]

    def create_constraints(self, board: 'AbstractBoard'):
        if not self.subrules[0][0]:
            return
        model = get_model()
        for pos, var in board(mode="variable"):
            if not board.in_bounds(pos.right()):
                model.Add(board.get_variable(pos.left()) == 1).OnlyEnforceIf(var)
            elif not board.in_bounds(pos.left()):
                model.Add(board.get_variable(pos.right()) == 1).OnlyEnforceIf(var)
            else:
                model.AddBoolOr(board.batch([pos.right(), pos.left()], mode="variable")).OnlyEnforceIf(var)

    @classmethod
    def method_choose(cls) -> int:
        return 1
