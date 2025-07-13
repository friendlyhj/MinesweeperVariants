#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# @Time    : 2025/07/09 10:32
# @Author  : Wu_RH
# @FileName: 1E.py
"""
[1E'] 视差 (Eyesight')：线索表示纵向和横向的视野之差，箭头指示视野更长的方向
"""
from typing import Callable, List, Dict

from abs.Rrule import AbstractClueRule, AbstractClueValue
from abs.board import AbstractBoard, AbstractPosition
from utils.image_create import get_row, get_image, get_text, get_col, get_dummy
from utils.solver import get_model


class Rule1E(AbstractClueRule):
    name = "1E'"

    def clue_class(self):
        return Value1E

    def fill(self, board: 'AbstractBoard') -> 'AbstractBoard':
        fn: Callable[[int], AbstractPosition]
        for pos, _ in board("N"):
            value = 0
            for fn in [pos.up, pos.down]:
                n = 1
                while board.get_type(fn(n)) not in "F":
                    n += 1
                    value += 1
            for fn in [pos.left, pos.right]:
                n = 1
                while board.get_type(fn(n)) not in "F":
                    n += 1
                    value -= 1
            obj = Value1E(pos, bytes([value + 128]))
            board.set_value(pos, obj)
        return board


class Value1E(AbstractClueValue):
    def __init__(self, pos: 'AbstractPosition', code: bytes = b''):
        self.value = code[0] - 128
        self.pos = pos

    def __repr__(self):
        return str(self.value)

    def compose(self, board) -> List[Dict]:
        if self.value == 0:
            return super().compose(board)
        if self.value < 0:
            return [get_col(
                get_image(
                    "double_horizontal_arrow",
                    image_height=0.4,
                ),
                get_dummy(height=-0.1),
                get_text(str(-self.value))
            )]
        if self.value > 0:
            return [
                get_row(
                    get_dummy(width=0.15),
                    get_image("double_vertical_arrow", ),
                    get_dummy(width=-0.15),
                    get_text(str(self.value)),
                    get_dummy(width=0.15),
                ),
            ]

    @classmethod
    def method_choose(cls) -> int:
        return 1

    @classmethod
    def type(cls) -> bytes:
        return Rule1E.name.encode("ascii")

    def code(self) -> bytes:
        return bytes([self.value + 128])

    def create_constraints(self, board: 'AbstractBoard'):
        def dfs(value: int, pos: 'AbstractPosition'):
            def AddPossibility(_pos: 'AbstractPosition', i: int, j: int):
                """
                输入：pos，对应的位置；i：竖着的格子数量；j：横着的格子数量
                输出：无，但是自动在possible_list里面加上对应的情况
                """
                for up in range(i):  # 遍历向上 up 格，可以为 0，不能为 i，注意本身也要算一格
                    if not (board.in_bounds(_pos.up(up)) and board.in_bounds(_pos.down(i - up - 1))): continue
                    for right in range(j):  # 遍历向右 right 格，可以为 0，不能为 j，注意本身也要算一格
                        if (not (board.in_bounds(_pos.right(right)) and
                                 board.in_bounds(_pos.left(j - right - 1)))): continue
                        # 到这里的都是符合的情况，开始加 possible_list
                        lst_1 = []
                        lst_2 = []
                        for m in range(up + 1):
                            if m == up:
                                if board.in_bounds(_pos.up(m + 1)): lst_2.append(_pos.up(m + 1))
                            lst_1.append(_pos.up(m))
                        for m in range((i - up - 1) + 1):
                            if m == i - up - 1:
                                if board.in_bounds(_pos.down(m + 1)): lst_2.append(_pos.down(m + 1))
                            lst_1.append(_pos.down(m))
                        for m in range(right + 1):
                            if m == right:
                                if board.in_bounds(_pos.right(m + 1)): lst_2.append(_pos.right(m + 1))
                            lst_1.append(_pos.right(m))
                        for m in range((j - right - 1) + 1):
                            if m == j - right - 1:
                                if board.in_bounds(_pos.left(m + 1)): lst_2.append(_pos.left(m + 1))
                            lst_1.append(_pos.left(m))
                        if lst_1 == [] and lst_2 == []: continue
                        possible_list.append((set(lst_1), set(lst_2[:])))

            size = board.get_config(self.pos.board_key, "size")  # 题板尺寸二元组，先行数再列数
            # 列举符合线索值的情况
            for i in range(1, size[1] + 1):  # i：竖着能看到的格子数量
                j = i - value  # j：横着能看到的格子数量
                if j < 1 or j > size[0]: continue
                AddPossibility(pos, i, j)

        model = get_model()

        possible_list = []

        dfs(value=self.value, pos=self.pos)
        tmp_list = []

        for vars_t, vars_f in possible_list:
            vars_t = board.batch(vars_t, mode="variable")
            vars_f = board.batch(vars_f, mode="variable")
            tmp = model.NewBoolVar("tmp")
            model.Add(sum(vars_t) == 0).OnlyEnforceIf(tmp)
            model.AddBoolAnd(vars_f).OnlyEnforceIf(tmp)
            tmp_list.append(tmp)
        model.AddBoolOr(tmp_list)
