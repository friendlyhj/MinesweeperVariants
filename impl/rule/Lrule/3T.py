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
    name = ["3T", "无三联"]
    doc = "任意三个雷不能等距排布"
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
                for i in range(max_num // 2):
                    for j in range(max_num // 2):
                        if i == 0 and j == 0:
                            continue
                        positions.append([
                            pos, pos.shift(i, j),
                            pos.shift(2*i, 2*j)
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
