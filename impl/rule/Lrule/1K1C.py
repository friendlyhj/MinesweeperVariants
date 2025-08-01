#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# @Time    : 2025/07/07 17:13
# @Author  : Wu_RH
# @FileName: 1C.py
"""
[1K1C] 马步八连通 (Knight-Connected)：雷区域马步连通
"""
from abs.Lrule import AbstractMinesRule
from abs.board import AbstractBoard
from utils.impl_obj import get_total
from utils.solver import get_model

from .connect import connect


class Rule1C(AbstractMinesRule):
    name = ["1K1C", "马步八连通", "Knight-Connected"]
    doc = "雷区域马步连通"
    subrules = [
        [True, "[1K1C]马步连通"]
    ]

    def create_constraints(self, board):
        if not self.subrules[0][0]:
            return
        model = get_model()
        connect(
            ub=get_total() // 2 + 1,
            model=model,
            board=board,
            connect_value=1,
            nei_value=(5, 5)
        )

    @classmethod
    def method_choose(cls) -> int:
        return 1
