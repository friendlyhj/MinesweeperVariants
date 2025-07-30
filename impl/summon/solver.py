#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Time    : 2025/06/07 19:40
# @Author  : Wu_RH
# @FileName: solver.py
import math
import os
from pathlib import Path
from typing import Union

import yaml
from ortools.sat.python import cp_model

from abs.Mrule import AbstractMinesClueRule
from abs.Rrule import AbstractClueRule
from abs.board import AbstractBoard
from abs.Lrule import MinesRules, Rule0R

from impl.impl_obj import ModelGenerateError

from utils.impl_obj import get_total
from utils.impl_obj import MINES_TAG, VALUE_QUESS
from utils.solver import reset_model
from utils.tool import get_logger, get_random

# ==== 获取默认值 ====
default_path = Path("config/default.yaml")
CONFIG = {}
if default_path.exists():
    with open(default_path, "r", encoding="utf-8") as f:
        CONFIG = yaml.safe_load(f)


class SolutionCollector(cp_model.CpSolverSolutionCallback):
    def __init__(self, board: "AbstractBoard",
                 mines_rules: "MinesRules"):
        super().__init__()
        self.valid_solution_count = 0  # 有效解计数
        self.mines_rules = mines_rules
        self.board = board

    def check_solution(self, board):
        for _, obj in board("C"):
            if obj.method_choose() & 5:
                continue
            if not obj.check(board):
                return False
        for rule in self.mines_rules.rules:
            if rule.method_choose() & 1:
                continue
            if rule.check(board):
                continue
            return False
        return True

    def on_solution_callback(self):
        _board = self.board.clone()
        for pos, _ in _board("N"):
            if self.Value(_board.get_variable(pos)):
                _board.set_value(pos, MINES_TAG)
            else:
                _board.set_value(pos, VALUE_QUESS)

        if self.check_solution(_board):
            self.valid_solution_count += 1
            if self.valid_solution_count > 1:
                self.StopSearch()  # 立即停止搜索


def get_solver(b: bool):
    solver = cp_model.CpSolver()
    solver.parameters.random_seed = 0
    solver.parameters.randomize_search = False  # 禁用启发式随机化
    solver.parameters.search_branching = cp_model.FIXED_SEARCH  # 按变量添加顺序搜索
    solver.parameters.cp_model_presolve = False  # 禁用 presolve（避免内部变量简化）
    solver.parameters.linearization_level = 0  # 禁用线性化（可能引入不可控启发）
    solver.parameters.num_search_workers = 1  # 禁用并行（确保搜索路径固定）
    solver.parameters.use_optional_variables = False  # 固定变量使用路径
    if CONFIG["timeout"] > 0:
        solver.parameters.max_time_in_seconds = CONFIG["timeout"]    # 时间限制
    # solver.parameters.enumerate_all_solutions = b
    return solver


def solver_by_csp(
        mines_rules: MinesRules,
        clue_rule: Union[AbstractClueRule, None],
        mines_clue_rule: Union[AbstractMinesClueRule, None],
        board: AbstractBoard,
        drop_r=False,
        bool_mode=False,
        answer_board=None
) -> int:
    """
    返回int 0表示无解 1表示唯一解 2表示多解
    """
    # -*- csp推导 -*- #
    logger = get_logger()
    logger.trace("构建新模型")
    model = reset_model()
    board.clear_variable()

    should_check = False

    # 1.获取所有的右线线索约束
    if clue_rule:
        should_check = (not clue_rule.create_constraints(board)) or should_check

    if mines_clue_rule:
        should_check = (not mines_clue_rule.create_constraints(board)) or should_check

    # 2.获取所有左线约束
    for rule in mines_rules.rules:
        if rule.method_choose() & 1:
            if drop_r and isinstance(rule, Rule0R):
                continue
            rule.create_constraints(board)
        else:
            should_check = True

    # 3.获取所有变量并赋值已解完的部分
    for key in board.get_board_keys():
        for _, var in board("C", mode="variable", key=key):
            model.Add(var == 0)
            logger.trace(f"var: {var} == 0")
        for _, var in board("F", mode="variable", key=key):
            model.Add(var == 1)
            logger.trace(f"var: {var} == 1")

    # 4.获取求解器并推导

    logger.trace("求解器输入:\n" + board.show_board())
    solver = get_solver(False)

    if answer_board is not None and not should_check:
        current_solution = []
        logger.trace("设置预设不同值")
        for key in board.get_interactive_keys():
            for pos, _ in board("N", key=key):
                value = 1 if answer_board.get_type(pos) == "F" else 0
                val = board.get_variable(pos)
                tmp = model.NewBoolVar(f"answer_tmp{pos}")
                current_solution.append(tmp)
                logger.trace(f"[{pos}]{val} != {value} ({answer_board.get_type(pos)})")
                model.Add(val != value).OnlyEnforceIf(tmp)
        model.AddBoolOr(current_solution)  # 新增排除当前解约束（至少有一个变量取反）

        status2 = solver.Solve(model)
        if status2 == cp_model.FEASIBLE or status2 == cp_model.OPTIMAL:
            logger.trace(f"求解器多解")
            return 2
        return 1

    if should_check:
        collector = SolutionCollector(board, mines_rules)
        status = solver.Solve(model, collector)
    else:
        collector = None
        status = solver.Solve(model)

    # 5.检查是否无解或者多解
    if status == cp_model.INFEASIBLE:
        logger.trace("求解器无解")
        return 0

    if status == cp_model.UNKNOWN:
        logger.trace("求解器遇到未知问题")
        return 0

    if status == cp_model.MODEL_INVALID:
        # 这个bug太玄乎了 修不好直接爆了
        # 关键他重新跑一遍就正常了 我没法debug
        logger.trace("\n" + board.show_board())
        logger.trace("求解器模型构建出现错误")

        # 输出状态码名称
        logger.trace(f"Solver status: {solver.StatusName(status)}")

        # 输出求解统计信息
        logger.trace(f"Num conflicts: {solver.NumConflicts()}")
        logger.trace(f"Num branches: {solver.NumBranches()}")
        logger.trace(f"Wall time (s): {solver.WallTime()}")

        for key in board.get_board_keys():
            logger.trace(f"board key: {key}")
            logger.trace("varlist:{}".format([var for _, var in board(mode="variable", key=key)]))
            logger.trace("obj:{}".format([var for _, var in board(mode="object", key=key)]))
            logger.trace("type:{}".format([var for _, var in board(mode="type", key=key)]))
            logger.trace("dye:{}".format([var for _, var in board(mode="dye", key=key)]))

        raise ModelGenerateError("model Error")

    if logger.print_level <= logger.TRACE:
        if not os.path.exists(CONFIG["output_path"]):
            os.makedirs(CONFIG["output_path"])
        model.ExportToFile("log/model.txt")

    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        logger.trace(f"求解器status:{status}")
        return 0

    if bool_mode:
        # 如果打开 那么就将状态压缩至 有解/无解
        return 1

    if should_check:
        if collector.valid_solution_count > 1:
            logger.trace(f"求解器多解")
            return 2
    else:
        current_solution = []
        for key in board.get_interactive_keys():
            for pos, _ in board("N", key=key):
                var = board.get_variable(pos)
                val = solver.Value(var)
                if val == 1:
                    current_solution.append(var.Not())  # 这个变量不能为1，取反
                else:
                    current_solution.append(var)  # 这个变量不能为0，保持原变量

        model.AddBoolOr(current_solution)  # 新增排除当前解约束（至少有一个变量取反）

        status2 = solver.Solve(model)
        if status2 == cp_model.FEASIBLE or status2 == cp_model.OPTIMAL:
            logger.trace(f"求解器多解")
            return 2
    return 1
