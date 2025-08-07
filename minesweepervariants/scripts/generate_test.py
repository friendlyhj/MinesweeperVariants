#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# @Time    : 2025/07/06 05:43
# @Author  : Wu_RH
# @FileName: generate_test.py
import os
import threading
import time
from pathlib import Path
import yaml

from minesweepervariants.impl.summon import Summon
from minesweepervariants.utils.image_create import draw_board
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
    with open(default_path, "r", encoding="utf-8") as config_file:
        CONFIG.update(yaml.safe_load(config_file))
if base_path.exists():
    with open(base_path, "r", encoding="utf-8") as config_file:
        CONFIG.update(yaml.safe_load(config_file))


def main(
        log_lv: str,  # 日志等级
        seed: int,  # 随机种子
        size: tuple[int, int],  # 题板尺寸
        total: int,  # 总雷数
        rules: list[str],  # 规则id集合
        dye: str,  # 染色规则
        board_class: str,  # 题板的名称
):
    logger = get_logger(log_lv=log_lv)
    get_random(seed, new=True)
    attempt_index = 0
    s = Summon(size=size, total=total, rules=rules, board=board_class, dye=dye)
    total = s.total
    logger.info(f"total mines: {total}")
    _board = None
    while True:
        attempt_index += 1
        print(f"尝试第{attempt_index}次minesweepervariants..", end="\r")
        get_random(seed, new=True)
        a_time = time.time()
        _board = s.summon_board()
        if _board is None:
            continue
        logger.info(f"<{attempt_index}>生成用时:{(time_used := time.time() - a_time)}s")
        logger.info(f"总雷数: {total}")
        logger.info("\n" + _board.show_board())

        rule_text = ""
        for rule in rules:
            rule_text += "[" + (rule.split(CONFIG['delimiter'])[0] if
                                CONFIG['delimiter'] in rule else rule) + "]"
        if rule_text == "":
            rule_text = "[V]"
        if dye:
            rule_text += f"[@{dye}]"
        rule_text += f"{size[0]}x{size[1]}"

        if not os.path.exists(CONFIG["output_path"]):
            os.mkdir(CONFIG["output_path"])

        with open(os.path.join(CONFIG["output_path"], "demo.txt"), "a", encoding="utf-8") as f:
            f.write("\n" + ("=" * 100) + "\n\n生成时间" + logger.get_time() + "\n")
            f.write(f"生成用时:{time_used}s\n")
            f.write(f"总雷数: {total}\n")
            f.write(f"种子: {get_seed()}\n")
            f.write(rule_text)
            f.write("\n"+_board.show_board())

            f.write(f"\n题板: img -c {_board.encode().hex()} ")
            f.write(f"-r \"{rule_text}-R{total}")
            f.write(f"-{get_seed()}\" ")
            f.write("-o answer\n")

        def d():
            draw_board(board=_board, cell_size=100, output="answer",
                       bottom_text=rule_text + f"-R{total}-{get_seed()}\n")
        threading.Thread(target=d, daemon=True).start()

        logger.info("\n\n" + "=" * 20 + "\n")
        logger.info("\n生成时间" + logger.get_time() + "\n")
        logger.info(f"生成用时:{time_used}s\n")
        logger.info(f"总雷数: {total}\n")
        logger.info("\n" + _board.show_board() + "\n")

        input("检查完毕后输入回车继续尝试 使用ctrl+c终止进程\r")
        attempt_index = 0
