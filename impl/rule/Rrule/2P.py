#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# @Time    : 2025/07/05 07:51
# @Author  : Wu_RH
# @FileName: 2P.py
"""
[2P] 乘积 (Product)：线索表示距离最近的 2 个雷的距离之积
"""
from typing import List, Dict

from abs.Rrule import AbstractClueValue, AbstractClueRule
from abs.board import AbstractPosition, AbstractBoard
from utils.image_create import get_text, get_image, get_row, get_col, get_dummy
from utils.solver import get_model


def sqrt_form(n):
    """
    将正整数 n 写作n平方根的最简形式：a√b。
    例如：输入 8，输出 "2√2"；输入 4，输出 "2"；输入 2，输出 "√2"。
    """
    if n <= 0:
        return 0, -1

    a = 1  # 初始化平方因子部分
    b = n  # 初始化剩余部分
    i = 2  # 从最小质因数开始遍历

    # 提取所有平方因子：将 n 分解为 a^2 * b（b 无平方因子）
    while i * i <= b:
        # 当 i^2 整除 b 时，重复除去该因子
        while b % (i * i) == 0:
            b //= i * i  # 整数除法，更新剩余部分
            a *= i  # 更新平方因子部分
        i += 1

    # 根据 a 和 b 的值格式化输出
    if b == 1:
        return a, -1  # 例如 n=4, 输出 "2"
    elif a == 1:
        return -1, b  # 例如 n=2, 输出 "√2"
    else:
        return a, b  # 例如 n=8, 输出 "2√2"


def get_factor_pairs(n):
    """
    返回正整数n的所有正整数乘法因子对（去重）

    参数:
        n: 正整数

    返回:
        列表，包含所有因子对 (a, b) 满足 a × b = n 且 a ≤ b
        按第一个因子升序排列
    """
    pairs = []
    # 只需遍历到平方根即可
    for i in range(1, int(n ** 0.5) + 1):
        if n % i == 0:
            j = n // i
            # 确保 a ≤ b
            if i <= j:
                pairs.append((i, j))
    return pairs


class Rule2P(AbstractClueRule):
    name = "2P"

    def fill(self, board: 'AbstractBoard') -> 'AbstractBoard':
        if len([_ for _ in board("F")]) < 2:
            return board
        for pos, _ in board("N"):
            r = 0
            a_lay = b_lay = -1

            while b_lay == -1:
                r += 1
                count = board.batch(pos.neighbors(r, r), mode="type").count("F")
                if count >= 2:
                    if a_lay == -1:
                        a_lay = b_lay = r
                    else:
                        b_lay = r
                elif count == 1:
                    if a_lay == -1:
                        a_lay = r
                    else:
                        b_lay = r
            if a_lay * b_lay > 254:
                value = a_lay * b_lay
                obj = Value2P(pos, bytes([value // 255, value % 255]))
            else:
                obj = Value2P(pos, bytes([a_lay * b_lay]))
            board.set_value(pos, obj)
        return board

    def clue_class(self):
        return Value2P


class Value2P(AbstractClueValue):
    def __init__(self, pos: 'AbstractPosition', code: bytes = b''):
        self.pos = pos
        if len(code) == 1:
            self.value = code[0]
        elif len(code) == 2:
            self.value = code[0] * 255 + code[1]

    def __repr__(self):
        value_a, value_b = sqrt_form(self.value)
        if value_b == -1:
            return f"{value_a}"
        elif value_a == -1:
            return f"√{value_b}"
        return f"{value_a}√{value_b}"

    def compose(self, board) -> List[Dict]:
        value_a, value_b = sqrt_form(self.value)
        if value_b == -1:
            return [get_col(
                get_dummy(height=0.175),
                get_text(str(value_a)),
                get_dummy(height=0.175),
            )]
        elif value_a == -1:
            return [get_row(
                get_image("sqrt"),
                get_text(str(value_b)),
                spacing=-0.15
            )]
        else:
            return [get_row(
                get_text(str(value_a)),
                get_image("sqrt"),
                get_text(str(value_b)),
                spacing=-0.2
            )]

    @classmethod
    def method_choose(cls) -> int:
        return 1

    @classmethod
    def type(cls) -> bytes:
        return Rule2P.name.encode("ascii")

    def code(self) -> bytes:
        if self.value > 254:
            return bytes([self.value // 255, self.value % 255])
        return bytes([self.value])

    def create_constraints(self, board: 'AbstractBoard'):
        model = get_model()

        var_list = []
        for par_a, par_b in get_factor_pairs(self.value):
            var = model.NewBoolVar("[2P]")
            if par_a == par_b:
                nei = self.pos.neighbors(par_a, par_a)
                model.Add(sum(board.batch(nei, mode="variable", drop_none=True)) >= 2).OnlyEnforceIf(var)
            else:
                nei_a = self.pos.neighbors(par_a, par_a)
                model.Add(sum(board.batch(nei_a, mode="variable", drop_none=True)) == 1).OnlyEnforceIf(var)
                nei_b = self.pos.neighbors(par_b, par_b)
                model.Add(sum(board.batch(nei_b, mode="variable", drop_none=True)) >= 1).OnlyEnforceIf(var)
                none_var = self.pos.neighbors(0, par_a - 1) + self.pos.neighbors(par_a + 1, par_b - 1)
                model.Add(sum(board.batch(none_var, mode="variable", drop_none=True)) == 0).OnlyEnforceIf(var)
            var_list.append(var)
        model.AddBoolOr(var_list)

