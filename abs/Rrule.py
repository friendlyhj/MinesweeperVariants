#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# @Time    : 2025/06/03 18:38
# @Author  : Wu_RH
# @FileName: Rrule.py

from abc import abstractmethod
from typing import TYPE_CHECKING, List, Dict

from abs.rule import AbstractRule, AbstractValue
from utils.image_create import get_text, get_image, get_dummy, get_col

if TYPE_CHECKING:
    from abs.board import AbstractBoard, AbstractPosition


class AbstractClueRule(AbstractRule):
    """
    数字线索规则
    """

    @abstractmethod
    def fill(self, board: 'AbstractBoard') -> 'AbstractBoard':
        """
        填充所有None为规则线索对象
        :param board: 题板
        :return: 题板
        """
        ...

    @abstractmethod
    def clue_class(self):
        """
        返回规则对应的Value线索类
        """
        ...

    def create_constraints(self, board: 'AbstractBoard') -> bool:
        """
        默认直接遍历板中的所有线索添加约束函数
        :param board: 输入题板
        :return: 需要返回时候包含全部线索约束 True已经包含全部约束 False未包含全部约束
        """
        strict = True
        for key in board.get_board_keys():
            for _, obj in board("C", key=key):
                if not isinstance(obj, self.clue_class()):
                    continue
                if obj.method_choose() & 1:
                    obj.create_constraints(board)
                else:
                    strict = False
        return strict


class AbstractClueValue(AbstractValue):
    """
    线索格数字对象类
    """

    @abstractmethod
    def __init__(self, pos: 'AbstractPosition', code: bytes = b''):
        """
        获取code并初始化 输入值为code函数的返回值
        :param code: 实例对象代码
        """
        self.pos = pos

    def __repr__(self) -> str:
        """
        当前值在展示时候的显示字符串
        :return: 显示的字符串
        """
        return ""

    def compose(self, board) -> List[Dict]:
        """
        返回一个可渲染对象列表
        默认使用__repr__
        """
        return [get_col(
            get_dummy(height=0.175),
            get_text(self.__repr__()),
            get_dummy(height=0.175),
        )]


# --------实例类-------- #


class ValueQuess(AbstractClueValue):
    """
    问号类(线索非雷)
    """

    def __init__(self, pos: 'AbstractPosition', code: bytes = b''):
        super().__init__(pos)

    def method_choose(self) -> int:
        return 1

    def __repr__(self):
        return "?"

    @classmethod
    def type(cls) -> bytes:
        return b"?"

    def code(self) -> bytes:
        return b""


class ValueCross(AbstractClueValue):
    """
    副板的叉号
    """

    def __init__(self, pos: 'AbstractPosition', code: bytes = b''):
        super().__init__(pos)

    def method_choose(self) -> int:
        return 1

    def __repr__(self):
        return "X"

    def compose(self, board) -> List[Dict]:
        return [get_image("Cross")]

    @classmethod
    def type(cls) -> bytes:
        return b"X"

    def code(self) -> bytes:
        return b""
