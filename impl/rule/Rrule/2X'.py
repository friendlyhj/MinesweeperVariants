#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# 
# @Time    : 2025/06/16 09:20
# @Author  : xxx
# @FileName: 2X'.py
"""
[2X'] 十字' (Cross')：线索表示 3x3 范围内染色格或非染色格的雷数
"""
from abs.Rrule import AbstractClueRule, AbstractClueValue
from abs.board import AbstractBoard, AbstractPosition

from utils.tool import get_logger, get_random
from utils.solver import get_model


class Rule2X(AbstractClueRule):
    name = "2X'"

    def fill(self, board: 'AbstractBoard') -> 'AbstractBoard':
        logger = get_logger()
        r = get_random()
        for pos, _ in board("N"):
            value1 = len([_pos for _pos in pos.neighbors(3) if board.get_type(_pos) == "F" and board.get_dyed(_pos)])
            value2 = len([_pos for _pos in pos.neighbors(3) if board.get_type(_pos) == "F" and not board.get_dyed(_pos)])
            board.set_value(pos, Value2X(pos, bytes([r.choice([value1, value2])])))
            logger.debug(f"Set {pos} to 2X[{value1 * 10 + value2}]")
        return board

    def clue_class(self):
        return Value2X


class Value2X(AbstractClueValue):
    def __init__(self, pos: 'AbstractPosition', code: bytes = None):
        super().__init__(pos, code)
        self.neighbor = self.pos.neighbors(2)
        self.value = code[0]

    def __repr__(self) -> str:
        return f"{self.value}"

    @classmethod
    def type(cls) -> bytes:
        return Rule2X.name.encode("ascii")

    def code(self) -> bytes:
        return bytes([self.value])

    def create_constraints(self, board: 'AbstractBoard'):
        """创建CP-SAT约束: 周围染色格雷数等于两个染色格的数量"""
        model = get_model()

        # 收集周围格子的布尔变量
        var_a_list = []
        var_b_list = []
        for pos in self.neighbor:
            if not board.in_bounds(pos):
                continue
            dye = board.get_dyed(pos)
            if dye:
                var_b_list.append(board.get_variable(pos))
            else:
                var_a_list.append(board.get_variable(pos))

        var_a = model.NewBoolVar("[2X]")
        var_b = model.NewBoolVar("[2X]")
        model.Add(sum(var_a_list) == self.value).OnlyEnforceIf(var_a)
        model.Add(sum(var_b_list) == self.value).OnlyEnforceIf(var_b)
        model.AddBoolOr([var_a, var_b])

    def deduce_cells(self, board: 'AbstractBoard') -> bool:
        return False

    def check(self, board: 'AbstractBoard') -> bool:
        return False

    @classmethod
    def method_choose(cls) -> int:
        return 3
