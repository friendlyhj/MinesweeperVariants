#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# @Time    : 2025/07/03 00:27
# @Author  : Wu_RH
# @FileName: game.py

from typing import Union, Callable
import itertools as it


from abs.Lrule import Rule0R
from abs.Rrule import AbstractClueValue
from abs.board import AbstractBoard
from abs.board import AbstractPosition
from impl.summon import Summon
from impl.summon.solver import solver_by_csp
from utils.impl_obj import MINES_TAG, VALUE_QUESS, POSITION_TAG
from utils.tool import get_logger, get_random

NORMAL = 0  # 普通模式
EXPERT = 1  # 专家模式
ULTIMATE = 2  # 终极模式
PUZZLE = 3  # 纸笔模式(用于调试)


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
    def __init__(self, summon: Summon, mode=NORMAL, drop_r=False):
        self.logger = get_logger()
        self.summon = summon
        self.mode = mode
        self.drop_r = drop_r

        if mode == PUZZLE:
            self.answer_board = None
            self.board = None
        else:
            self.logger.debug("开始初始化题板")
            self.answer_board = self.summon.summon_board()
            self.board = self.create_board()
            self.logger.debug("初始化完毕")

        self.deduced_values = {}
        self._origin_map = {}

    def solve_current_board(self, board_state, drop_rules: bool) -> int:
        # CSP 解算器包装函数
        return solver_by_csp(
            self.summon.mines_rules,
            self.summon.clue_rule,
            self.summon.mines_clue_rule,
            board_state,
            drop_r=drop_rules,
            bool_mode=True
        )

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
        clues = [i for i in board("C")]
        for pos, clue in get_random().sample(clues, len(clues)):
            board.set_value(pos, MINES_TAG)
            if solver_by_csp(
                    self.summon.mines_rules,
                    self.summon.clue_rule,
                    self.summon.mines_clue_rule,
                    board.clone(), drop_r=True) == 0:
                board.set_value(pos, None)
                continue
            board.set_value(pos, clue)
        return board

    def apply(self, pos: AbstractPosition, action: int) -> Union["AbstractBoard", None]:
        """
        :param pos: 交互位置
        :param action: 操作代码
            0: 左键点击/翻开/设置非雷
            1: 右键点击/标雷/设置必雷
        """
        if self.mode == PUZZLE:
            if action == 1:
                value_tag = self.board.get_config(pos.board_key, "MINES")
                self.board.set_value(pos, value_tag)
            elif action == 0:
                value_tag = self.board.get_config(pos.board_key, "VALUE")
                self.board.set_value(pos, VALUE_TAG if value_tag == VALUE_QUESS else value_tag)
            return self.board
        if self.board.get_type(pos) != "N":
            # 等会再写交互罢:D
            # 懒b ↑
            return self.board
        if self.answer_board.get_type(pos) == "C":
            if action == 1:
                # 标错了
                return None
            if self.mode == NORMAL:
                self.board.set_value(pos, self.answer_board.get_value(pos))
                return self.board
            elif self.mode == EXPERT:
                if pos in self.deduced():
                    self.board.set_value(pos, self.answer_board.get_value(pos))
                    return self.board
                else:
                    return None
            elif self.mode == ULTIMATE:
                if pos in self.deduced():
                    self.board.set_value(pos, VALUE_TAG)
                else:
                    return None
                if not self.deduced():
                    # 全部都推完了
                    ...
                return self.board

        elif self.answer_board.get_type(pos) == "F":
            if action == 0:
                # 踩雷了
                return None
            if self.mode == NORMAL:
                self.board.set_value(pos, self.answer_board.get_value(pos))
                return self.board
            elif self.mode == EXPERT:
                if pos in self.deduced():
                    self.board.set_value(pos, self.answer_board.get_value(pos))
                    return self.board
                else:
                    return None
            elif self.mode == ULTIMATE:
                if pos in self.deduced():
                    value_tag = self.board.get_config(pos.board_key, "MINES")
                    self.board.set_value(pos, value_tag)
                else:
                    return None
                if not self.deduced():
                    # 全部都推完了
                    ...
                return self.board
        else:
            # 你答案题板为啥有None?
            self.logger.warn("答案题板携带None")

    def click(self, positions: list["AbstractPosition"]) -> Union["AbstractBoard", None]:
        """
        翻开/点击 某个空白格
        :param positions: 翻开的位置列表
        """
        for pos in positions:
            if self.apply(pos, 0) is None:
                return None
        return self.board

    def mark(self, positions: list["AbstractPosition"]) -> Union["AbstractBoard", None]:
        """
        右键标雷
        """
        for pos in positions:
            if self.apply(pos, 1) is None:
                return None
        return self.board

    def step(self):
        """
        游戏步进:
        遍历完全部的可推
        """

    def deduced(self):
        """
        收集所有必然能推出的位置及其不可能的值
        """
        if self.mode == PUZZLE:
            # 如果是纸笔模式直接把答案反一下给他
            deduced_values = {}
            for key in self.board.get_board_keys():
                for pos, _ in self.board("N", key=key):
                    if self.answer_board.get_type(pos) == "C":
                        deduced_values[pos] = self.board.get_config(
                            pos.board_key, "MINES")
                    elif self.answer_board.get_type(pos) == "F":
                        deduced_values[pos] = self.board.get_config(
                            pos.board_key, "VALUE")
            self.deduced_values = deduced_values
            return deduced_values
        # 获取之前推导过的
        deduced_values: dict["AbstractPosition", object] = self.deduced_values
        # 与题板进行检查 并去除已经放置的
        if type(self.mode) == str:
            raise ValueError("未进行多题板遍历")
        for key in self.board.get_board_keys():
            for position, _ in self.board("CF", key=key):
                if position in deduced_values:
                    del deduced_values[position]

        for key in self.board.get_board_keys():
            for position, _ in self.board("N", key=key):
                if position in deduced_values:
                    continue
                answer_type = self.answer_board.get_type(position)
                if answer_type == "C":
                    false_tag = self.board.get_config(position.board_key, "MINES")
                    self.board.set_value(position, false_tag)
                elif answer_type == "F":
                    true_tag = self.board.get_config(position.board_key, "VALUE")
                    self.board.set_value(position, true_tag)
                elif answer_type == "N":
                    self.logger.error("\n"+self.answer_board.show_board())
                    raise ValueError("None type shouldn't on answer board")

                if self.solve_current_board(self.board, drop_rules=False) == 0:
                    deduced_values[position] = self.board.get_value(position)

                self.board.set_value(position, None)  # 还原

        self.deduced_values = deduced_values

        return deduced_values

    def hint(self) -> list[tuple[list[str], list[AbstractPosition]]]:
        """
        返回每一类推理依据及其能推出的位置
        """

        # 初始化当前的所有可推格
        deduced_assignments = self.deduced()
        # 每个可推出位置 -> 可推出它的约束来源列表
        deduction_origin_map: dict["AbstractPosition", list[str]] = {}

        # 克隆一个题板用于假设推理
        hypothesis_board = self.board.clone()

        def build_assignment_operator(_pos: "AbstractPosition") -> \
                tuple[Callable[[], None], Callable[[], None], str]:
            _val = self.board.get_value(_pos)
            if self.board.get_type(_pos) == "C":
                _deactivate = lambda: hypothesis_board.set_value(_pos, VALUE_TAG)
            elif self.board.get_type(_pos) == "F":
                value_flag = hypothesis_board.get_config(_pos.board_key, "MINES")
                _deactivate = lambda: hypothesis_board.set_value(_pos, value_flag)
            else:
                self.logger.error("board遍历的时候使用参数CF返回了N 汇报给上层")
                raise ValueError("")
            _restore = lambda: hypothesis_board.set_value(_pos, _val)
            return _deactivate, _restore, str(_pos)

        def build_subrule_toggle_operator(_param: tuple) -> \
                tuple[Callable[[], None], Callable[[], None], str]:
            _rule, subrule_index = _param
            _deactivate = lambda: _rule.subrules.__getitem__(subrule_index).__setitem__(0, False)
            _restore = lambda: _rule.subrules.__getitem__(subrule_index).__setitem__(0, True)
            return _deactivate, _restore, str(_rule.subrules[subrule_index][1])

        # 初始化所有线索与规则的启用/禁用操作
        constraint_toggle_list: list[tuple[Callable[[], None], Callable[[], None], str]] = []

        # 加入所有线索点操作
        for pos, obj in self.board("CF"):
            if obj in (
                VALUE_TAG, MINES_TAG,
                self.board.get_config(
                    pos.board_key, "VALUE"),
                self.board.get_config(
                    pos.board_key, "MINES")
            ):
                continue
            if obj.invalid(self.board):
                continue
            constraint_toggle_list.append(build_assignment_operator(pos))

        # 加入所有右线规则子约束的开关操作
        for idx in range(len(self.summon.clue_rule.subrules)):
            constraint_toggle_list.append(
                build_subrule_toggle_operator((self.summon.clue_rule, idx))
            )

        # 加入所有左线规则子约束的开关操作
        for rule in self.summon.mines_rules.rules:
            if self.drop_r and isinstance(rule, Rule0R):
                continue
            for idx in range(len(rule.subrules)):
                constraint_toggle_list.append(build_subrule_toggle_operator((rule, idx)))

        working_toggle_list = constraint_toggle_list

        for deduced_position, deduced_value in deduced_assignments.items():
            self.logger.debug(f"start {deduced_position}")
            # 本轮使用的可用约束组
            active_toggle_list = working_toggle_list.copy()
            # 被识别为有效的相关约束
            related_toggle_stack = []

            min_count = min([float("inf")] + [len(i) for i in deduction_origin_map.values()])
            hypothesis_board.set_value(deduced_position, deduced_value)
            deduction_origin_map[deduced_position] = []

            try:
                for idx in range(len(working_toggle_list) - 1, -1, -1):
                    deactivate, restore, constraint_label = working_toggle_list[idx]
                    deactivate()
                    if self.solve_current_board(hypothesis_board, drop_rules=False) != 0:
                        deduction_origin_map[deduced_position].append(constraint_label)
                        related_toggle_stack.append(active_toggle_list.pop(idx))
                    restore()
                    if min_count < len(deduction_origin_map[deduced_position]):
                        raise ValueError

            except ValueError:
                del deduction_origin_map[deduced_position]
                hypothesis_board.set_value(deduced_position, None)
                continue

            for deactivate, *_ in active_toggle_list:
                deactivate()
            for _, restore, *_ in related_toggle_stack:
                restore()

            self.logger.debug(f"{deduced_position} OR | "
                              f"len: {len(related_toggle_stack)}")

            found = False
            subset_size = 0
            while True:
                self.logger.debug(f"size: {subset_size}")
                if subset_size + len(related_toggle_stack) > min_count:
                    break
                if len(deduction_origin_map) != 1 and subset_size > 2:
                    break
                if subset_size > 3:
                    break
                for subset in it.combinations(active_toggle_list, subset_size):
                    if found:
                        break
                    for _, restore, *_ in subset:
                        restore()
                    if self.solve_current_board(hypothesis_board, drop_rules=False) == 0:
                        deduction_origin_map[deduced_position].extend([label for *_, label in subset])
                        found = True
                    for deactivate, *_ in subset:
                        deactivate()
                if found:
                    break
                subset_size += 1
            if not found:
                del deduction_origin_map[deduced_position]
                self.logger.debug(f"{deduced_position}: fail")
            else:
                self.logger.debug(f"{deduced_position}: {subset_size}\t"
                                  f"len: {len(deduction_origin_map[deduced_position])}")
            self.logger.debug(f"{len(deduction_origin_map)}/{len(deduced_assignments)}")

            for _, restore, *_ in working_toggle_list:
                restore()
            hypothesis_board.set_value(deduced_position, None)

        # 整理为约束依据 -> 被推出的所有格子列表
        grouped_deductions: list[tuple[list[str], list["AbstractPosition"]]] = []
        for pos, origin_list in deduction_origin_map.items():
            found = False
            for existing_basis, grouped_positions in grouped_deductions:
                if origin_list == existing_basis:
                    grouped_positions.append(pos)
                    found = True
                    break
            if not found:
                grouped_deductions.append((origin_list, [pos]))

        return grouped_deductions

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

            # chord
            __board = self.summon.clue_coverage(self.board)[1]
            chord = len([None for key in self.board.get_board_keys() for _ in self.board('N', key=key)])
            chord -= len([None for key in __board.get_board_keys() for _ in __board('N', key=key)])
            clue_freq[1] += chord
            self.board = __board
            self.logger.debug(f"确定了{chord}个线索")

            if "N" not in self.board:
                break

            n_length = len([None for key in self.board.get_board_keys() for _ in self.board('N', key=key)])
            print(f"{n_num - n_length}/{n_num}", end="\r")
            self.logger.debug("\n"+self.board.show_board())
            self.logger.debug(clue_freq)
            grouped_hints = self.hint()
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
                imposs = self.deduced_values[pos]
                mines_tag = self.board.get_config(pos.board_key, "MINES")
                self.apply(pos, 0 if imposs == mines_tag else 1)
                if pos_clues[pos] not in clue_freq:
                    clue_freq[pos_clues[pos]] = 0
                clue_freq[pos_clues[pos]] += 1
            self.logger.debug("\n" + self.board.show_board())
            self.logger.debug(clue_freq)
        self.board = _board
        self.deduced_values = {}
        return clue_freq

