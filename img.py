#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# @Time    : 2025/06/19 23:05
# @Author  : Wu_RH
# @FileName: img.py
# @Version : 1.0.0
import sys
import yaml
import argparse
from pathlib import Path

from minesweepervariants.impl.impl_obj import get_board, decode_board
from minesweepervariants.utils.image_create import draw_board

# ==== 获取默认值 ====
default_path = Path("config/default.yaml")
defaults = {
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
        defaults.update(yaml.safe_load(f))

# ==== 参数解析 ====
parser = argparse.ArgumentParser(description="")

parser.add_argument("-c", "--code", type=str,
                    help="题板字节码")  # 字符串类型
parser.add_argument("-r", "--rule-text", type=str, default="",
                    help="规则字符串，有空格需要带引号")  # 字符串类型
parser.add_argument("-o", "--output", type=str, default=defaults["output_file"],
                    help="输出的文件名（不含后缀）")  # 字符串类型
parser.add_argument("-s", "--size", type=int, default=defaults["cell_size"],
                    help="单元格像素数")  # 整数
parser.add_argument("-b", "--board-class", type=str, default=defaults["board_class"],
                    help="题板类的名称代号")
parser.add_argument("-w", "--white-base", action="store_true", default=defaults["white_base"],
                    help="题板背景是否是白底的")

args = parser.parse_args()

# ==== 调用生成 ====

if args.code is None:
    parser.print_help()
    sys.exit(0)

try:
    board = decode_board(args.code)
except:
    code = bytes.fromhex(args.code)
    board = get_board(args.board_class)(code=code)


draw_board(
    board=board,
    bottom_text=args.rule_text,
    output=args.output,
    background_white=args.white_base,
    cell_size=args.size
)
