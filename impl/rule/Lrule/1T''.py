#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# @Time    : 2025/06/15 11:59
# @Author  : Wu_RH
# @FileName: 1T''.py

"""
[1T'']纯三连：所有雷格必须与其他雷组成三连，且最终题板可以为每一个雷构造唯一的三连组（我又表达困难了，淦）
"""

from abs.Lrule import AbstractMinesRule
from abs.board import AbstractBoard
from utils.solver import get_model


class Rule1Tpp(AbstractMinesRule):
    # name = ["1T''", "纯三连"]
    doc = "所有雷格必须与其他雷组成三连，且最终题板可以为每一个雷构造唯一的三连组（我又表达困难了，淦）"
    subrules = [
        [True, "[1T'']"]
    ]

    def create_constraints(self, board: 'AbstractBoard'):
        if not self.subrules[0][0]:
            return

        model = get_model()

        for key in board.get_interactive_keys():
            boundary_pos = board.boundary(key=key)

            board.get_variable(boundary_pos)
            b_vars = [board.batch(board.get_col_pos(pos), mode="variable")
                      for pos in board.get_row_pos(boundary_pos)]
            M, N = len(b_vars), len(b_vars[0])

            h_vars = []  # 水平三联块变量 h[i][j]
            v_vars = []  # 垂直三联块变量 v[i][j]
            d1_vars = []  # 主对角线方向三联块变量（从左上到右下） d1[i][j]
            d2_vars = []  # 次对角线方向三联块变量（从右上到左下） d2[i][j]

            # 创建水平块变量
            for i in range(M):
                row = []
                for j in range(N - 2):
                    var = model.NewBoolVar(f"h_{i}_{j}")
                    row.append(var)
                    # 如果块存在，则三个格子必须是 True
                    model.AddImplication(var, b_vars[i][j])
                    model.AddImplication(var, b_vars[i][j + 1])
                    model.AddImplication(var, b_vars[i][j + 2])
                h_vars.append(row)

            # 创建垂直块变量
            for i in range(M - 2):
                col = []
                for j in range(N):
                    var = model.NewBoolVar(f"v_{i}_{j}")
                    col.append(var)
                    model.AddImplication(var, b_vars[i][j])
                    model.AddImplication(var, b_vars[i + 1][j])
                    model.AddImplication(var, b_vars[i + 2][j])
                v_vars.append(col)

            # 创建主对角线方向块变量（左上到右下）
            for i in range(M - 2):
                diag1_row = []
                for j in range(N - 2):
                    var = model.NewBoolVar(f"d1_{i}_{j}")
                    diag1_row.append(var)
                    model.AddImplication(var, b_vars[i][j])
                    model.AddImplication(var, b_vars[i + 1][j + 1])
                    model.AddImplication(var, b_vars[i + 2][j + 2])
                d1_vars.append(diag1_row)

            # 创建次对角线方向块变量（右上到左下）
            for i in range(M - 2):
                diag2_row = []
                for j in range(2, N):
                    var = model.NewBoolVar(f"d2_{i}_{j}")
                    diag2_row.append(var)
                    model.AddImplication(var, b_vars[i][j])
                    model.AddImplication(var, b_vars[i + 1][j - 1])
                    model.AddImplication(var, b_vars[i + 2][j - 2])
                d2_vars.append(diag2_row)

            # 计算每个格子的覆盖次数 cover_count[i][j]
            cover_count = []
            for i in range(M):
                row_counts = []
                for j in range(N):
                    cover_vars = []

                    # 水平覆盖：块起点可能在 j, j-1, j-2
                    if j <= N - 3:
                        cover_vars.append(h_vars[i][j])
                    if 1 <= j <= N - 2:
                        cover_vars.append(h_vars[i][j - 1])
                    if j >= 2:
                        cover_vars.append(h_vars[i][j - 2])

                    # 垂直覆盖：块起点可能在 i, i-1, i-2
                    if i <= M - 3:
                        cover_vars.append(v_vars[i][j])
                    if 1 <= i <= M - 2:
                        cover_vars.append(v_vars[i - 1][j])
                    if i >= 2:
                        cover_vars.append(v_vars[i - 2][j])

                    # 主对角线覆盖：块起点可能在 (i,j), (i-1,j-1), (i-2,j-2)
                    if i <= M - 3 and j <= N - 3:
                        cover_vars.append(d1_vars[i][j])
                    if 1 <= i <= M - 2 and 1 <= j <= N - 2:
                        cover_vars.append(d1_vars[i - 1][j - 1])
                    if i >= 2 and j >= 2:
                        cover_vars.append(d1_vars[i - 2][j - 2])

                    # 次对角线覆盖：块起点可能在 (i,j), (i-1,j+1), (i-2,j+2)
                    if i <= M - 3 and j >= 2:
                        cover_vars.append(d2_vars[i][j - 2])
                    if 1 <= i <= M - 2 and j + 1 < N:
                        cover_vars.append(d2_vars[i - 1][j - 1])
                    if i >= 2 and j + 2 < N:
                        cover_vars.append(d2_vars[i - 2][j])

                    # cover_count[i][j] 是覆盖变量的和
                    var_cover_count = model.NewIntVar(0, len(cover_vars), f"cover_count_{i}_{j}")
                    model.Add(var_cover_count == sum(cover_vars))
                    row_counts.append(var_cover_count)
                cover_count.append(row_counts)

            # 强制每个格子的覆盖数等于该格是否为True
            for i in range(M):
                for j in range(N):
                    model.Add(cover_count[i][j] == b_vars[i][j])

    @classmethod
    def method_choose(cls) -> int:
        return 1

    def suggest_total(self, info: dict):

        def hard_constraint(m, total):
            m.AddModuloEquality(0, total, 3)

        info["hard_fns"].append(hard_constraint)
