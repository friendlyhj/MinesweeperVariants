#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# @Time    : 2025/07/07 17:42
# @Author  : Wu_RH
# @FileName: 2C.py
"""
[2C] 连方 (Connected)：(1) 所有四连通雷区域为矩形；(2) 所有雷区域对角相邻
"""
from typing import List

from abs.Lrule import AbstractMinesRule
from abs.board import AbstractBoard, AbstractPosition
from utils.solver import get_model
from .connect import connect


def block(a_pos: AbstractPosition, board: AbstractBoard) -> List[AbstractPosition]:
    b_pos = a_pos.up()
    c_pos = a_pos.left()
    d_pos = b_pos.left()
    if not board.in_bounds(d_pos):
        return []
    return [a_pos, b_pos, c_pos, d_pos]


class Rule2C(AbstractMinesRule):
    name = "2C"
    subrules = [
        [True, "[2C]雷区必须是矩形"],
        [True, "[2C]雷区必须联通"]
    ]

    def create_constraints(self, board: 'AbstractBoard'):
        model = get_model()
        if self.subrules[0][0]:
            for pos, _ in board():
                var_list = board.batch(block(pos, board), mode="variable")
                if not var_list:
                    continue
                model.Add(sum(var_list) != 3)
        if self.subrules[1][0]:
            connect(
                model,
                board
            )

    @classmethod
    def method_choose(cls) -> int:
        return 1