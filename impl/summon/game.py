#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# @Time    : 2025/07/03 00:27
# @Author  : Wu_RH
# @FileName: game.py
import threading
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
                self.drop_r = True
            else:
                self.drop_r = False

        self.answer_board = None
        self.board = None

        self.mode = mode
        self.ultimate_mode = ultimate_mode

        self.deduced_values = {}
        self.last_deduced_board = None
        self.last_hint = [None, []]

        self._hint_lock = threading.Lock()
        self._hint_thread = None

        self._deduce_lock = threading.Lock()
        self._deduce_thread = None

    def hint(self, wait: bool = True, r=False) -> list[tuple[list, list[AbstractPosition]]] | None:
        """
        简化版提示获取
        - wait=True: 启动计算并硬等到结果
        - wait=False: 如果计算未运行就启动并立即返回
        """
        with self._hint_lock:
            # 如果线程正在运行
            if self._hint_thread and self._hint_thread.is_alive():
                if wait:
                    self._hint_thread.join()  # 硬等
                    return self.last_hint[1]
                return None  # 不等待直接返回

            # 没有运行则启动新线程
            def hint_task():
                try:
                    # print("hint start"+"!" * 50)
                    # print("hint start"+"!" * 50)
                    # print("hint start"+"!" * 50)
                    res = self._hint(r)  # 直接计算
                    # print("hint end"+"!" * 50)
                    # print("hint end"+"!" * 50)
                    # print("hint end"+"!" * 50)
                    print("hint: " + str(res))
                except Exception as e:
                    print(f"提示计算崩溃: {e}")
                    raise  # 重新抛出异常

            self._hint_thread = threading.Thread(target=hint_task, daemon=True)
            self._hint_thread.start()

            if wait:
                self._hint_thread.join()  # 启动后立即硬等
                return self.last_hint[1]

            return None  # 不等待直接返回

    def deduced(self, wait: bool = True, r = False):
        """
        简化版推导获取
        - wait=True: 启动计算并硬等到结果
        - wait=False: 如果计算未运行就启动并立即返回
        """
        with self._deduce_lock:
            # 如果线程正在运行
            if self._deduce_thread and self._deduce_thread.is_alive():
                if wait:
                    self._deduce_thread.join()  # 硬等
                    return self.deduced_values
                return None  # 不等待直接返回

            # 没有运行则启动新线程
            def deduce_task():
                try:
                    self._deduced(r)  # 直接计算
                except Exception as e:
                    print(f"推导计算崩溃: {e}")
                    raise  # 重新抛出异常

            self._deduce_thread = threading.Thread(target=deduce_task, daemon=True)
            self._deduce_thread.start()

            if wait:
                self._deduce_thread.join()  # 启动后立即硬等
                return self.deduced_values

            return None  # 不等待直接返回

    def solve_current_board(self, board_state, drop_r: bool) -> int:
        # CSP 解算器包装函数
        for _ in range(5):
            try:
                return solver_by_csp(
                    self.summon.mines_rules,
                    self.summon.clue_rule,
                    self.summon.mines_clue_rule,
                    board_state,
                    drop_r=drop_r,
                    bool_mode=True
                )
            except Exception as e:
                print(e)

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
        obj: AbstractClueValue
        board: AbstractBoard = self.board.clone()
        chord_positions = []
        if obj.deduce_cells(board) is not None:
            for pos, obj in self.board():
                if (obj is None) and (board[pos] is not None):
                    chord_positions.append(pos)
            return chord_positions

        self.logger.debug(f"chord pos: {clue_pos}, {self.board[clue_pos]}")

        # 失效所有与其无关的约束
        for pos, obj in board():
            if pos == clue_pos:
                continue
            if obj is None:
                continue
            if board.get_type(pos) == "F":
                board[pos] = MINES_TAG
            elif board.get_type(pos) == "C":
                board[pos] = VALUE_TAG

        # 失效右线
        if self.board.get_type(clue_pos) != "C":
            for idx in range(len(self.summon.clue_rule.subrules)):
                self.summon.clue_rule.subrules[idx][0] = False

        # 失效中线
        if self.board.get_type(clue_pos) != "F":
            for idx in range(len(self.summon.clue_rule.subrules)):
                self.summon.clue_rule.subrules[idx][0] = False

        # 失效左线
        for rule in self.summon.mines_rules.rules:
            for idx in range(len(rule.subrules)):
                rule.subrules[idx][0] = False

        for pos, value in list(self.deduced().items()).copy():
            obj = board[pos]
            board[pos] = value
            if not self.solve_current_board(board, drop_r=self.drop_r):
                chord_positions.append(pos)
            board[pos] = obj

        # 失效右线
        if self.board.get_type(clue_pos) != "C":
            for idx in range(len(self.summon.clue_rule.subrules)):
                self.summon.clue_rule.subrules[idx][0] = True

        # 失效中线
        if self.board.get_type(clue_pos) != "F":
            for idx in range(len(self.summon.clue_rule.subrules)):
                self.summon.clue_rule.subrules[idx][0] = True

        # 失效左线
        for rule in self.summon.mines_rules.rules:
            for idx in range(len(rule.subrules)):
                rule.subrules[idx][0] = True

        return chord_positions

    def click(self, pos: "AbstractPosition") -> Union["AbstractBoard", None]:
        """
        翻开/点击 某个空白格
        :param pos: 翻开的位置
        """
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
            self.step()
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
            self.step()
        return self.board

    def step(self):
        if self.deduced():
            return
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

    def _deduced(self, r=False):
        """
        收集所有必然能推出的位置及其不可能的值
        """
        if self.mode == PUZZLE:
            # 如果是纸笔模式直接把答案反一下给他
            positions = [position for key in self.board.get_board_keys() for position, _ in self.board("N", key=key)]
            deduced_values = {}
            for pos in positions:
                if self.answer_board.get_type(pos) == "C":
                    deduced_values[pos] = self.board.get_config(
                        pos.board_key, "MINES")
                elif self.answer_board.get_type(pos) == "F":
                    deduced_values[pos] = self.board.get_config(
                        pos.board_key, "VALUE")
            self.deduced_values = deduced_values
            return deduced_values
        if not r and self.last_deduced_board == self.board:
            return self.deduced_values
        self.last_deduced_board = self.board.clone()
        # 获取之前推导过的
        deduced_values: dict["AbstractPosition", object] = self.deduced_values
        # 与题板进行检查 并去除已经放置的
        if type(self.mode) is str:
            raise ValueError("未进行多题板遍历")
        for key in self.board.get_board_keys():
            for position, _ in self.board("CF", key=key):
                if position in deduced_values:
                    del deduced_values[position]

        board = self.board.clone()

        positions = [position for key in board.get_board_keys() for position, _ in self.board("N", key=key)]
        for position in positions:
            if position in deduced_values:
                continue
            self.logger.debug(f"deduced start {position}")
            answer_type = self.answer_board.get_type(position)
            if answer_type == "C":
                false_tag = board.get_config(position.board_key, "MINES")
                board.set_value(position, false_tag)
            elif answer_type == "F":
                true_tag = board.get_config(position.board_key, "VALUE")
                board.set_value(position, true_tag)
            elif answer_type == "N":
                self.logger.error("\n" + self.answer_board.show_board())
                raise ValueError("None type shouldn't on answer board")

            if self.solve_current_board(board, drop_r=self.drop_r) == 0:
                deduced_values[position] = board.get_value(position)

            board.set_value(position, None)  # 还原

        self.deduced_values = deduced_values

        return deduced_values

    def _hint(self, r=False) -> list[tuple[list, list[AbstractPosition]]]:
        """
        返回每一类推理依据及其能推出的位置
        """
        if not r and self.board == self.last_hint[0]:
            return self.last_hint[1]

        grouped_deductions: list[tuple[list, list["AbstractPosition"]]] = []
        for pos, _ in self.board("CF"):
            positions = self.chord_clue(pos)
            if not positions:
                continue
            grouped_deductions.append(([pos], positions))
        if grouped_deductions:
            self.last_hint = [self.board.clone(), grouped_deductions.copy()]
            return grouped_deductions

        # 初始化当前的所有可推格
        deduced_assignments = self.deduced()
        if not deduced_assignments:
            self.step()
            if self.drop_r and not len(self.deduced().keys()):
                self.drop_r = False
                self.last_hint = [None, []]
                self.last_deduced_board = None
                self.deduced(False)
                return [self.board.clone(), [([("R", 0)], [])]]
            self.last_hint = [None, []]
            return []

        # 每个可推出位置 -> 可推出它的约束来源列表
        deduction_origin_map: dict["AbstractPosition", list] = {}

        # 克隆一个题板用于假设推理
        hypothesis_board = self.board.clone()

        def build_assignment_operator(_pos: "AbstractPosition") -> \
                tuple[Callable[[], None], Callable[[], None], object]:
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
            # 位置直接返回位置对象
            return _deactivate, _restore, _pos

        def build_subrule_toggle_operator(_param: tuple) -> \
                tuple[Callable[[], None], Callable[[], None], object]:
            _rule, subrule_index = _param
            _deactivate = lambda: _rule.subrules.__getitem__(subrule_index).__setitem__(0, False)
            _restore = lambda: _rule.subrules.__getitem__(subrule_index).__setitem__(0, True)
            # 关于hint的规则显示链接
            return _deactivate, _restore, (_rule.name, subrule_index)

        # 初始化所有线索与规则的启用/禁用操作
        constraint_toggle_list: list[tuple[Callable[[], None], Callable[[], None], object]] = []

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

        # 加入所有中线规则子约束的开关操作
        for idx in range(len(self.summon.mines_clue_rule.subrules)):
            constraint_toggle_list.append(
                build_subrule_toggle_operator((self.summon.clue_rule, idx))
            )

        # 加入所有左线规则子约束的开关操作
        for rule in self.summon.mines_rules.rules:
            if self.drop_r and isinstance(rule, Rule0R):
                build_subrule_toggle_operator((rule, 0))[0]()
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
                    if self.solve_current_board(hypothesis_board, drop_r=self.drop_r) != 0:
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
                    if self.solve_current_board(hypothesis_board, drop_r=self.drop_r) == 0:
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
        for pos, origin_list in deduction_origin_map.items():
            print("origin_list", origin_list)
            origin_list = ([i for i in origin_list if isinstance(i, tuple)] +
                           sorted([i for i in origin_list if isinstance(i, AbstractPosition)]))
            found = False
            for existing_basis, grouped_positions in grouped_deductions:
                if origin_list == existing_basis:
                    grouped_positions.append(pos)
                    found = True
                    break
            if not found:
                grouped_deductions.append((origin_list, [pos]))

        for rule in self.summon.mines_rules.rules:
            if self.drop_r and isinstance(rule, Rule0R):
                build_subrule_toggle_operator((rule, 0))[1]()

        self.last_hint = [self.board.clone(), grouped_deductions[:]]

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
            # __board = self.summon.clue_coverage(self.board)[1]
            # chord = len([None for key in self.board.get_board_keys() for _ in self.board('N', key=key)])
            # chord -= len([None for key in __board.get_board_keys() for _ in __board('N', key=key)])
            # clue_freq[1] += chord
            # self.board = __board
            # self.logger.debug(f"确定了{chord}个线索")
            #
            # if "N" not in self.board:
            #     break

            n_length = len([None for key in self.board.get_board_keys() for _ in self.board('N', key=key)])
            print(f"{n_num - n_length}/{n_num}", end="\r")
            self.logger.debug("\n" + self.board.show_board())
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


if __name__ == '__main__':
    get_random(seed=4941992)
    size = (5, 5)
    rules = ["V"]
    s = Summon(size, -1, rules)
    g = GameSession(s, ULTIMATE, True, 8)
    g.answer_board = s.summon_board()
    g.create_board()
    while "N" in g.board:
        print(g.hint())
        print(g.deduced_values)
        print(g.board)
        for p, v in list(g.deduced_values.items())[:]:
            if v is MINES_TAG:
                g.click(p)
            else:
                g.mark(p)
    print(g.__dict__)
