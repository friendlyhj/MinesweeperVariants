#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# @Time    : 2025/06/15 11:59
# @Author  : Wu_RH
# @FileName: 3D1T'.py

"""
[3D1T']必三连: 雷必然处在横竖对角构成三连
"""

from .. import Abstract3DMinesRule
from abs.board import AbstractBoard
from utils.solver import get_model
from utils.tool import get_logger


class Rule3D1Tp(Abstract3DMinesRule):
    name = ["3D1T'", "3DT'", "三维必三连"]
    doc = "雷必然处在横竖对角构成三连"
    subrules = [
        [True, "[3D1T']雷必三连"]
    ]

    def create_constraints(self, board: 'AbstractBoard'):
        if not self.subrules[0][0]:
            return

        model = get_model()
        logger = get_logger()

        # 初始化位置覆盖字典
        position_coverage = {pos: [] for pos, _ in board()}

        # 遍历棋盘上的每个位置
        for pos, _ in board():
            # 生成26个三维方向 (dx, dy, dz)，排除(0,0,0)
            directions = []
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    for dz in (-1, 0, 1):
                        if dx == 0 and dy == 0 and dz == 0:
                            continue
                        directions.append((dx, dy, dz))

            for dx, dy, dz in directions:
                positions = [pos]  # 起始位置

                # 计算偏移位置1：水平移动 + 垂直移动
                p1 = pos.shift(dx, dy)  # 水平移动
                if p1 is not None:
                    if dz == 1:
                        p1 = self.up(board, p1, 1)  # 向上移动
                    elif dz == -1:
                        p1 = self.down(board, p1, 1)  # 向下移动
                positions.append(p1)

                # 计算偏移位置2：继续同方向移动
                p2 = None
                if p1 is not None:
                    p2 = p1.shift(dx, dy)  # 水平移动
                    if p2 is not None:
                        if dz == 1:
                            p2 = self.up(board, p2, 1)  # 向上移动
                        elif dz == -1:
                            p2 = self.down(board, p2, 1)  # 向下移动
                positions.append(p2)

                # 检查所有位置是否有效
                if not all(p is not None and board.is_valid(p) for p in positions):
                    continue  # 跳过无效位置

                # 获取位置对应的变量
                vars = [board.get_variable(p) for p in positions]

                # 创建三连组变量：当且仅当三个位置都是雷时为真
                b = model.NewBoolVar(f"triple_{pos}_{dx}_{dy}_{dz}")
                model.AddBoolAnd(vars).OnlyEnforceIf(b)
                model.AddBoolOr([v.Not() for v in vars]).OnlyEnforceIf(b.Not())

                # 记录此三连组覆盖的所有位置
                for p in positions:
                    position_coverage[p].append(b)

        # 只对雷位置添加约束：必须属于至少一个三连组
        for pos, var in board(mode="variable"):
            coverage_list = position_coverage.get(pos, [])

            if coverage_list:  # 确保该位置有三连组覆盖
                # 雷 => 至少属于一个三连组
                model.AddBoolOr(coverage_list).OnlyEnforceIf(var)
                logger.debug(f"Pos {pos}:雷必须属于{len(coverage_list)}个三连组之一")
            else:
                # 无三连组覆盖的位置不能是雷
                model.Add(var == 0)
                logger.warning(f"位置{pos}无三连组覆盖，强制为非雷")

    def check(self, board: 'AbstractBoard') -> bool:
        pass

    @classmethod
    def method_choose(cls) -> int:
        return 1
