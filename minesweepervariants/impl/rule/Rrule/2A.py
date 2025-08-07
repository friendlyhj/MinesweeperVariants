#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# @Time    : 2025/06/16 09:20
# @Author  : xxx
# @FileName: 2A.py
"""
[2A]面积: 线索表示四方向相邻雷区域的面积之和
(注:如果出现大数字则速率极度底下)
"""
from ....abs.Rrule import AbstractClueRule, AbstractClueValue
from ....abs.board import AbstractBoard, AbstractPosition

from ....utils.tool import get_logger


class Rule2A(AbstractClueRule):
    # name = ["2A", "面积", "Area"]
    doc = "线索表示四方向相邻雷区域的面积之和"

    def fill(self, board: 'AbstractBoard') -> 'AbstractBoard':
        logger = get_logger()
        for pos, _ in board("N"):
            checked = [[False for j in range(20)] for i in range(20)]

            def dfs(p: 'AbstractPosition', _checked):
                if not board.in_bounds(p): return None
                if board.get_type(p) != "F": return None
                if _checked[p.x][p.y]: return None
                _checked[p.x][p.y] = True
                dfs(p.left(1), _checked)
                dfs(p.right(1), _checked)
                dfs(p.up(1), _checked)
                dfs(p.down(1), _checked)
                return None

            dfs(pos.left(1), checked)
            dfs(pos.right(1), checked)
            dfs(pos.up(1), checked)
            dfs(pos.down(1), checked)
            cnt = 0
            for i in range(20):
                for j in range(20):
                    if checked[i][j]:
                        cnt += 1
            board.set_value(pos, Value2A(pos, bytes([cnt])))
            logger.debug(f"Set {pos} to 2A[{cnt}]")
        return board

    def clue_class(self):
        return Value2A


class Value2A(AbstractClueValue):
    def __init__(self, pos: 'AbstractPosition', code: bytes = None):
        super().__init__(pos, code)
        self.value = code[0]
        self.neighbor = pos.neighbors(1)
        self.pos = pos

    def __repr__(self) -> str:
        return f"{self.value}"

    @classmethod
    def type(cls) -> bytes:
        return Rule2A.name[0].encode("ascii")

    def code(self) -> bytes:
        return bytes([self.value])

    def create_constraints(self, board: 'AbstractBoard', switch):
        # 跳过已有的线索格
        model = board.get_model()
        s = switch.get(model, self)
        possible_list = set()

        def dfs(step=0, checked=None, valides=None):
            if valides is None:
                valides = [self.pos]
            if checked is None:
                checked = []
            if step == self.value + 1:
                possible_list.add((tuple(sorted(set(valides))), tuple(sorted(set(checked)))))
                return
            for pos in sorted(set(valides)):
                if pos != self.pos and board.get_type(pos) == "C":
                    continue
                if pos in checked:
                    continue
                checked.append(pos)
                valides.remove(pos)
                pos_list = []
                for _pos in pos.neighbors(1):
                    if _pos in checked:
                        continue
                    if _pos in valides:
                        continue
                    if not board.in_bounds(_pos):
                        continue
                    valides.append(_pos)
                    pos_list.append(_pos)
                dfs(step + 1, checked, valides)
                for _pos in pos_list:
                    valides.remove(_pos)
                checked.remove(pos)
                valides.append(pos)

        # print(board.show_board())
        # print("\t", self.pos, self, end='\r')
        dfs()
        # print("dfs done", end='\r')

        tmp_list = []
        for vars_t, vars_f in possible_list:
            # print()
            # print(vars_t)
            # print(vars_f)
            if any(t_pos in vars_f for t_pos in vars_t):
                continue
            if any(f_pos in vars_t for f_pos in vars_f):
                continue
            vars_f = [var_f for var_f in vars_f if var_f != self.pos]
            vars_t = board.batch(vars_t, mode="variable")
            vars_f = board.batch(vars_f, mode="variable")
            tmp = model.NewBoolVar("tmp")
            model.Add(sum(vars_t) == 0).OnlyEnforceIf(tmp)
            if vars_f:
                model.AddBoolAnd(vars_f).OnlyEnforceIf(tmp)
            tmp_list.append(tmp)
        model.AddBoolOr(tmp_list).OnlyEnforceIf(s)
        # print(self.pos, self, len(tmp_list))

        # import sys
        # sys.exit(0)
        # print("done")
