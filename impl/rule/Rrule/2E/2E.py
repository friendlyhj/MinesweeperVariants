#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# @Time    : 2025/07/01 07:30
# @Author  : Wu_RH
# @FileName: 2E.py
"""
[2E]加密: 线索被字母所取代，每个字母对应一个线索，且每个线索对应一个字母
"""
from typing import List

from abs.board import AbstractBoard, AbstractPosition
from abs.Rrule import AbstractClueRule, AbstractClueValue
from utils.impl_obj import VALUE_QUESS, VALUE_CROSS, VALUE_CIRCLE
from utils.solver import get_model
from utils.tool import get_random


class Rule2E(AbstractClueRule):
    name = "2E"
    subrules = [
        [True, "[2E]每个字母对应一个线索，且每个线索对应一个字母"]
    ]

    def __init__(self, data=None, board: 'AbstractBoard' = None):
        super().__init__(data, board)
        pos = board.boundary()
        size = min(pos.x + 1, 9)
        board.generate_board(self.name, (size, size))
        board.set_config(self.name, "pos_label", True)

    def fill(self, board: 'AbstractBoard') -> 'AbstractBoard':
        random = get_random()
        shuffled_nums = [i for i in range(min(9, board.boundary().x + 1))]
        random.shuffle(shuffled_nums)
        for pos, _ in board("N"):
            count = board.batch(pos.neighbors(2), mode="type").count("F")
            if count not in shuffled_nums:
                board.set_value(pos, VALUE_QUESS)
            else:
                code = bytes([shuffled_nums[count]])
                board.set_value(pos, Value2E(pos, code))

        for x, y in enumerate(shuffled_nums):
            pos = board.get_pos(x, y, self.name)
            board.set_value(pos, VALUE_CIRCLE)

        for pos, _ in board("N", key=self.name):
            board.set_value(pos, VALUE_CROSS)

        return board

    def clue_class(self):
        return Value2E

    def create_constraints(self, board: 'AbstractBoard') -> bool:
        if not self.subrules[0][0]:
            return super().create_constraints(board)

        model = get_model()
        bound = board.boundary(key=self.name)

        row = board.get_row_pos(bound)
        for pos in row:
            line = board.get_col_pos(pos)
            var = board.batch(line, mode="variable")
            model.Add(sum(var) == 1)

        col = board.get_col_pos(bound)
        for pos in col:
            line = board.get_row_pos(pos)
            var = board.batch(line, mode="variable")
            model.Add(sum(var) == 1)

        return super().create_constraints(board)

    def init_clear(self, board: 'AbstractBoard'):
        for pos, _ in board(key=self.name):
            board.set_value(pos, None)


class Value2E(AbstractClueValue):
    def __init__(self, pos: 'AbstractPosition', code: bytes = b''):
        self.value = code[0]
        self.neighbors = pos.neighbors(2)

    def __repr__(self) -> str:
        return "ABCDEFGHI"[self.value]

    def high_light(self, board: 'AbstractBoard') -> List['AbstractPosition']:
        return self.neighbors

    @classmethod
    def type(cls) -> bytes:
        return Rule2E.name.encode("ascii")

    @classmethod
    def method_choose(cls) -> int:
        return 1

    def code(self) -> bytes:
        return bytes([self.value])

    def create_constraints(self, board: 'AbstractBoard'):
        model = get_model()

        line = board.batch(board.get_col_pos(
            board.get_pos(0, self.value, Rule2E.name)
        ), mode="variable")

        neighbors = board.batch(self.neighbors, mode="variable", drop_none=True)

        for index in range(len(line)):
            model.Add(sum(neighbors) == index).OnlyEnforceIf(line[index])
            model.Add(sum(neighbors) != index).OnlyEnforceIf(line[index].Not())
