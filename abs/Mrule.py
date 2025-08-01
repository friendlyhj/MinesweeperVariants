#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# @Time    : 2025/06/03 18:38
# @Author  : Wu_RH
# @FileName: Mrule.py

# 雷线索由于未实装 等待版本大更新

from typing import TYPE_CHECKING, List, Union, Dict
from abs.rule import AbstractRule, AbstractValue
from utils.image_create import get_image, get_col, get_dummy, get_text
from abc import abstractmethod, ABC

if TYPE_CHECKING:
    from .board import AbstractPosition, AbstractBoard


class AbstractMinesClueRule(AbstractRule):
    """
    雷线索规则
    """

    @abstractmethod
    def mines_class(self):
        """
        返回规则对应的Mines雷线索类
        """

    @abstractmethod
    def fill(self, board: 'AbstractBoard') -> 'AbstractBoard':
        """
        将在左线放置完成后调用
        需要将题板内的所有雷值赋值为线索
        :param board: 题板
        :return: 题板
        """

    def create_constraints(self, board: 'AbstractBoard') -> bool:
        """
        默认直接遍历板中的所有线索添加约束函数
        :param board: 输入题板
        :return: 需要返回时候包含全部线索约束 True已经包含全部约束 False未包含全部约束
        """
        strict = True
        for key in board.get_board_keys():
            for _, obj in board("F", key=key):
                if not isinstance(obj, self.mines_class()):
                    continue
                if obj.method_choose() & 1:
                    obj.create_constraints(board)
                else:
                    strict = False
        return strict


class AbstractMinesValue(AbstractValue, ABC):
    pos: 'AbstractPosition'

    @abstractmethod
    def __init__(self, pos: 'AbstractPosition', code: bytes = None):
        self.pos = pos

    def __repr__(self):
        """
        当前值在展示时候的显示字符串
        :return: 显示的字符串
        """
        return "_F_"

    def compose(self, board: 'AbstractBoard') -> List[Dict]:
        """
        返回一个可渲染对象列表
        默认使用__repr__
        """
        return [get_col(
            get_dummy(height=0.175),
            get_text(self.__repr__(),
                     color=("#FFFF00", "#FF7F00")),
            get_dummy(height=0.175),
        )]


# --------实例类-------- #


class MinesTag(AbstractMinesValue):
    """
    雷标志类
    用于暂存表示为类
    """

    def __init__(self, pos: 'AbstractPosition', code: bytes = None):
        pass

    @classmethod
    def method_choose(cls) -> int:
        return 3

    def __repr__(self):
        return "雷"

    def compose(self, board) -> List[Dict]:
        return [get_image(
            "flag",
            cover_pos_label=False
        )]

    @classmethod
    def type(cls) -> bytes:
        return b"F"

    def code(self) -> bytes:
        return b""


class Rule0F(AbstractMinesClueRule):
    name = "_0F"

    def init_clear(self, board: 'AbstractBoard'):
        for key in board.get_board_keys():
            if not board.get_config(key, "interactive"):
                continue
            for pos, _ in board("F", key= key):
                board.set_value(pos, None)

    def fill(self, board: 'AbstractBoard') -> 'AbstractBoard':
        return board

    def mines_class(self):
        return MinesTag


class ValueCircle(AbstractMinesValue):
    def __init__(self, pos: 'AbstractPosition', code: bytes = None):
        pass

    @classmethod
    def method_choose(cls) -> int:
        return 3

    def __repr__(self):
        return "O"

    def compose(self, board) -> List[Dict]:
        return [get_image("circle", cover_pos_label=False)]

    def code(self) -> bytes:
        return b""

    @classmethod
    def type(cls) -> bytes:
        return b"O"


