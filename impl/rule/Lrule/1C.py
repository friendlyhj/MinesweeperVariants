#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# @Time    : 2025/07/07 17:13
# @Author  : Wu_RH
# @FileName: 1C.py
"""
[1C] 八连通 (Connected)：雷区域八连通
"""
from abs.Lrule import AbstractMinesRule
from abs.board import AbstractBoard
from utils.impl_obj import get_total

from .connect import connect


class Rule1C(AbstractMinesRule):
    name = ["1C", "C", "八连通", "Connected"]
    doc = "雷区域八连通"

    def create_constraints(self, board, switch):
        model = board.get_model()
        connect(
            ub=get_total() // 2 + 1,
            model=model,
            board=board,
            connect_value=1,
            nei_value=2,
            switch=switch,
            map_index=(self, 0),
        )
