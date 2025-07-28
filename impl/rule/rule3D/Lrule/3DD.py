#!/usr/bin/env python3
"""
[3DD] 蛆 (Dual)：所有雷均形成1x2x1、2x1x1或1x1x2的三维矩形，即每个雷恰好有一个六连通相邻的雷
"""

from .. import Abstract3DMinesRule
from abs.board import AbstractBoard
from utils.solver import get_model


class Rule3DD(Abstract3DMinesRule):  # type: ignore
    name = "3DD"
    subrules = [
        [True, "[3DD] 对偶"]
    ]

    def create_constraints(self, board: 'AbstractBoard'):
        if not self.subrules[0][0]:
            return

        model = get_model()
        for pos, var in board(mode="variable"):
            # 获取六连通邻域：同层四连通 + 上下层对应位置
            six_neighbors = self._get_six_connected_neighbors(board, pos)
            six_neighbor_vars = board.batch(six_neighbors, mode="variable", drop_none=True)

            if not six_neighbor_vars:
                # 如果没有六连通邻居，该位置不能是雷
                model.Add(var == 0)
                continue

            # 核心约束：每个雷恰好有1个六连通相邻的雷
            # val 为1时，六连通邻域中必须有且仅有一个雷
            sum_vals = sum(six_neighbor_vars)
            model.Add(sum_vals == 1).OnlyEnforceIf(var)

    def _get_six_connected_neighbors(self, board: 'AbstractBoard', pos):
        """获取六连通邻域：同层四连通 + 上下层对应位置"""
        neighbors = []

        # 同层四连通邻域（左右上下）
        four_neighbors = pos.neighbors(1)
        neighbors.extend(four_neighbors)

        # 上层对应位置
        up_pos = self.up(board, pos, n=1)
        if up_pos is not None:
            neighbors.append(up_pos)

        # 下层对应位置
        down_pos = self.down(board, pos, n=1)
        if down_pos is not None:
            neighbors.append(down_pos)

        return neighbors

    def check(self, board: 'AbstractBoard') -> bool:
        """验证规则是否满足"""
        for pos, dye in board(mode="dye"):
            # 获取六连通邻域
            six_neighbors = self._get_six_connected_neighbors(board, pos)
            types = board.batch(six_neighbors, mode="type", drop_none=True)

            # 统计雷的数量
            mine_count = types.count("F")

            if mine_count > 1:
                # 如果有超过1个相邻的雷，违反规则
                return False
            elif mine_count == 1:
                # 恰好有1个相邻的雷，符合规则
                continue
            elif mine_count == 0:
                # 没有相邻的雷，检查是否有未知位置
                unknown_count = types.count("N")
                if unknown_count == 0:
                    # 没有相邻的雷且没有未知位置，违反规则
                    return False
        return True

    @classmethod
    def method_choose(cls) -> int:
        return 3

    def suggest_total(self, info: dict):
        """建议雷的总数应该是偶数，因为雷成对出现"""
        def constraint_even_total(model, total):
            model.AddModuloEquality(0, total, 2)
        info["hard_fns"].append(constraint_even_total)
