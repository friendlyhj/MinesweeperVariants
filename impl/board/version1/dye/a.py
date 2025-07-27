#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# 
# @Time    : 2025/06/11 14:03
# @Author  : xxx
# @FileName: a.py

from . import AbstractDye
from abs.board import AbstractBoard


class DyeA(AbstractDye):
    name = "a"

    def dye(self, board: "AbstractBoard"):
        pos = board.boundary()
        for _pos in board.get_row_pos(pos):
            for __pos in board.get_col_pos(_pos):
                board.set_dyed(__pos, True)
