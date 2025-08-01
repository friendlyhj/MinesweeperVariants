#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# @Time    : 2025/06/10 18:09
# @Author  : Wu_RH
# @FileName: 1M.py
"""
[1M]多雷: 每个染色格的雷被视为两个(总雷数不受限制)
"""

from abs.board import AbstractBoard, AbstractPosition
from abs.Rrule import AbstractClueRule, AbstractClueValue
from utils.solver import get_model
from utils.tool import get_logger
from utils.impl_obj import VALUE_QUESS, MINES_TAG


class Rule1M(AbstractClueRule):
    name = ["1M", "M", "多雷"]
    doc = "每个染色格的雷被视为两个(总雷数不受限制)"

    def fill(self, board: 'AbstractBoard'):
        logger = get_logger()
        for pos, _ in board("N"):
            positions = pos.neighbors(2)
            value = 0
            for t, d in zip(
                    board.batch(positions, "type"),
                    board.batch(positions, "dye")
            ):
                if t != "F":
                    continue
                if d:
                    value += 2
                else:
                    value += 1
            obj = Value1M(pos, code=bytes([value]))
            board.set_value(pos, obj)
            logger.debug(f"[1M]: put {obj} to {pos}")
        return board

    def clue_class(self):
        return Value1M


class Value1M(AbstractClueValue):
    value: int
    neighbors: list

    def __init__(self, pos: 'AbstractPosition', code: bytes = b''):
        super().__init__(pos)
        self.value = code[0]
        self.neighbors = pos.neighbors(2)

    def __repr__(self) -> str:
        return f"{self.value}"

    def high_light(self, board: 'AbstractBoard') -> list['AbstractPosition']:
        return self.neighbors

    @classmethod
    def type(cls) -> bytes:
        return Rule1M.name[0].encode("ascii")

    def code(self) -> bytes:
        return bytes([self.value])

    def deduce_cells(self, board: 'AbstractBoard') -> bool:
        min_value = 0
        max_value = 0
        types = board.batch(self.neighbors, "type")
        if "N" not in types:
            return False
        dyes = board.batch(self.neighbors, "dye")
        for pos, dye in zip(self.neighbors, dyes):
            if board.get_type(pos) == "F":
                min_value += 2 if dye else 1
                max_value += 2 if dye else 1
            elif board.get_type(pos) == "N":
                max_value += 2 if dye else 1
        if min_value == self.value:
            [board.set_value(pos, VALUE_QUESS) for pos in self.neighbors if board.get_type(pos) == "N"]
            return True
        if max_value == self.value:
            [board.set_value(pos, MINES_TAG) for pos in self.neighbors if board.get_type(pos) == "N"]
            return True
        return False

    def create_constraints(self, board: 'AbstractBoard'):
        model = get_model()
        vals = []
        dyes = board.batch(self.neighbors, "dye")
        for pos, dye in zip(self.neighbors, dyes):
            if board.get_type(pos) != "N":
                continue
            if dye:
                vals.append(board.get_variable(pos) * 2)
            else:
                vals.append(board.get_variable(pos))
        if vals:
            model.Add(sum(vals) == self.value)

    def check(self, board: 'AbstractBoard') -> bool:
        min_value = 0
        max_value = 0
        dyes = board.batch(self.neighbors, "dye")
        for pos, dye in zip(self.neighbors, dyes):
            if board.get_type(pos) == "F":
                min_value += 2 if dye else 1
                max_value += 2 if dye else 1
            elif board.get_type(pos) == "N":
                max_value += 2 if dye else 1
        return min_value < self.value < max_value

    @classmethod
    def method_choose(cls) -> int:
        return 3
