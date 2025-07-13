#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# 
# @Time    : 2025/06/10 09:52
# @Author  : xxx
# @FileName: 3dc.py

from . import AbstractDye


class DyeC(AbstractDye):
    name = "3dc"

    def dye(self, board):
        dye = True
        for key in board.get_interactive_keys():
            pos = board.boundary(key=key)
            for _pos in (line := board.get_row_pos(pos)):
                for __pos in board.get_col_pos(_pos):
                    board.set_dyed(__pos, dye := not dye)
                if not len(line) % 2:
                    dye = not dye
            if not len(line) % 2:
                dye = not dye
