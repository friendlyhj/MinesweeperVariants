#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Time    : 2025/06/07 19:40
# @Author  : Wu_RH
# @FileName: solver.py
import math
import os
from pathlib import Path
import yaml
from abs.rule import AbstractRule, AbstractValue
from ortools.sat.python import cp_model
from collections import defaultdict
from typing import Dict, List, Tuple, Union, Optional, Any

from utils.tool import get_logger

from abs.Mrule import AbstractMinesClueRule
from abs.Rrule import AbstractClueRule
from abs.board import AbstractBoard, AbstractPosition
from abs.Lrule import MinesRules, Rule0R
from impl.impl_obj import ModelGenerateError


# ==== 获取默认值 ====
default_path = Path("config/default.yaml")
CONFIG = {}
if default_path.exists():
    with open(default_path, "r", encoding="utf-8") as f:
        CONFIG = yaml.safe_load(f)


def get_solver(b: bool):
    solver = cp_model.CpSolver()
    solver.parameters.random_seed = 42  # 启发式多样性
    solver.parameters.num_search_workers = CONFIG["workes_number"]  # 多线程并行搜索
    solver.parameters.search_branching = cp_model.AUTOMATIC_SEARCH
    solver.parameters.linearization_level = 2  # 启用线性化加速
    solver.parameters.cp_model_presolve = b
    solver.parameters.use_optional_variables = True
    solver.parameters.randomize_search = True
    if CONFIG["timeout"] > 0:
        solver.parameters.max_time_in_seconds = CONFIG["timeout"]  # 时间限制
    return solver


class Switch:

    def __init__(self):
        # 变量索引到HintFlag的映射
        self.index_to_hint: Dict[int, Tuple[str, int]] = {}

        # 名称到当前索引计数器的映射
        self.name_counter: Dict[str, int] = defaultdict(int)

        # 存储所有创建的变量
        self.all_vars: List[cp_model.IntVar] = []

        # HintFlag到变量索引列表的映射（用于重映射）
        self.hint_to_indices: Dict[Tuple[str, int], List[int]] = defaultdict(list)

    def to_str(self, obj: Union[AbstractRule, AbstractValue, AbstractPosition, str]):
        if isinstance(obj, AbstractRule):
            name = f"RULE|{obj.name[0]}"
        elif (
            isinstance(obj, AbstractPosition) or
            isinstance(obj, AbstractValue)
        ):
            if isinstance(obj, AbstractValue):
                pos = obj.pos
            else:
                pos = obj
            if pos is None:
                raise ValueError("pos cannot be None")
            pos = f"|{pos.x}|{pos.y}|{pos.board_key}"
            name = "POS" + pos
        elif isinstance(obj, str):
            name = obj
        else:
            raise ValueError("obj must be an Rule or Value")
        return name

    def get(
            self,
            model: cp_model.CpModel,
            obj: Union[AbstractRule, AbstractValue, AbstractPosition, str],
            hint_flag: Optional[Tuple[str, int]] = None
    ) -> cp_model.IntVar:
        """
        创建或获取一个开关变量

        参数:
        name: 变量基础名称
        hint_flag: 可选，指定要映射到的HintFlag (name, index)

        返回:
        创建的布尔变量
        """
        name = self.to_str(obj)
        # 自动生成或使用指定的HintFlag
        if hint_flag is None:
            # 获取当前索引并递增
            current_index = self.name_counter[name]
            self.name_counter[name] += 1
            hint_flag = (name, current_index)
        else:
            # 使用指定的HintFlag
            name, index = hint_flag
            # 更新名称计数器以确保后续索引正确
            self.name_counter[name] = max(self.name_counter[name], index + 1)

        # 创建新变量
        var = model.NewBoolVar(f"{name}_{hint_flag[1]}")
        var_index = var.Index()

        # 存储映射关系
        self.index_to_hint[var_index] = hint_flag
        self.hint_to_indices[hint_flag].append(var_index)
        self.all_vars.append(var)

        return var

    def remap_index(self, index: int, target_hint: Tuple[Any, int]):
        """
        将现有变量索引重映射到另一个HintFlag

        参数:
        index: 要重映射的变量索引
        target_hint: 要映射到的目标HintFlag (name, index)
        """
        if index not in self.index_to_hint:
            raise ValueError(f"Index {index} not found in switch")

        # 转换target_hint为字符串形式
        obj, idx_val = target_hint
        name_str = self.to_str(obj)
        target_hint_str = (name_str, idx_val)

        # 移除旧映射
        old_hint = self.index_to_hint[index]
        if old_hint in self.hint_to_indices:
            self.hint_to_indices[old_hint].remove(index)
            if not self.hint_to_indices[old_hint]:
                del self.hint_to_indices[old_hint]

        # 添加新映射
        self.index_to_hint[index] = target_hint_str
        self.hint_to_indices[target_hint_str].append(index)

        # 更新名称计数器
        self.name_counter[name_str] = max(self.name_counter[name_str], idx_val + 1)

    def get_hint_by_index(self, index: int) -> Tuple[str, int]:
        """
        根据变量索引获取对应的HintFlag

        参数:
        index: 变量索引

        返回:
        (name, index) 元组
        """
        if index not in self.index_to_hint:
            raise ValueError(f"Index {index} not found in switch")
        return self.index_to_hint[index]

    def get_all_vars(self) -> List[cp_model.IntVar]:
        """
        获取所有创建的变量

        返回:
        变量列表
        """
        return self.all_vars

    def get_indices_by_hint(self, hint: Tuple[str, int]) -> List[int]:
        """
        根据HintFlag获取所有映射到它的变量索引

        参数:
        hint: (name, index) 元组

        返回:
        变量索引列表
        """
        return self.hint_to_indices.get(hint, [])


def solver_by_csp(
        mines_rules: MinesRules,
        clue_rule: Union[AbstractClueRule, None],
        mines_clue_rule: Union[AbstractMinesClueRule, None],
        board: AbstractBoard,
        drop_r=False,
        bool_mode=False,
        answer_board=None,
        model=None
) -> int:
    """
    返回int 0表示无解 1表示唯一解 2表示多解
    """
    # -*- csp推导 -*- #
    logger = get_logger()

    if model is None:
        logger.trace("求解器输入:\n" + board.show_board())
        logger.trace("构建新模型")
        board = board.clone()
        board.clear_variable()
        model = board.get_model()
        switch = Switch()

        # 2.获取所有规则约束
        for rule in (
                mines_rules.rules +
                [clue_rule, mines_clue_rule]
        ):
            if rule is None:
                continue
            if drop_r and isinstance(rule, Rule0R):
                continue
            rule: AbstractRule
            rule.create_constraints(board, switch)

        for key in board.get_board_keys():
            for pos, obj in board(key=key):
                if obj is None:
                    continue
                obj: AbstractValue
                obj.create_constraints(board, switch)

        # 3.获取所有变量并赋值已解完的部分
        for key in board.get_board_keys():
            for _, var in board("C", mode="variable", key=key):
                model.Add(var == 0)
                logger.trace(f"var: {var} == 0")
            for _, var in board("F", mode="variable", key=key):
                model.Add(var == 1)
                logger.trace(f"var: {var} == 1")

        model: cp_model.CpModel
        # model.AddAssumptions(switch.var_map.values())
        for switch_var in switch.get_all_vars():
            model.Add(switch_var == 1)

    # 4.获取求解器并推导
    solver = get_solver(True)

    if answer_board is not None:
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
            logger.trace("varlist:{}".format([(var.index, var) for _, var in board(mode="variable", key=key)]))
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


def hint_by_csp(
        board: AbstractBoard,
        answer_board: AbstractBoard,
        switch: Switch,
        pos: AbstractPosition,
):
    if board[pos] is not None:
        return None
    model = board.get_model().clone()
    model: cp_model.CpModel

    model.AddAssumptions(switch.get_all_vars())

    target_var = board.get_variable(pos)
    model.Add(target_var == (0 if answer_board.get_type(pos) == "F" else 1))

    solver = get_solver(True)
    state = solver.Solve(model)

    if state != cp_model.INFEASIBLE:
        return None

    hint = solver.SufficientAssumptionsForInfeasibility()
    hint = [i if i > -1 else -i - 1 for i in hint]
    # print(hint)
    hint = [switch.get_hint_by_index(i) for i in hint]

    return hint


def deduced_by_csp(
        board: AbstractBoard,
        answer_board: AbstractBoard,
        pos: AbstractPosition,
):
    """
    检查是否无解
    """
    if board[pos] is not None:
        return None
    model = board.get_model().clone()
    model: cp_model.CpModel

    target_var = board.get_variable(pos)
    model.Add(target_var == (0 if answer_board.get_type(pos) == "F" else 1))

    solver = get_solver(False)
    state = solver.Solve(model)

    if state == cp_model.INFEASIBLE:
        return True
    return False
