#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# @Time    : 2025/07/04 07:39
# @Author  : Wu_RH
# @FileName: 4V.py
"""
[4V]2X'plus: 线索表示数字是两个题板中相同位置的其中一个范围中心3*3区域的雷总数
"""

from abs.Rrule import AbstractClueRule, AbstractClueValue
from abs.board import AbstractBoard, AbstractPosition, MASTER_BOARD
from utils.impl_obj import VALUE_QUESS, MINES_TAG
from utils.solver import get_model
from utils.tool import get_random


class Rule4V(AbstractClueRule):
    name = "4V"
    size = 1

    def __init__(self, board: "AbstractBoard" = None, data=None) -> None:
        super().__init__(board, data)
        size = (board.boundary().x + 1, board.boundary().y + 1)
        for i in range(self.size):
            key = self.name + f"_{i}"
            board.generate_board(key, size)
            board.set_config(key, "interactive", True)
            board.set_config(key, "row_col", True)
            board.set_config(key, "VALUE", VALUE_QUESS)
            board.set_config(key, "MINES", MINES_TAG)

    def fill(self, board: 'AbstractBoard') -> 'AbstractBoard':
        random = get_random()

        for key in [MASTER_BOARD] + [self.name + f"_{i}" for i in range(self.size)]:
            for pos, _ in board("N", key=key):
                neighbors_list = []
                for _key in [MASTER_BOARD] + [self.name + f"_{i}" for i in range(Rule4V.size)]:
                    _pos = pos.clone()
                    _pos.board_key = _key
                    neighbors_list.append(_pos.neighbors(0, 2))
                count = random.choice([board.batch(positions, mode="type").count("F")
                                       for positions in neighbors_list])
                value = Value4V(pos=pos, code=bytes([count]))
                value.value = count
                board.set_value(pos, value)

        return board

    def clue_class(self):
        return Value4V

    def create_constraints(self, board: 'AbstractBoard') -> bool:
        return super().create_constraints(board)

    def suggest_total(self, info: dict):
        ub = 0
        for key in info["interactive"]:
            size = info["size"][key]
            ub += size[0] * size[1]
        info["soft_fn"](ub * 0.4)


class Value4V(AbstractClueValue):
    def __init__(self, pos: 'AbstractPosition', code: bytes = b''):
        self.neighbors_list = []
        for key in [MASTER_BOARD] + [Rule4V.name + f"_{i}" for i in range(Rule4V.size)]:
            _pos = pos.clone()
            _pos.board_key = key
            self.neighbors_list.append(_pos.neighbors(0, 2))
        self.value = code[0]

    @classmethod
    def method_choose(cls) -> int:
        return 1

    @classmethod
    def type(cls) -> bytes:
        return Rule4V.name.encode("ascii")

    def __repr__(self) -> str:
        return f"{self.value}"

    def create_constraints(self, board: 'AbstractBoard'):
        model = get_model()

        sum_var = []
        for neighbor in self.neighbors_list:
            var_list = board.batch(neighbor, mode="variable", drop_none=True)
            if var_list:
                b = model.NewBoolVar(f"[{Rule4V.name}]tmp")
                model.Add(sum(var_list) == self.value).OnlyEnforceIf(b)
                model.Add(sum(var_list) != self.value).OnlyEnforceIf(b.Not())
                sum_var.append(b)
        model.AddBoolOr(sum_var)

    def code(self) -> bytes:
        return bytes([self.value])
