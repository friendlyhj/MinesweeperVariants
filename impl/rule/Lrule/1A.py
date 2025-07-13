#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# @Time    : 2025/07/07 17:13
# @Author  : Wu_RH
# @FileName: 1A.py
"""
[1A] 无马步 (Anti-Knight)：所有雷的马步位置不能有雷
"""

from abs.Lrule import AbstractMinesRule
from abs.board import AbstractBoard
from utils.solver import get_model


class Rule1A(AbstractMinesRule):
    name = "1A"
    subrules = [
        [True, "[1A]无马步"]
    ]

    def create_constraints(self, board: 'AbstractBoard'):
        if not self.subrules[0][0]:
            return
        model = get_model()
        for pos, var in board(mode="variable"):
            pos_list = [
                pos.left(2).up(1),
                pos.left(2).down(1),
                pos.down(2).left(1),
                pos.down(2).right(1)
            ]
            var_list = board.batch(pos_list, mode="variable", drop_none=True)
            for _var in var_list:
                model.AddBoolOr([_var.Not(), var.Not()])

    @classmethod
    def method_choose(cls) -> int:
        return 1