#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# @Time    : 2025/07/28 03:49
# @Author  : Wu_RH
# @FileName: 3T.py
"""
[3T]无三连:任意三个雷不能等距排布
"""

from abs.Lrule import AbstractMinesRule
from abs.board import AbstractBoard
from utils.solver import get_model


class Rule1T(AbstractMinesRule):
    name = "3T"
    subrules = [
        [True, "[3T]雷等距无三连"]
    ]

    def create_constraints(self, board: 'AbstractBoard'):
        if not self.subrules[0][0]:
            return
        model = get_model()

        for key in board.get_interactive_keys():
            pos_bound = board.boundary(key=key)
            max_num = max(pos_bound.x, pos_bound.y) + 1
            for pos, _ in board():
                positions = []
                for i in range(1, max_num // 2):
                    positions.extend([
                        [pos, pos.left(i), pos.left(2*i)],
                        [pos, pos.down(i), pos.down(2*i)],
                        [pos, pos.left(i).down(i), pos.left(2*i).down(2*i)],
                        [pos, pos.left(i).up(i), pos.left(2*i).up(2*i)]
                    ])
                for position in positions:
                    var_list = board.batch(position, mode="variable")
                    if True in [i is None for i in var_list]:
                        continue
                    model.Add(sum(var_list) != 3)

    def check(self, board: 'AbstractBoard') -> bool:
        pass

    @classmethod
    def method_choose(cls) -> int:
        return 1
