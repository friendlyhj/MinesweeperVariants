#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# @Time    : 2025/07/30 08:15
# @Author  : Wu_RH
# @FileName: app.py.py
from pathlib import Path
from typing import Union

from flask import Flask, render_template, jsonify, request
import yaml
import sys
import os

from abs.board import AbstractPosition
from abs.rule import AbstractRule
from impl.summon.game import GameSession as Game
from impl.summon.summon import Summon
from impl.impl_obj import get_board, decode_board
from impl.board.version2 import Board

# 添加项目路径到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入项目核心模块

app = Flask(
    __name__,
    template_folder='web/templates',
    static_folder='web/assets',
    static_url_path='/assets'
)

# 加载配置
default_path = Path("config/web_config.yaml")
# CONFIG = {}
# if default_path.exists():
#     with open(default_path, "r", encoding="utf-8") as f:
#         CONFIG = yaml.safe_load(f)
board_name = "Board1"
hypothesis_data = dict()


def format_cell(_board, pos):
    def init_component(data) -> dict:
        if data["type"] in ["col", "row"]:
            if data["type"] == "col":
                style = "display: flex; flex-direction: column; align-items: center; gap: 4px;"
            else:
                style = "display: flex; flex-direction: row; justify-content: center; gap: 4px;"

            return {
                "type": "container",
                "value": [init_component(i) for i in data["children"] if init_component(i) is not None],
                "style": style
            }
        elif data["type"] == "text":
            style = f"fill: var({primary_color});"
            style += " text-align: center; display: flex;"
            style += " justify-content: center; align-items: center;"
            style += " height: 100%; width: 100%;"
            return {
                "type": "text",
                "value": data.get("text", ""),
                "style": style
            }
        elif data["type"] == "image":
            path = data.get("image")[7:-4]
            return {
                "type": "assets",
                "value": path,
                "style": f"fill: var({primary_color}); "
            }
        elif data["type"] == "placeholder":
            style = ""
            if "width" in data:
                style += f" width: {int(100 * data['width'])}%;"
            if "height" in data:
                style += f" height: {int(100 * data['height'])}%;"
            return {
                "type": "container",
                "value": [],
                "style": style
            }

    obj = _board[pos]
    dye = _board.get_dyed(pos)
    primary_color = "--flag-color" if _board.get_type(pos) == "F" else "--foreground-color"
    if obj is None:
        cell_data = init_component({
            "type": "row",
            "children": []
        })
    else:
        cell_data = init_component({
            "type": "row",
            "children": obj.compose(_board)
        })
    if dye:
        # TODO 将(255, 255, 255) 改为 --foreground-color
        cell_data["style"] += " background-color: rgba(255, 255, 255, 0.296875); height: 100%; width: 100%;"
    VALUE = _board.get_config(pos.board_key, "VALUE")
    MINES = _board.get_config(pos.board_key, "MINES")
    if obj in [VALUE, MINES, None]:
        overlayText = ""
    else:
        overlayText = obj.type().decode("ascii")
    hightlight = []
    if obj is not None:
        for h_pos in set(h_pos for h_pos in obj.high_light(_board) if _board.in_bounds(h_pos)):
            hightlight.append({
                "x": h_pos.x,
                "y": h_pos.y,
                "boardname": h_pos.board_key,
            })
    cell_data = {
        "type": "" if obj is None else obj.type().decode("ascii"),
        "position": {
            "x": pos.x, "y": pos.y,
            "boardname": pos.board_key
        },
        "component": cell_data,
        "highlight": hightlight,
        "overlayText": overlayText
    }
    # import json
    # json_str = json.dumps(cell_data, separators=(",", ":"))
    # print(json_str)
    return cell_data


def format_board(_board, rule=""):
    if _board is None:
        return
    # board: Board
    board_data: dict = {
        "rules": rule,
        "boards": {},
        "cells": []
    }
    count = 0
    for key in _board.get_board_keys():
        board_data["boards"][key] = _board.get_config(key, "size")
        for pos, obj in _board():
            board_data["cells"].append(
                format_cell(_board, pos))
            count += 1
    board_data["count"] = count
    import json
    json_str = json.dumps(board_data, separators=(",", ":"))
    print(json_str)
    return board_data


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/metadata')
def generate_board():
    global hypothesis_data
    answer_board = None
    mask_board = None
    if mask_board:
        data = request.get_json()
        code = data.get("code", None)
        used_r = data.get("used_r", False)
        ultimate_mode = data.get("u_mode", "+A")

        total = data.get("code", -1)
        dye = data.get("dye", "")

        gamemode = data.get("mode", "EXPERT")
    else:
        # code: str = "bWFpbv8FBQP_P3z_Rnz_VnwB_0Z8_1Z8BP9GfP9WfAL_VnwC_1Z8BP9GfP9GfP9WfAL_Rnz_VnwG_0Z8_1Z8BP9WfAH_Rnz_Rnz_Rnz_VnwD_1Z8Af9WfAL_VnwD_1Z8Av9WfAL_Rnw=:0167b5ba"
        code = None
        gamemode = "ULTIMATE"
        ultimate_mode = 1
        total = 10
        used_r = True
        dye = "l"
        data = {"size": (10, 10)}
    mode = 1
    match gamemode:
        case "NORMAL":
            mode = 0
        case "EXPERT":
            mode = 1
        case "ULTIMATE":
            mode = 2
        case "PAZZLE":
            mode = 3
    print(mode)
    if code:
        code, mask = code.split(":", 1)
        print(code, mask)
        answer_board = decode_board(code, board_name)
        mask = int.from_bytes(bytes.fromhex(mask), "big", signed=False)
        mask_board = answer_board.clone()
        for pos, _ in answer_board():
            if mask & 1:
                mask_board[pos] = None
            mask >>= 1
        master_key = mask_board.get_board_keys()[0]
        size = mask_board.get_config(master_key, "size")
    else:
        size = data["size"]

    # rules = data["rules"]
    rules = ["3A"]
    hypothesis_data["summon"] = Summon(
        size, total, rules, used_r, dye
    )
    hypothesis_data["game"] = Game(
        summon=hypothesis_data["summon"],
        mode=mode,
        drop_r=not used_r,
        ultimate_mode=ultimate_mode
    )
    if code:
        hypothesis_data["game"].answer_board = answer_board
        hypothesis_data["game"].board = mask_board
    else:
        if mode < 3:
            try:
                hypothesis_data["game"].answer_board = hypothesis_data["summon"].summon_board()
                mask_board = hypothesis_data["game"].create_board()
            except:
                return jsonify({"error": "generate failed"}), 500
        else:
            try:
                mask_board = hypothesis_data["summon"].create_puzzle()
                ...
            except:
                return jsonify({"error": "generate failed"}), 500
            hypothesis_data["game"].answer_board = hypothesis_data["summon"].answer_board
        # answer_board = hypothesis_data["game"].answer_board
    # print(hypothesis_data)
    # print(answer_board.show_board())
    # hypothesis_data["game"].hint(wait=False)
    return format_board(mask_board)


@app.route('/api/click', methods=['POST'])
def click():
    global hypothesis_data
    data = request.get_json()
    refresh = {
        "cells": [],
        "gameover": False,
        "reason": ""
    }
    # print(data)
    # print(hypothesis_data)
    game: Game = hypothesis_data["game"]
    # print(game.deduced())
    # print(game.board.show_board())
    board = game.board.clone()
    pos = board.get_pos(data["x"], data["y"], data["boardName"])
    # if data["x"] == 0 and data["y"] == 0:
    #     print(hypothesis_data["game"].hint(wait=True))
    #     print(hypothesis_data["game"].deduced(wait=True))
    #     return {}
    if data["button"] == "left":
        _board = game.click(pos)
    elif data["button"] == "right":
        _board = game.mark(pos)
    else:
        _board = None
    # print("end click")
    # print(game.answer_board.show_board())
    if _board is None:
        if data["button"] == "left":
            refresh["reason"] = "你踩雷了"
        elif data["button"] == "right":
            refresh["reason"] = "你标记了一个错误的雷"
        refresh["gameover"] = True
    else:
        for pos, obj in _board():
            if obj is None and board[pos] is None:
                continue
            if (
                not (obj is None or board[pos] is None) and
                obj.type() == board[pos].type() and
                obj.code() == board[pos].code() and
                obj.high_light(_board) == board[pos].high_light(board)
            ):
                continue
            data = format_cell(_board, pos)
            refresh["cells"].append(data)
    refresh["success"] = False
    # print(refresh)
    # if _board:
    #     print(_board.show_board())
    #     print(game.deduced())
    #     print(game.last_hint[1])
    if refresh["cells"]:
        hypothesis_data["game"].hint(wait=False)
    return refresh, 200


@app.route('/api/click', methods=['POST'])
def hint_post():
    global hypothesis_data
    data = request.get_json()
    count = data.get("count", 0)
    game = hypothesis_data["game"]
    if count > 1:
        hint_list = game.hint(wait=True)
        min_length = min(len(tup[0]) for tup in hint_list)
        # 步骤2: 收集所有第一个列表长度等于最小长度的二元组
        hint_list = [tup for tup in hint_list if len(tup[0]) == min_length]
        count -= 1
    else:
        deduced_dict = game.deduced(wait=True)
        hint_list = [[], deduced_dict.values()]

    b_hint, t_hint = hint_list[count]
    # 由...
    b_hint: list[Union["AbstractPosition", list["AbstractRule", int]]]
    # 推出的坐标列表
    t_hint: list["AbstractPosition"]


@app.route('/api/rules', methods=['POST'])
def rule_list():
    from impl.rule import get_all_rules
    from impl.board.dye import get_all_dye
    return {
        "rules": get_all_rules(),   # {"L": {name: doc, ...}, "M": ..., "R": ...}
        "dye": get_all_dye()        # {name: doc, ...}
    }


if __name__ == '__main__':
    app.run(debug=True)
    # app.run()
