#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# 
# @Time    : 2025/06/10 09:52
# @Author  : xxx
# @FileName: c.py

from . import AbstractDye


class DyeC(AbstractDye):
    name = "c"

    def dye(self, board, board_key: str):
        dye = True
        pos = board.boundary(key=board_key)
        for _pos in (line := board.get_row_pos(pos)):
            for __pos in board.get_col_pos(_pos):
                board.set_dyed(__pos, dye := not dye)
            if not len(line) % 2:
                dye = not dye
