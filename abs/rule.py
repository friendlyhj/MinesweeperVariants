#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# @Time    : 2025/06/07 13:39
# @Author  : Wu_RH
# @FileName: rule.py

from abc import ABC, abstractmethod
from typing import List, Union, TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from abs.board import AbstractBoard


class AbstractRule(ABC):
    # 规则名称
    name: str

    """
    subrules: 如果该规则需要使用线索数检查的话 就必须实现该属性
        列表内为一个二元列表 其二元列表第一个为一个bool值用来表示该规则的子规则约束模块的开关
        并对应到check和create_constraints这个两个函数 bool:True表示开启 False表示关闭
        其二元列表的第二个是该子规则模块的描述 用来在线索的时候返回
    """
    subrules: list[list[bool, str]] = []

    def __init__(self, board: "AbstractBoard" = None, data=None) -> None:
        ...

    def init_clear(self, board: 'AbstractBoard'):
        """
        在题板生成阶段调用，用于删除题板上必须被清除的线索或对象。
        例如纸笔题目中，某些规则可能要求特定位置不能出现雷或线索。
        """

    def suggest_total(self, info: dict):
        """
        :param info:
            `info (dict)`：上下文信息字典，包含以下关键字段：
                * `size (dict[str, tuple[int, int]])` 其键为题板的字符串索引 值为size元组
                * `interactive (list[str])`：题板交互权，列表内为题板索引，所有键均为允许求解器主动交互。
                * `hard_fns (list[Callable[[CpModel, IntVar], None]])`：硬约束函数列表。
                    * 规则通过定义函数的形式添加硬约束（如调用 `model.Add(...)`），
                    * 需要将该函数追加到此列表，生成器后续会统一调用执行，确保所有硬约束生效。
                    * 函数签名应为 `(model: CpModel, total: IntVar) -> None`，不返回值。
                * `soft_fn (Callable[[int, int], None])`：软约束函数。
                    * 签名为 `(target_value: int, priority: int)`，用于表示软约束的目标值和优先级。
                    * 规则调用此函数以注册软约束，具体添加到模型的逻辑由生成器统一处理。
                    * 规则只需传入期望的目标值与优先级，无需关心底层实现和返回值。
        规则在生成阶段调用，向`info`添加硬约束，并通过调用 `info` 根键的软约束函数实现软约束。
        """


class AbstractValue(ABC):
    def __repr__(self):
        ...

    def compose(self, board: 'AbstractBoard') -> List[Dict]:
        """
        返回一个可渲染对象列表
        默认使用__repr__
        """
        ...

    @classmethod
    @abstractmethod
    def method_choose(cls) -> int:
        """
        需要返回选择哪个方法进行遍历
        使用1 2表示的1-7的代码选择
        推荐优先实现约束生成
        1: create_constraints方法 构建约束列表
        2: check方法 检查题板是否符合规则
        """

    def invalid(self, board: 'AbstractBoard') -> bool:
        """
        返回该线索对于输入题板是否无用
        :return: True:已经无效 False:仍然有效
        """
        return False

    @classmethod
    @abstractmethod
    def type(cls) -> bytes:
        """
        返回当前规则的类型 必须所有规则返回是不同的
        如0V返回0V
        :return:
        """
        ...

    def deduce_cells(self, board: 'AbstractBoard') -> bool:
        """
        快速检查当前题板并修改可以直接得出结论的地方
        :param board: 输入题板
        :return: 是否修改了 True 修改 False 未修改
        """
        return False

    def code(self) -> bytes:
        """
        返回为当前对象的格式化值 返回为str
        返回值会被初始化的时候使用
        返回值不可包含空格
        :return:
        """
        return b''

    def create_constraints(self, board: 'AbstractBoard'):
        """
        基于当前线索对象向 CP-SAT 模型添加约束。
        此方法根据当前线索的位置与规则，分析题板上的变量布局，并在模型中添加等价的逻辑约束表达式。
        所有变量必须来源于board中get_variable(pos)返回的变量
        model可以通过utils.solver下的函数get_model()获取
        如果必然无法用约束表达的规则应通过 check()/exhaustive() 实现。
        :param      board: 输入的题板对象
        """
        ...

    def check(self, board: 'AbstractBoard') -> bool:
        """
        检查当前题板的该线索是否严格非法
        如果存在其他合法但是未赋值的情况则返回合法
        :param board: 题板
        :return: True合法或未知 False严格非法
        """
        return True
