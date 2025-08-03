#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# @Time    : 2025/07/03 00:27
# @Author  : Wu_RH
# @FileName: game.py
import threading
import time
from pathlib import Path
from typing import Union, Callable
import itertools as it

import yaml
from ortools.sat.python import cp_model

from abs.Lrule import Rule0R
from concurrent.futures import ThreadPoolExecutor, as_completed
from abs.Rrule import AbstractClueValue
from abs.board import AbstractBoard
from abs.board import AbstractPosition
from impl.summon import Summon
from impl.summon.solver import solver_by_csp, hint_by_csp, Switch
from utils.impl_obj import MINES_TAG, VALUE_QUESS, POSITION_TAG
from utils.tool import get_logger, get_random

# ==== 获取默认值 ====
default_path = Path("config/default.yaml")
CONFIG = {}
if default_path.exists():
    with open(default_path, "r", encoding="utf-8") as f:
        CONFIG = yaml.safe_load(f)

NORMAL = 0  # 普通模式
EXPERT = 1  # 专家模式
ULTIMATE = 2  # 终极模式
PUZZLE = 3  # 纸笔模式(用于调试)

ULTIMATE_A = 1
ULTIMATE_F = 2
ULTIMATE_S = 4
ULTIMATE_R = 8


class ValueAsterisk(AbstractClueValue):
    def __init__(self, pos: 'AbstractPosition', code: bytes = b''):
        pass

    def __repr__(self) -> str:
        return "*"

    @classmethod
    def type(cls) -> bytes:
        return b"*"

    def code(self) -> bytes:
        return b""

    @classmethod
    def method_choose(cls) -> int:
        return 3


VALUE_TAG = ValueAsterisk(POSITION_TAG)


class GameSession:
    def __init__(self, summon: Summon = None,
                 mode=NORMAL, drop_r=False,
                 ultimate_mode=ULTIMATE_A | ULTIMATE_F | ULTIMATE_S,
                 ):
        self.logger = get_logger()
        self.summon = summon
        self.drop_r = drop_r
        if mode == ULTIMATE:
            if ultimate_mode & ULTIMATE_R:
                self.drop_r = False
            else:
                self.drop_r = True

        self.answer_board = None
        self.board = None

        self.mode = mode
        self.ultimate_mode = ultimate_mode

        self.last_hint = [None, []]

    def solve_current_board(
            self, board_state,
            drop_r: bool,
            bool_mode: bool = True,
            answer_board: AbstractBoard = None,
            model: cp_model.CpModel = None
    ) -> int:
        # CSP 解算器包装函数
        e = None
        for _ in range(5):
            try:
                return solver_by_csp(
                    self.summon.mines_rules,
                    self.summon.clue_rule,
                    self.summon.mines_clue_rule,
                    board_state,
                    drop_r=drop_r,
                    bool_mode=bool_mode,
                    answer_board=answer_board,
                    model=model
                )
            except Exception as e:
                print(e)
        raise e

    def create_board(self) -> "AbstractBoard":
        """
        一层具象
        终极模式的规则是 直到推无可推再给下一步线索 如果倒过来想呢
        倒过来就是删无可删 再重头删一遍

        具体操作
        初始化: 将所有雷设置为None
        第一步: 将整个版面的线索都替换为雷试下能不能无解 如果无解代表矛盾
        第二步: 现在整个题板都遍历完了一遍 看起来已经是删无可删了 那么就
        """
        board = self.answer_board.clone()
        for pos, _ in board("F"):
            board.set_value(pos, None)
        clues = [i for i in board("CF")]
        print(board.show_board(), clues)
        get_random().shuffle(clues)
        r_flag = True
        while clues:
            if r_flag and self.drop_r:
                r_flag = solver_by_csp(
                    self.summon.mines_rules,
                    self.summon.clue_rule,
                    self.summon.mines_clue_rule,
                    board.clone(),
                    answer_board=self.answer_board,
                    drop_r=not r_flag
                ) == 1
            while True:
                if not clues:
                    break
                pos, clue = clues.pop()
                if board.get_type(pos) == "C":
                    board.set_value(pos, MINES_TAG)
                elif board.get_type(pos) == "F":
                    board.set_value(pos, VALUE_TAG)
                if solver_by_csp(
                        self.summon.mines_rules,
                        self.summon.clue_rule,
                        self.summon.mines_clue_rule,
                        board.clone(), drop_r=not r_flag) == 0:
                    board.set_value(pos, None)
                    break
                board.set_value(pos, clue)
        self.board = board
        return board

    def chord_clue(self, clue_pos: AbstractPosition) -> list[AbstractPosition]:
        # 看最后一次提示有没有包含该格的单线索
        VALUE = self.board.get_config(clue_pos.board_key, "VALUE")
        MINES = self.board.get_config(clue_pos.board_key, "MINES")
        if self.board[clue_pos] in [VALUE, MINES, VALUE_TAG, None]:
            return []
        for pos, positions in self.last_hint[1]:
            if pos != [clue_pos]:
                continue
            if any(self.board.get_type(_pos) != "N" for _pos in positions):
                break
            return positions
        if self.board == self.last_hint[0]:
            return []
        obj = self.board.get_value(clue_pos)
        board: AbstractBoard = self.board.clone()
        chord_positions = []
        if obj.deduce_cells(board) is not None:
            for pos, obj in self.board():
                if (obj is None) and (board[pos] is not None):
                    chord_positions.append(pos)
            return chord_positions

        for pos, positions in self.hint().items():
            if pos != [clue_pos]:
                continue
            if any(self.board.get_type(_pos) != "N" for _pos in positions):
                break
            return positions

        self.logger.debug(f"chord pos: {clue_pos}, {self.board[clue_pos]}")

        return chord_positions

    def apply(self, pos: AbstractPosition, action: int) -> Union["AbstractBoard", None]:
        """
        :param pos: 交互位置
        :param action: 操作代码
            0: 左键点击/翻开/设置非雷
            1: 右键点击/标雷/设置必雷
        """
        global NORMAL, EXPERT, ULTIMATE, PUZZLE
        if self.mode == PUZZLE:
            if action == 1:
                value_tag = self.board.get_config(pos.board_key, "MINES")
                self.board.set_value(pos, value_tag)
            elif action == 0:
                value_tag = self.board.get_config(pos.board_key, "VALUE")
                self.board.set_value(pos, VALUE_TAG if value_tag == VALUE_QUESS else value_tag)
            return self.board
        if self.board.get_type(pos) != "N":
            # 点击了线索
            chord_positions = self.chord_clue(pos)
            if self.mode in [NORMAL, EXPERT]:
                # 普通和专家直接设置值
                for _pos in chord_positions:
                    self.board[_pos] = self.answer_board[_pos]
            elif self.mode in [ULTIMATE, PUZZLE]:
                # 如果是纸笔和专家就放标志
                for _pos in chord_positions:
                    if self.answer_board.get_type(_pos) == "F":
                        self.board[_pos] = MINES_TAG
                    elif self.answer_board.get_type(_pos) == "C":
                        self.board[_pos] = VALUE_TAG
        elif self.mode == NORMAL:
            # 普通模式
            if action and self.answer_board.get_type(pos) == "F":
                return None
            if not action and self.answer_board.get_type(pos) == "C":
                return None
            self.board[pos] = self.answer_board[pos]
        elif self.mode in [EXPERT, ULTIMATE, PUZZLE]:
            # 专家模式
            if pos not in self.deduced_values.keys():
                self.deduced()
            if pos not in self.deduced_values.keys():
                return None
            if action and self.board.type_value(self.deduced_values[pos]) == "C":
                return None
            if not action and self.board.type_value(self.deduced_values[pos]) == "F":
                return None
            if self.mode in [ULTIMATE, PUZZLE]:
                self.board[pos] = MINES_TAG if action else VALUE_TAG
            else:
                self.board[pos] = self.answer_board[pos]
        else:
            return None
        for pos, _ in self.board("CF"):
            if pos in self.deduced_values.keys():
                del self.deduced_values[pos]
        if (
                self.mode in [ULTIMATE, PUZZLE] and
                self.ultimate_mode & ULTIMATE_A
        ):
            print(self.drop_r)
            if not self.deduced():
                self.hint()
        return self.board

    def click(self, pos: "AbstractPosition") -> Union["AbstractBoard", None]:
        """
        翻开/点击 某个空白格
        :param pos: 翻开的位置
        """
        t = time.time()
        global NORMAL, EXPERT, ULTIMATE, PUZZLE
        if self.board.get_type(pos) != "N":
            # 点击了线索
            chord_positions = self.chord_clue(pos)
            if self.mode in [NORMAL, EXPERT]:
                # 普通和专家直接设置值
                for _pos in chord_positions:
                    self.board[_pos] = self.answer_board[_pos]
            elif self.mode in [ULTIMATE, PUZZLE]:
                # 如果是纸笔和专家就放标志
                for _pos in chord_positions:
                    if self.answer_board.get_type(_pos) == "F":
                        self.board[_pos] = MINES_TAG
                    elif self.answer_board.get_type(_pos) == "C":
                        self.board[_pos] = VALUE_TAG
        elif self.mode == NORMAL:
            # 普通模式
            if self.answer_board.get_type(pos) == "F":
                return None
            self.board[pos] = self.answer_board[pos]
        elif self.mode in [EXPERT, ULTIMATE, PUZZLE]:
            # 专家模式
            if pos not in self.deduced_values.keys():
                self.deduced()
            if pos not in self.deduced_values.keys():
                return None
            if self.board.type_value(self.deduced_values[pos]) == "C":
                return None
            if self.mode in [ULTIMATE, PUZZLE]:
                self.board[pos] = VALUE_TAG
            else:
                self.board[pos] = self.answer_board[pos]
        else:
            return None
        for pos, _ in self.board("CF"):
            if pos in self.deduced_values.keys():
                del self.deduced_values[pos]
        if (
                self.mode in [ULTIMATE, PUZZLE] and
                self.ultimate_mode & ULTIMATE_A
        ):
            print(self.drop_r)
            if not self.deduced():
                self.hint()
        print("click time: ", time.time() - t)
        return self.board

    def mark(self, pos: AbstractPosition) -> Union["AbstractBoard", None]:
        """
        右键标雷
        """
        global NORMAL, EXPERT, ULTIMATE, PUZZLE
        if self.board.get_type(pos) != "N":
            # 右键了线索
            chord_positions = self.chord_clue(pos)
            if self.mode in [NORMAL, EXPERT]:
                # 普通和专家直接设置值
                for _pos in chord_positions:
                    self.board[_pos] = self.answer_board[_pos]
            elif self.mode in [ULTIMATE, PUZZLE]:
                # 如果是纸笔和专家就放标志
                for _pos in chord_positions:
                    if self.answer_board.get_type(_pos) == "F":
                        self.board[_pos] = MINES_TAG
                    elif self.answer_board.get_type(_pos) == "C":
                        self.board[_pos] = VALUE_TAG
        elif self.mode == NORMAL:
            # 普通模式
            if self.answer_board.get_type(pos) == "C":
                return None
            self.board[pos] = self.answer_board[pos]
        elif self.mode in [EXPERT, ULTIMATE, PUZZLE]:
            # 专家模式
            if pos not in self.deduced_values.keys():
                self.deduced()
            if pos not in self.deduced_values.keys():
                return None
            if self.board.type_value(self.deduced_values[pos]) == "F":
                return None
            if self.mode in [ULTIMATE, PUZZLE]:
                self.board[pos] = MINES_TAG
            else:
                self.board[pos] = self.answer_board[pos]
        else:
            return None
        for pos, _ in self.board("CF"):
            if pos in self.deduced_values.keys():
                del self.deduced_values[pos]
        if (
                self.mode in [ULTIMATE, PUZZLE] and
                self.ultimate_mode & ULTIMATE_A
        ):
            if not self.deduced():
                self.hint()
        return self.board

    def step(self):
        # 没有可推格了
        flag = True
        for pos in self.deduced_values.keys():
            if self.answer_board.get_type(pos) == "C":
                flag = False
        if self.ultimate_mode & ULTIMATE_F:
            for pos in self.deduced_values.keys():
                if self.answer_board.get_type(pos) == "F":
                    flag = False
        if self.ultimate_mode & ULTIMATE_S:
            for pos in self.deduced_values.keys():
                self.board: AbstractBoard
                if pos in self.board.get_board_keys():
                    flag = False
        else:
            for pos in self.deduced_values.keys():
                self.board: AbstractBoard
                if pos in self.board.get_interactive_keys():
                    flag = False
        if flag:
            for pos, obj in self.board():
                if obj not in [VALUE_TAG, MINES_TAG]:
                    continue
                self.board[pos] = self.answer_board[pos]

    def deduced(self, r=False):
        """
        收集所有必然能推出的位置及其不可能的值
        """

        self.logger.trace("构建新模型")
        self.board.clear_variable()
        model = self.board.get_model()
        switch = Switch()

        all_rules = self.summon.mines_rules.rules

        # 2.获取所有规则约束
        for rule in all_rules:
            if rule is None:
                continue
            if self.drop_r and isinstance(rule, Rule0R):
                continue
            rule.create_constraints(self.board, switch)

        for key in self.board.get_board_keys():
            for pos, obj in self.board(key=key):
                if obj is None:
                    continue
                obj.create_constraints(self.board, switch)

        # 3.获取所有变量并赋值已解完的部分
        for key in self.board.get_board_keys():
            for _, var in self.board("C", mode="variable", key=key):
                model.Add(var == 0)
                self.logger.trace(f"var: {var} == 0")
            for _, var in self.board("F", mode="variable", key=key):
                model.Add(var == 1)
                self.logger.trace(f"var: {var} == 1")

        results = {}
        future_to_param = {}

        with ThreadPoolExecutor(max_workers=CONFIG["workes_number"]) as executor:
            # 提交任务
            for pos, _ in self.board("N"):
                fut = executor.submit(
                    self.solve_current_board,
                    self.board, self.drop_r,
                    True, None, model
                )
                future_to_param[fut] = pos  # 记录参数以便出错追踪

            # 收集结果
            for fut in as_completed(future_to_param):
                pos = future_to_param[fut]
                try:
                    result = fut.result()
                    if result is None:
                        continue
                    result.sort()
                    result = tuple(set(result))
                    if result not in results:
                        results[result] = []
                    results[result].append(pos)
                except Exception as exc:
                    raise exc

        return results

    def hint(self) -> dict[tuple, list[AbstractPosition]]:
        """
        返回每一类推理依据及其能推出的位置
        """

        self.logger.trace("构建新模型")
        self.board.clear_variable()
        model = self.board.get_model()
        switch = Switch()

        all_rules = self.summon.mines_rules.rules

        # 2.获取所有规则约束
        for rule in all_rules:
            if rule is None:
                continue
            if self.drop_r and isinstance(rule, Rule0R):
                continue
            rule.create_constraints(self.board, switch)

        for key in self.board.get_board_keys():
            for pos, obj in self.board(key=key):
                if obj is None:
                    continue
                obj.create_constraints(self.board, switch)

        # 3.获取所有变量并赋值已解完的部分
        for key in self.board.get_board_keys():
            for _, var in self.board("C", mode="variable", key=key):
                model.Add(var == 0)
                self.logger.trace(f"var: {var} == 0")
            for _, var in self.board("F", mode="variable", key=key):
                model.Add(var == 1)
                self.logger.trace(f"var: {var} == 1")

        results = {}
        future_to_param = {}

        with ThreadPoolExecutor(max_workers=CONFIG["workes_number"]) as executor:
            # 提交任务
            for pos, _ in self.board("N"):
                fut = executor.submit(hint_by_csp, self.board, self.answer_board, switch, pos)
                future_to_param[fut] = pos  # 记录参数以便出错追踪

            # 收集结果
            for fut in as_completed(future_to_param):
                pos = future_to_param[fut]
                try:
                    result = fut.result()
                    if result is None:
                        continue
                    result.sort()
                    result = tuple(set(result))
                    if result not in results:
                        results[result] = []
                    results[result].append(pos)
                except Exception as exc:
                    raise exc

        return results

    def check_difficulty(self, q=1000, br=False):
        clue_freq = {1: 0}
        _board = self.board.clone()
        n_num = len([None for key in _board.get_board_keys()
                     for _ in _board('N', key=key)])
        while self.board.has("N"):
            if br and max(clue_freq.keys()) >= q:
                return clue_freq

            print(f"{n_num - len([None for key in self.board.get_board_keys() for _ in self.board('N', key=key)])}"
                  f"/{n_num}", end="\r")
            num_clues_used = float("inf")

            n_length = len([None for key in self.board.get_board_keys() for _ in self.board('N', key=key)])
            print(f"{n_num - n_length}/{n_num}", end="\r")
            self.logger.debug("\n" + self.board.show_board())
            self.logger.debug(clue_freq)
            grouped_hints = self.hint().items()
            if not grouped_hints:
                self.logger.warn("hint无返回值")
                self.logger.warn("\n" + self.board.show_board())
                return
            self.logger.debug("\n" + self.board.show_board())
            [self.logger.debug(str(i[0]) + " -> " + str(i[1])) for i in grouped_hints]
            pos_clues = {}
            for hints, deduceds in grouped_hints:
                if "R" in hints:
                    hints_length = 1 + (len(hints) // 4)
                else:
                    hints_length = len(hints)
                if hints_length > num_clues_used:
                    continue
                elif hints_length < num_clues_used:
                    num_clues_used = hints_length
                    pos_clues.clear()
                for deduced in deduceds:
                    pos_clues[deduced] = num_clues_used
            for pos in pos_clues:
                imposs = self.answer_board.get_type(pos)
                self.apply(pos, 0 if imposs == "C" else 1)
                if pos_clues[pos] not in clue_freq:
                    clue_freq[pos_clues[pos]] = 0
                clue_freq[pos_clues[pos]] += 1
            self.logger.debug("\n" + self.board.show_board())
            self.logger.debug(clue_freq)
        self.board = _board
        self.deduced_values = {}
        return clue_freq


if __name__ == '__main__':
    # get_random(new=True, seed=9578119)
    # get_random(seed=4941992)
    get_logger(log_lv="TRACE")
    size = (5, 5)
    rules = ["V"]
    s = Summon(size, -1, rules)
    g = GameSession(s, ULTIMATE, True, 8)
    g.answer_board = s.summon_board()
    g.create_board()
    print(g.hint())
    # g.create_board()
    # while "N" in g.board:
    #     print(g.hint())
    #     print(g.deduced_values)
    #     print(g.board)
    #     for p, v in list(g.deduced_values.items())[:]:
    #         if v is MINES_TAG:
    #             g.click(p)
    #         else:
    #             g.mark(p)
    # print(g.__dict__)
    # print(g.answer_board)
    # print(g.answer_board[g.answer_board.get_pos(1, 1)].high_light(g.answer_board))
