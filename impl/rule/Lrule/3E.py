#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# @Time    : 2025/06/11 21:51
# @Author  : Wu_RH
# @FileName: 3E.py

"""
[3E]演化: 每个3x1区域决定其中间下方1格是否为雷，演化被当前题板所有区域共享。
"""

NAME_3E = ["3E_x", "3E_y"]

from abs.Lrule import AbstractMinesRule
from abs.board import AbstractBoard
from utils.impl_obj import VALUE_QUESS, MINES_TAG
from utils.solver import get_model
from utils.tool import get_random


class Rule3E(AbstractMinesRule):
    name = ["3E", "迭代", "演化"]
    doc = "每个3x1区域决定其中间下方1格是否为雷，演化被当前题板所有区域共享。"
    subrules = [[True, "[3E]"]]

    def __init__(self, board: AbstractBoard, data=None):
        super().__init__(board, data)
        board.generate_board(NAME_3E[0], size=(8, 3))
        board.generate_board(NAME_3E[1], size=(8, 1))
        board.set_config(NAME_3E[1], "VALUE", VALUE_QUESS)
        board.set_config(NAME_3E[1], "MINES", MINES_TAG)

    def create_constraints(self, board: 'AbstractBoard'):
        if not self.subrules[0][0]:
            return
        model = get_model()

        for index, pos in enumerate(board.get_col_pos(
                board.get_pos(0, 0, NAME_3E[0]))):
            pos1, pos2, pos3 = board.get_row_pos(pos)
            board.set_value(pos1, MINES_TAG if index & 4 else VALUE_QUESS)
            board.set_value(pos2, MINES_TAG if index & 2 else VALUE_QUESS)
            board.set_value(pos3, MINES_TAG if index & 1 else VALUE_QUESS)

        vals_list = []

        for i in range(8):
            x = model.NewIntVar(i, i, f"[3E]{i}_x")
            y = board.get_variable(board.get_pos(i, 0, NAME_3E[1]))
            model.Add(x == i)
            vals_list.append([x, y])

        for key in board.get_interactive_keys():
            col = board.get_col_pos(board.boundary(key=key))
            bool_var_index = 0
            for pos in col:
                row = board.get_row_pos(pos)
                for index in range(len(row) - 2):
                    variables = board.batch(row[index: index + 3], mode="variable")
                    y_variables = board.get_variable(row[index + 1].down())
                    if y_variables is None:
                        continue
                    for vals in vals_list:
                        cond = model.NewBoolVar(f"[3E]{bool_var_index}")
                        model.Add(vals[0] == 4 * variables[0] + 2 * variables[1] + variables[2]).OnlyEnforceIf(cond)
                        model.Add(vals[0] != 4 * variables[0] + 2 * variables[1] + variables[2]).OnlyEnforceIf(cond.Not())
                        model.Add(y_variables == vals[1]).OnlyEnforceIf(cond)
                        bool_var_index += 1

    def init_board(self, board: 'AbstractBoard'):
        y_col = board.get_col_pos(board.boundary(key=NAME_3E[1]))
        col = board.get_col_pos(board.boundary())
        for pos in col:
            row = board.get_row_pos(pos)
            for index in range(len(row) - 2):
                types = board.batch(row[index: index + 3], mode="type")
                y_type = board.get_type(row[index + 1].down())
                if y_type == "":
                    continue
                index = 4 if types[0] == "F" else 0
                index += 2 if types[1] == "F" else 0
                index += 1 if types[2] == "F" else 0
                board.set_value(y_col[index], MINES_TAG if y_type == "F" else VALUE_QUESS)

        for pos, _ in board("N", key=NAME_3E[1]):
            board.set_value(pos, VALUE_QUESS)

    def init_clear(self, board: 'AbstractBoard'):
        y_col = board.get_col_pos(board.boundary(key=NAME_3E[1]))
        col = board.get_col_pos(board.boundary())
        for pos in col:
            row = board.get_row_pos(pos)
            for index in range(len(row) - 2):
                types = board.batch(row[index: index + 3], mode="type")
                y_type = board.get_type(row[index + 1].down())
                if y_type == "":
                    continue
                index = 4 if types[0] == "F" else 0
                index += 2 if types[1] == "F" else 0
                index += 1 if types[2] == "F" else 0
                board.set_value(y_col[index], MINES_TAG)

        for pos, _ in board("N", key=NAME_3E[1]):
            board.set_value(pos, VALUE_QUESS)

        for pos, _ in board("F", key=NAME_3E[1]):
            board.set_value(pos, None)

    @classmethod
    def method_choose(cls) -> int:
        return 1
