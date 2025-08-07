#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# @Time    : 2025/06/17 08:52
# @Author  : xxx
# @FileName: generate_game.py
"""
普通模式-随机生成题板
"""
import os
import time
from pathlib import Path

import yaml

from minesweepervariants.impl.impl_obj import ModelGenerateError, get_board, encode_board
from minesweepervariants.impl.summon import Summon
from minesweepervariants.impl.summon.game import GameSession, PUZZLE
from minesweepervariants.impl.summon.summon import GenerateError
from minesweepervariants.utils.impl_obj import get_seed
from minesweepervariants.utils.tool import get_logger, get_random

base_path = Path("config/base_puzzle_config.yaml")
default_path = Path("config/default.yaml")
CONFIG = {
    "output_file": "output",   # 默认的img文件名(不含后缀)
    "cell_size": 100,          # 一个单元格的尺寸
    "white_base": False,       # 默认黑底
    "board_class": None,       # 调用默认版本最高的board_class
    "image_debug": False,      # 在生成图片的时候启用debug显示: 在显示的时候会附上红蓝框方便查看

    "seed": -1,                # 随机种子
    "logger_lv": "INFO",       # 默认logger为info级别
    "attempts": -1,            # 默认无限次次数尝试 (无-q参数默认20次)
    "query": -1,               # 如果非-1的话就会启用-1参数
    "total": -1,               # 默认自动计算总雷数数量
    "dye": "",                  # 默认无染色
    "used_r": False,           # 默认不启用R推理
    "output_path": ".\\output", # 保存到哪个文件夹内 默认为工作目录下的output内
    "timeout": 0,              # 求解器进行多少时间后算为超时 单位秒 0为无限制
    "workes_number": 20        # 提示系统中多线程的数量
}
if default_path.exists():
    with open(default_path, "r", encoding="utf-8") as f:
        CONFIG.update(yaml.safe_load(f))
if base_path.exists():
    with open(base_path, "r", encoding="utf-8") as f:
        CONFIG.update(yaml.safe_load(f))


def main(
        log_lv: str,  # 日志等级
        seed: int,  # 随机种子
        size: tuple[int, int],  # 题板尺寸
        total: int,  # 总雷数
        rules: list[str],  # 所有的规则集合
        query: int,  # 至少有几线索推理
        attempts: int,  # 尝试次数
        dye: str,  # 染色规则
        drop_r: bool,  # 在推理时候是否隐藏R推理
        early_stop: bool,  # 如果达到指定的线索数量 直接跳出
        board_class: str,     # 题板的类名
        vice_board: bool,   # 启用删除副板
):
    logger = get_logger(log_lv=log_lv)
    get_random(seed, new=True)
    s = Summon(size=size, total=total, rules=rules, board=board_class,
               drop_r=drop_r, dye=dye, vice_board=vice_board)

    rule_text = ""
    for rule in rules:
        rule_text += "[" + (rule.split(CONFIG['delimiter'])[0] if
                            CONFIG['delimiter'] in rule else rule) + "]"
    if rule_text == "":
        rule_text = "[V]"
    if dye:
        rule_text += f"[{dye}]"

    size_a = 0
    size_b = 0
    size_c = len(s.board.get_interactive_keys())
    for key in s.board.get_interactive_keys():
        bound = s.board.boundary(key)
        size_a = max(size_a, bound.x + 1)
        size_b = max(size_b, bound.y + 1)
    rule_text += f"{size[0]}x{size[1]}"
    if size_c > 1:
        rule_text += f"x{size_c}"
    total = s.total
    logger.info(f"total mines: {total}")

    attempt_index = 0

    while True:
        get_random(seed, new=True)
        a_time = time.time()
        if attempts != -1 and attempt_index >= attempts:
            break
        attempt_index += 1
        game = GameSession(s, mode=PUZZLE, drop_r=drop_r)
        try:
            game.board = s.create_puzzle()
        except ModelGenerateError:
            continue
        except GenerateError:
            continue
        game.answer_board = get_board(board_class)(code=s.answer_board_code)
        # game.board = get_board("0B")(code=b'')
        # game.answer_board = get_board("0B")(code=b'')
        _board = game.board.clone()
        game.logger.info("\n" + "=" * 30 + "\nanswer_board:\n" + game.answer_board.show_board())
        game.logger.info("\nboard:\n" + game.board.show_board())
        game.logger.info("board: " + str(game.board.encode()))
        game.logger.info("answer: " + str(game.answer_board.encode()))
        try:
            clue_freq = game.check_difficulty(query, br=early_stop)
        except ModelGenerateError:
            continue
        if not clue_freq:
            logger.warn("生成失败")
            continue
        game.logger.info("\n" + "=" * 50 + "\n" + str(clue_freq))
        time_used = time.time() - a_time
        n_num = len([None for _ in _board("N")])
        board_str = _board.show_board()
        answer = game.answer_board.show_board()
        board_code = _board.encode()
        answer_code = game.answer_board.encode()

        if not any(k >= query for k in clue_freq):
            continue

        if not os.path.exists(CONFIG["output_path"]):
            os.makedirs(CONFIG["output_path"])

        mask = 0
        for _, obj in _board():
            if obj is None:
                mask += 1
            mask <<= 1

        # 计算需要的字节长度
        byte_length = (mask.bit_length() + 7) // 8  # 计算所需字节数
        byte_length = max(byte_length, 1)  # 确保至少 1 字节

        mask = mask.to_bytes(byte_length, "big", signed=False)

        with open(os.path.join(CONFIG["output_path"], "demo.txt"), "a", encoding="utf-8") as f:
            f.write("\n" + ("=" * 100) + "\n\n生成时间" + logger.get_time() + "\n")
            f.write(f'线索表\n')
            if 0 in clue_freq:
                f.write("存在线索数为0的可推格 请注意辨别\n")
            if early_stop:
                f.write("(已启用-e参数 线索图不准确)\n")
            f.write(f'{clue_freq}\n')
            f.write(f"生成用时:{time_used}s\n")
            f.write(f"总雷数: {total}/{n_num}\n")
            f.write(f"种子: {get_seed()}\n")
            f.write("\n" + rule_text)
            f.write("\n" + board_str)
            f.write("\n" + answer)

            f.write(f"\n答案: img -c {answer_code.hex()} ")
            f.write(f"-r \"{rule_text}-R{total}/")
            f.write(f"{n_num}-{get_seed()}\" ")
            f.write("-o answer\n")

            f.write(f"\n题板: img -c {board_code.hex()} ")
            f.write(f"-r \"{rule_text}-R{'*' if drop_r else total}/")
            f.write(f"{n_num}-{get_seed()}\" ")
            f.write("-o demo\n")

            f.write(f"\n题板代码: \n{encode_board(answer_code)}:{mask.hex()}\n")
