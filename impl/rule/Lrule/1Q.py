#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# 
# @Time    : 2025/06/10 11:44
# @Author  : xxx
# @FileName: Q1.py

"""
[1Q]无方: 每个2x2区域内都至少有一个雷
"""

from typing import List

from abs.Lrule import AbstractMinesRule
from abs.board import AbstractPosition, AbstractBoard


def block(a_pos: AbstractPosition, board: AbstractBoard) -> List[AbstractPosition]:
    b_pos = a_pos.up()
    c_pos = a_pos.left()
    d_pos = b_pos.left()
    if not board.in_bounds(d_pos):
        return []
    return [a_pos, b_pos, c_pos, d_pos]


class Rule1Q(AbstractMinesRule):
    name = ["1Q", "Q", "无方"]
    doc = "每个2x2区域内都至少有一个雷"

    def create_constraints(self, board: 'AbstractBoard', switch):
        model = board.get_model()
        s = switch.get(model, self)

        for key in board.get_interactive_keys():
            a_pos = board.boundary(key=key)
            for b_pos in board.get_col_pos(a_pos):
                for i_pos in board.get_row_pos(b_pos):
                    if not (pos_block := block(i_pos, board)):
                        continue
                    var_list = [board.get_variable(pos) for pos in pos_block]
                    model.AddBoolOr(var_list).OnlyEnforceIf(s)
