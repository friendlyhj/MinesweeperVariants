#!/usr/bin/env python3
"""
[3D1U] 3D一元 (Unary)：所有雷不能与其他雷相邻
"""
from abs.board import AbstractBoard
from .. import Abstract3DMinesRule
from utils.solver import get_model


class Rule3D1U(Abstract3DMinesRule):
    name = "3D1U"
    subrules = [
        [True, "[3D1U]一元"]
    ]

    def create_constraints(self, board: AbstractBoard):
        if not self.subrules[0][0]:
            return
        model = get_model()
        for pos, var in board(mode="variable"):
            if board.in_bounds(pos.down()):
                model.Add(board.get_variable(pos.down()) == 0).OnlyEnforceIf(var)
            if board.in_bounds(pos.up()):
                model.Add(board.get_variable(pos.up()) == 0).OnlyEnforceIf(var)
            if board.in_bounds(pos.right()):
                model.Add(board.get_variable(pos.right()) == 0).OnlyEnforceIf(var)
            if board.in_bounds(pos.left()):
                model.Add(board.get_variable(pos.left()) == 0).OnlyEnforceIf(var)
            if Abstract3DMinesRule.up(board, pos, n=1):
                model.Add(board.get_variable(self.up(board, pos, n=1)) == 0).OnlyEnforceIf(var)
            if Abstract3DMinesRule.down(board, pos, n=1):
                model.Add(board.get_variable(self.down(board, pos, n=1)) == 0).OnlyEnforceIf(var)

    def check(self, board: 'AbstractBoard') -> bool:
        pass

    @classmethod
    def method_choose(cls) -> int:
        return 1
