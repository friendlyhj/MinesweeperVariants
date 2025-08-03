#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# @Time    : 2025/07/30 08:15
# @Author  : Wu_RH
# @FileName: app.py.py
import threading
from pathlib import Path
from typing import Union

from flask import jsonify, request, redirect
import webbrowser
from flask_cors import CORS
import sys

from abs.board import AbstractPosition
from abs.rule import AbstractRule
from impl.summon.game import GameSession as Game
from impl.summon.summon import Summon
from impl.impl_obj import decode_board
from flask import Flask
import os
from datetime import datetime, timedelta

# 添加项目路径到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入项目核心模块

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
hypothesis_data = dict()
github_web = "https://koolshow.github.io"


def format_cell(_board, pos, hint=0):
    def init_component(data) -> dict:
        if data["type"] in ["col", "row"]:
            style = "display: flex; "
            if data["type"] == "col":
                # 垂直布局：主轴垂直方向，交叉轴居中
                style += "flex-direction: column;"
                # 子项高度平均分配（使用 flex-grow 实现）
                for child in data["children"]:
                    child_style = init_component(child).get("style", "")
                    if "flex-grow" not in child_style:
                        child_style += " flex-grow: 1;"
            else:
                # 水平布局：主轴水平方向，交叉轴居中
                style += "flex-direction: row;"
                # 子项宽度平均分配（使用 flex-grow 实现）
                for child in data["children"]:
                    child_style = init_component(child).get("style", "")
                    if "flex-grow" not in child_style:
                        child_style += " flex-grow: 1;"
            style += " align-items: center; justify-content: center; gap: 5%;"
            style += " width: 100%; height: 100%;"
            return {
                "type": "container",
                "value": [init_component(i) for i in data["children"]],
                "style": style
            }

        elif data["type"] == "text":
            # 文本项：使用 flex 布局填充可用空间，添加溢出处理
            style = f"fill: var({primary_color}); text-align: center;"
            style += " display: flex; justify-content: center; align-items: center;"
            style += " flex: 1; min-width: 0; max-width: 100;"  # 关键：允许内容收缩
            style += " overflow: hidden; text-overflow: ellipsis; white-space: nowrap;"

            return {
                "type": "text",
                "value": data.get("text", ""),
                "style": style
            }

        elif data["type"] == "image":
            path = data.get("image")
            # 图片项：保持比例，居中显示
            return {
                "type": "assets",
                "value": path,
                "style": f"fill: var({primary_color}); flex: 1; min-width: 0;"
            }

        elif data["type"] == "placeholder":
            style = "flex-shrink: 0;"  # 防止占位符被压缩

            if "width" in data:
                # 行内容器中使用固定宽度
                style += f" width: {int(100 * data['width'])}%;"
            if "height" in data:
                # 列内容器中使用固定高度
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
        if hint == 2:
            cell_data = init_component({
                "type": "row",
                "children": [{
                    "type": "text",
                    "text": "!"
                }]
            })
        else:
            cell_data = init_component({
                "type": "row",
                "children": []
            })
    else:
        # print(obj.compose(_board, True))
        cell_data = init_component({
            "type": "row",
            "children": [obj.compose(_board, True)]
        })
    if dye:
        # TODO 将(255, 255, 255) 改为 --foreground-color
        cell_data["style"] += " background-color: rgba(255, 255, 255, 0.296875);"
    if hint == 1:
        cell_data["style"] += " background-color: rgba(255, 255, 0, 0.296875);"
    if hint == 2:
        cell_data["style"] += " background-color: rgba(0, 255, 0, 0.296875);"
    cell_data["style"] += " width: 100%; height: 100%; align-items: center; justify-content: center;"
    VALUE = _board.get_config(pos.board_key, "VALUE")
    MINES = _board.get_config(pos.board_key, "MINES")
    if obj in [VALUE, MINES, None]:
        overlayText = ""
    else:
        overlayText = obj.type().decode("ascii")
    # hightlight = [{
    #             "x": pos.x,
    #             "y": pos.y,
    #             "boardname": pos.board_key,
    #         }]
    hightlight = {pos.board_key: [[pos.x, pos.y]]}
    if obj is not None:
        for h_pos in set(h_pos for h_pos in obj.high_light(_board) if _board.in_bounds(h_pos)):
            # hightlight.append({
            #     "x": h_pos.x,
            #     "y": h_pos.y,
            #     "boardname": h_pos.board_key,
            # })
            if h_pos.board_key not in hightlight:
                hightlight[h_pos.board_key] = []
            hightlight[h_pos.board_key].append([h_pos.x, h_pos.y])
    cell_data = {
        "type": "" if obj is None else obj.type().decode("ascii"),
        "position": {
            "x": pos.x, "y": pos.y,
            "boardname": pos.board_key
        },
        "component": cell_data,
        "highlight": hightlight,
        "clickable": True,
        "overlayText": overlayText
    }
    # import json
    # json_str = json.dumps(cell_data, separators=(",", ":"))
    # print(json_str)
    return cell_data


def format_board(_board):
    if _board is None:
        return
    # board: Board
    board_data: dict = {
        "boards": {},
        "cells": [],
    }
    count = 0
    for key in _board.get_board_keys():
        board_data["boards"][key] = _board.get_config(key, "size")
        for pos, obj in _board():
            # continue
            # if obj is None:
            #     continue
            board_data["cells"].append(
                format_cell(_board, pos))
            count += 1
    board_data["count"] = count
    import json
    json_str = json.dumps(board_data, separators=(",", ":"))
    print(json_str)
    return board_data


@app.route('/')
def root():
    return redirect("https://koolshow.github.io/MinesweeperVariants-Vue/")


@app.route('/api/new')
def generate_board():
    global hypothesis_data
    from impl.summon.game import NORMAL, EXPERT, ULTIMATE, PUZZLE
    from impl.summon.game import ULTIMATE_R, ULTIMATE_S, ULTIMATE_F, ULTIMATE_A
    # from utils.tool import get_random
    # get_random(new=True, seed=8205162)
    answer_board = None
    mask_board = None
    code = request.args.get("code", None)
    used_r = request.args.get("used_r", "true").lower() == "true"
    rules = request.args.get("rules", "V").split(",")
    ultimate_mode = request.args.get("u_mode", "+A")
    total = int(request.args.get("total", -1))
    dye = request.args.get("dye", "")
    gamemode = request.args.get("mode", "EXPERT")
    mode = 1
    match gamemode:
        case "NORMAL":
            mode = NORMAL
        case "EXPERT":
            mode = EXPERT
        case "ULTIMATE":
            mode = ULTIMATE
        case "PAZZLE":
            mode = PUZZLE
    u_mode = 0
    if "+A" in ultimate_mode:
        u_mode |= ULTIMATE_A
    if "+F" in ultimate_mode:
        u_mode |= ULTIMATE_F
    if "+S" in ultimate_mode:
        u_mode |= ULTIMATE_S
    if "+R" in ultimate_mode:
        u_mode |= ULTIMATE_R

    # print(mode)
    # print(123456)
    if code:
        code, mask = code.split(":", 1)
        # print(code, mask)
        answer_board = decode_board(code, None)
        mask = int.from_bytes(bytes.fromhex(mask), "big", signed=False)
        mask_board = answer_board.clone()
        for pos, _ in answer_board():
            if mask & 1:
                mask_board[pos] = None
            mask >>= 1
        master_key = mask_board.get_board_keys()[0]
        size = mask_board.get_config(master_key, "size")
    else:
        size = [int(i) for i in request.args.get("size", None).split("x")]

    hypothesis_data["summon"] = Summon(
        size, total, rules, used_r, dye
    )
    hypothesis_data["game"] = Game(
        summon=hypothesis_data["summon"],
        mode=mode,
        drop_r=not used_r,
        ultimate_mode=u_mode
    )
    if code:
        hypothesis_data["game"].answer_board = answer_board
        hypothesis_data["game"].board = mask_board
    else:
        # print(2)
        if mode < 3:
            try:
                hypothesis_data["game"].answer_board = hypothesis_data["summon"].summon_board()
                mask_board = hypothesis_data["game"].create_board()
                print(123456)
            except:
                return jsonify({"error": "generate failed"}), 500
            answer_board = hypothesis_data["game"].answer_board
            print(answer_board)
        else:
            try:
                mask_board = hypothesis_data["summon"].create_puzzle()
            except:
                return jsonify({"error": "generate failed"}), 500
            hypothesis_data["game"].answer_board = hypothesis_data["summon"].answer_board
            answer_board = hypothesis_data["summon"].answer_board
    if dye:
        rules += [f"@{dye}"]
        # answer_board = hypothesis_data["game"].answer_board
    # print(hypothesis_data)
    # print(answer_board.show_board())
    hypothesis_data["game"].deduced(wait=False)
    hypothesis_data["rules"] = rules[:]
    board_data = format_board(mask_board)
    board_data["rules"] = hypothesis_data["rules"]
    remains = [-1, -1, 0]
    remains[2] = len([_ for _ in mask_board("N")])
    if not hypothesis_data["game"].drop_r:
        remains[0] = len([_ for _ in mask_board("F")])
        remains[1] = len([_ for pos, _ in answer_board("F") if mask_board.get_type(pos) == "N"])
    else:
        remains[0] = "*"
        remains[1] = "*"
    board_data["remains"] = remains
    return jsonify(board_data)


@app.route('/api/metadata')
def metadata():
    if "game" in hypothesis_data:
        board = hypothesis_data["game"].board
        a_board = hypothesis_data["game"].answer_board
        board_data = format_board(board)
        remains = [-1, -1, 0]
        remains[2] = str(len([_ for _ in board("N")]))
        if not hypothesis_data["game"].drop_r:
            remains[0] = len([_ for _ in board("F")])
            remains[1] = len([_ for pos, _ in a_board("F") if board.get_type(pos) == "N"])
        else:
            remains[0] = "*"
            remains[1] = "*"
        board_data["rules"] = hypothesis_data["rules"]
        board_data["remains"] = remains
        return jsonify(board_data)
    return {}


@app.route('/api/click', methods=['POST'])
def click():
    global hypothesis_data
    data = request.get_json()
    refresh = {
        "cells": [],
        "gameover": False,
        "reason": ""
    }
    print(data)
    # print(hypothesis_data)
    game: Game = hypothesis_data["game"]
    # print(game.deduced())
    print(game.board.show_board())
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
    print("end click")
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
            print(pos, obj, data)
            refresh["cells"].append(data)
    refresh["success"] = True
    print(game.board)
    # print(game.deduced())
    # print(game.hint())
    # print(refresh)
    # if _board:
    #     print(_board.show_board())
    #     print(game.deduced())
    #     print(game.last_hint[1])
    hypothesis_data["game"].deduced(wait=False)
    a_board = hypothesis_data["game"].answer_board
    remains = [-1, -1, 0]
    remains[2] = len([_ for _ in board("N")])
    if not hypothesis_data["game"].drop_r:
        remains[0] = len([_ for _ in board("F")])
        remains[1] = len([_ for pos, _ in a_board("F") if board.get_type(pos) == "N"])
    else:
        remains[0] = "*"
        remains[1] = "*"
    refresh["remains"] = remains
    print("refresh: " + str(refresh))
    return refresh, 200


@app.route('/api/hint', methods=['GET'])
def hint_post():
    global hypothesis_data
    count = int(request.args.get("count", 0))
    game = hypothesis_data["game"]
    hint_list = game.hint(wait=True)
    for hint in hint_list:
        print(hint[0], "->", hint[1])
    print("hint end")
    # return {}, 200  # 格式和click返回应一样
    print(count)
    if count > 1:
        hint_list = game.hint(wait=True)
        min_length = min(len(tup[0]) for tup in hint_list)
        # 步骤2: 收集所有第一个列表长度等于最小长度的二元组
        hint_list = [tup for tup in hint_list if len(tup[0]) == min_length]
        count -= 1
    else:
        deduced_dict = game.deduced(wait=True)
        hint_list = [([], list(deduced_dict.keys()))]

    count -= 1

    print(hint_list)
    print(hint_list[count])
    b_hint, t_hint = hint_list[count]
    # 由...
    b_hint: list[Union["AbstractPosition", list["AbstractRule", int]]]
    # 推出的坐标列表
    t_hint: list["AbstractPosition"]
    print(b_hint, "->", t_hint)
    cell_data = [format_cell(game.board, p, hint=1) for p in b_hint]
    cell_data += [format_cell(game.board, p, hint=2) for p in t_hint]
    return jsonify({"cells": cell_data}), 200


@app.route('/api/rules', methods=['GET'])
def get_rule_list():
    from impl.rule import get_all_rules
    from impl.board.dye import get_all_dye
    all_rules = get_all_rules()
    rules_info = {}
    for key in ["L", "M", "R"]:
        for name in all_rules[key]:
            unascii_name = [n for n in all_rules[key][name]["names"] if not n.isascii()]
            zh_name = unascii_name[0] if unascii_name else ""
            rules_info[name] = [
                key.lower() + "Rule",
                zh_name,
                all_rules[key][name]["doc"]
            ]
    return {
        "rules": rules_info,
        "dye": get_all_dye()  # {dye_name: doc, ...}
    }

##

# def generate_self_signed_cert():
#     # 自动生成自签名证书函数
#     from cryptography.hazmat.backends import default_backend
#     from cryptography.hazmat.primitives import serialization, hashes
#     from cryptography.hazmat.primitives.asymmetric import rsa
#     from cryptography import x509

#     # 生成私钥
#     private_key = rsa.generate_private_key(
#         public_exponent=65537,
#         key_size=2048,
#         backend=default_backend()
#     )

#     # 生成证书主体
#     subject = issuer = x509.Name([
#         x509.NameAttribute(x509.NameOID.COUNTRY_NAME, "US"),
#         x509.NameAttribute(x509.NameOID.STATE_OR_PROVINCE_NAME, "California"),
#         x509.NameAttribute(x509.NameOID.LOCALITY_NAME, "San Francisco"),
#         x509.NameAttribute(x509.NameOID.ORGANIZATION_NAME, "My Company"),
#         x509.NameAttribute(x509.NameOID.COMMON_NAME, "localhost"),
#     ])

#     cert = (
#         x509.CertificateBuilder()
#         .subject_name(subject)
#         .issuer_name(issuer)
#         .public_key(private_key.public_key())
#         .serial_number(x509.random_serial_number())
#         .not_valid_before(datetime.utcnow())
#         .not_valid_after(datetime.utcnow() + timedelta(days=365))
#         .add_extension(
#             x509.SubjectAlternativeName([x509.DNSName("localhost")]),
#             critical=False
#         )
#         .sign(private_key, hashes.SHA256(), default_backend())
#     )

#     # 保存证书和私钥到文件
#     with open("cert.pem", "wb") as f:
#         f.write(cert.public_bytes(serialization.Encoding.PEM))
#     with open("key.pem", "wb") as f:
#         f.write(private_key.private_bytes(
#             encoding=serialization.Encoding.PEM,
#             format=serialization.PrivateFormat.TraditionalOpenSSL,
#             encryption_algorithm=serialization.NoEncryption()
#         ))

##

if __name__ == '__main__':
    port = int(sys.argv[1] if len(sys.argv) == 2 else "5050")
    # 允许所有来源跨域，或根据需要设置 origins=["*"]

    # threading.Thread(target=lambda: webbrowser.open(f"http://localhost:{port}", new=2)).start()
    app.run(
        host='0.0.0.0',
        port=port,
        # debug=True
    )
