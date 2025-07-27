#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# @Time    : 2025/06/03 05:23
# @Author  : Wu_RH
# @FileName: run.py
# @Version : 1.0.0
import shutil
import sys
import argparse
import textwrap

import yaml
from pathlib import Path

from main.generate_puzzle import main as puzzle
from main.generate_game import main as puzzle_query
from main.generate_test import main as test

# ==== 获取默认值 ====
default_path = Path("config/default.yaml")
defaults = {}
if default_path.exists():
    with open(default_path, "r", encoding="utf-8") as f:
        defaults = yaml.safe_load(f)

# ==== 参数解析 ====
parser = argparse.ArgumentParser(description="")

subparsers = parser.add_subparsers(dest='command', required=False)

subparsers.add_parser('list', help='列出所有规则的文档说明')

parser.add_argument("-s", "--size", nargs="+",
                    help="纸笔的题板边长")
parser.add_argument("-t", "--total", type=int, default=defaults.get("total"),
                    help="总雷数")
parser.add_argument("-c", "--rules", nargs="+", default=[],
                    help="所有规则名")
parser.add_argument("-d", "--dye", default=defaults.get("dye"),
                    help="染色规则名称，如 @c")
parser.add_argument("-r", "--used-r", action="store_true", default=defaults.get("used_r"),
                    help="推理是否加R")
parser.add_argument("-a", "--attempts", type=int, default=defaults.get("attempts"),
                    help="尝试生成题板次数")
parser.add_argument("-q", "--query", type=int, default=defaults.get("query"),
                    help="生成题板的至少有几线索推理")
parser.add_argument("-e", "--early-stop", action="store_true", default=False,
                    help="生成题板的时候达到指定线索数量推理的时候 直接退出 这会导致线索图不正确")
parser.add_argument("-v", "--vice-board", action="store_true", default=False,
                    help="启用后生成题板的时候可以删除副板的信息")
parser.add_argument("--test", action="store_true", default=False,
                    help="启用后将仅生成一份使用了规则的答案题板")
parser.add_argument("--seed", type=int, default=defaults.get("seed"),
                    help="随机种子")
parser.add_argument("--log-lv", default=defaults.get("log_lv"),
                    help="日志等级，如 DEBUG、INFO、WARNING")
parser.add_argument("--board-class", default=defaults.get("board_class"),
                    help="题板的类名/题板的名称 通常使用默认值即可")
args = parser.parse_args()

# ==== 调用生成 ====


def print_with_indent(text, indent="\t"):
    width = shutil.get_terminal_size(fallback=(80, 24)).columns // 2
    # 减去缩进长度，避免超宽
    effective_width = width - len(indent.expandtabs())
    lines = text.splitlines()
    for line in lines:
        wrapped = textwrap.fill(line, width=effective_width,
                                initial_indent=indent,
                                subsequent_indent=indent)
        print(wrapped, flush=True)
    print()


if args.command == "list":
    from impl import rule
    rule_list = rule.get_all_rules()

    if rule_list["L"]:
        print("\n\n左线规则:", flush=True)
    for doc in rule_list["L"]:
        print_with_indent(doc)

    if rule_list["M"]:
        print("\n\n中线规则:", flush=True)
    for doc in rule_list["M"]:
        print_with_indent(doc)

    if rule_list["R"]:
        print("\n\n右线规则:", flush=True)
    for doc in rule_list["R"]:
        print_with_indent(doc)

    sys.exit(0)

if args.size is None:
    parser.print_help()
    sys.exit(0)
else:
    if len(args.size) == 0:
        parser.print_help()
        sys.exit(0)
    elif len(args.size) == 1:
        size = (int(args.size[0]), int(args.size[0]))
    else:
        size = (int(args.size[0]), int(args.size[1]))

if args.seed != defaults.get("seed"):
    args.attempts = 1

for rule_name in args.rules:
    if "$" in rule_name:
        args.rules[args.rules.index(rule_name)] = rule_name.replace("$", "^")

with open("./output/temp.txt", "w") as f:
    f.write(str(args.rules))

if args.test:
    test(
        log_lv=args.log_lv,
        seed=args.seed,
        size=size,
        total=args.total,
        rules=[i.upper() for i in args.rules],
        dye=args.dye.lower(),
        board_class=args.board_class,
    )
elif args.query == defaults.get("query"):
    puzzle(
        log_lv=args.log_lv,
        seed=args.seed,
        attempts=args.attempts,
        size=size,
        total=args.total,
        rules=[i.upper() for i in args.rules],
        dye=args.dye.lower(),
        drop_r=(not args.used_r),
        board_class=args.board_class,
        vice_board=args.vice_board
    )
else:
    puzzle_query(
        log_lv=args.log_lv,
        seed=args.seed,
        size=size,
        total=args.total,
        rules=[i.upper() for i in args.rules],
        query=args.query,
        attempts=args.attempts,
        dye=args.dye.lower(),
        drop_r=(not args.used_r),
        early_stop=args.early_stop,
        board_class=args.board_class,
        vice_board=args.vice_board
    )
