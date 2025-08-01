#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# @Time    : 2025/07/28 16:28
# @Author  : Wu_RH
# @FileName: 3O.py
"""
[3O]横纵: 雷从四个方向中的任意一个连到题板外
"""
from abs.Lrule import AbstractMinesRule
from abs.board import AbstractBoard
from utils.solver import get_model


class Rule3O(AbstractMinesRule):
    name = ["3O", "横纵"]
    doc = "雷从四个方向中的任意一个连到题板外"
    subrules = [[True, "[3O]"]]

    @classmethod
    def method_choose(cls) -> int:
        return 1

    def create_constraints(self, board: 'AbstractBoard'):
        if not self.subrules[0][0]:
            return
        model = get_model()
        for pos, var in board(mode="variable"):
            row = board.get_row_pos(pos)
            col = board.get_col_pos(pos)
            row_a = row[:row.index(pos)]
            row_b = row[row.index(pos)+1:]
            col_a = col[:col.index(pos)]
            col_b = col[col.index(pos)+1:]
            print(row_a, row_b, col_a, col_b)
            vars_row_a = board.batch(row_a, "variable")
            vars_row_b = board.batch(row_b, "variable")
            vars_col_a = board.batch(col_a, "variable")
            vars_col_b = board.batch(col_b, "variable")
            r_a = model.NewBoolVar("r_a")
            r_b = model.NewBoolVar("r_b")
            c_a = model.NewBoolVar("c_a")
            c_b = model.NewBoolVar("c_b")
            model.Add(sum(vars_row_a) == len(vars_row_a)).OnlyEnforceIf(r_a)
            model.Add(sum(vars_row_b) == len(vars_row_b)).OnlyEnforceIf(r_b)
            model.Add(sum(vars_col_a) == len(vars_col_a)).OnlyEnforceIf(c_a)
            model.Add(sum(vars_col_b) == len(vars_col_b)).OnlyEnforceIf(c_b)
            model.AddBoolOr([r_a, r_b, c_a, c_b]).OnlyEnforceIf(var)
