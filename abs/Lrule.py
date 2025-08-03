#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# @Time    : 2025/06/03 18:38
# @Author  : Wu_RH
# @FileName: Lrule.py

from typing import TYPE_CHECKING
from abc import abstractmethod

from utils.impl_obj import get_total
from utils.solver import get_model
from utils.tool import get_logger
from abs.rule import AbstractRule

if TYPE_CHECKING:
    from .board import AbstractBoard


class AbstractMinesRule(AbstractRule):
    """
    雷布局规则
    """
    name: str = ""
    """
    name: 需要命名为字符串常量 字符串为规则的名称 如0R被命名为"0R"
    """

    def create_constraints(self, board: 'AbstractBoard'):
        """
        基于当前线索对象向 CP-SAT 模型添加约束。
        此方法根据当前规则，分析题板上的变量布局，并在模型中添加等价的逻辑约束表达式。
        所有变量必须来源于board中get_variable(pos)返回的变量
        model可以通过utils.solver下的函数get_model()获取
        如果必然无法用约束表达的规则应通过 check() 实现。
        :param board: 题板输入
        """
        ...

    def check(self, board: 'AbstractBoard') -> bool:
        """
        严格穷举来检查当前题板是否符合布局规则
        :param board: 题板输入
        :return: True合法 False非法
        """
        return True


# --------实例类-------- #


class MinesRules:
    """
    雷布局规则组
    """
    def __init__(self, rules: list['AbstractMinesRule'] = None):
        """
        雷布局规则组初始化
        :param rules:
        """
        if rules is None:
            rules = []
        self.rules = rules
        self.logger = get_logger()

    def append(self, rule: 'AbstractMinesRule'):
        """
        将规则加入组
        :param rule:
        :return:
        """
        self.rules.append(rule)

    def check(self, board: 'AbstractBoard'):
        """
        检查当前布局是否合法
        :param board:   题板
        :return: True 检查通过 False 检查未通过
        """
        if board is None:
            return False
        for i in self.rules:
            if not i.check(board):
                return False
        return True


class Rule0R(AbstractMinesRule):
    name = "0R"
    subrules = [[True, "R"]]
    """
    总雷数规则
    """
    def create_constraints(self, board: 'AbstractBoard'):
        if not self.subrules[0][0]:
            return
        model = get_model()
        all_variable = [board.get_variable(pos) for pos, _ in board()]
        model.Add(sum(all_variable) == get_total())
        get_logger().trace(f"[R]: model add {all_variable} == {get_total()}")

    def check(self, board: 'AbstractBoard') -> bool:
        type_list = [board.get_type(pos) for pos, _ in board()]
        return (f_num := type_list.count("F")) <= get_total() <= f_num + type_list.count("N")

    @classmethod
    def method_choose(cls) -> int:
        return 1

    def suggest_total(self, info: dict):
        ub = 0
        for key in info["interactive"]:
            size = info["size"][key]
            ub += size[0] * size[1]
        info["soft_fn"](ub * 0.4, -1)
