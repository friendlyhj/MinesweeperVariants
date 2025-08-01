#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# @Time    : 2025/06/03 04:23
# @Author  : Wu_RH
# @FileName: __init__.py

import os
import ast


def extract_module_docstring(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            source = f.read()
    except Exception:
        return None

    try:
        tree = ast.parse(source, filename=filepath)
    except SyntaxError:
        return None

    module_doc = ast.get_docstring(tree)
    if module_doc is None:
        return None

    for node in ast.walk(tree):
        if not isinstance(node, ast.ClassDef):
            continue

        bases_info = []
        for base in node.bases:
            if isinstance(base, ast.Name):
                bases_info.append(base.id)
            elif isinstance(base, ast.Attribute):
                bases_info.append(base.attr)
            else:
                bases_info.append(str(base))

        x = 0
        if any("MinesRule" in b for b in bases_info):
            x |= 1
        if any("MinesClueRule" in b for b in bases_info):
            x |= 2
        if any("ClueRule" in b for b in bases_info):
            x |= 4

        if x == 6:
            x = 2

        for stmt in node.body:
            if isinstance(stmt, ast.Assign):
                for target in stmt.targets:
                    if (
                        isinstance(target, ast.Name) and target.id == "name" and
                        isinstance(stmt.value, ast.Str)
                    ):
                        name_val = stmt.value.s.strip()
                        if name_val:
                            return module_doc, x, name_val
    return None


def scan_module_docstrings(directory):
    results = []
    for root, _, files in os.walk(directory):
        for name in files:
            if name.endswith('.py'):
                path = os.path.join(root, name)
                pck = extract_module_docstring(path)
                if pck is None:
                    continue
                doc, x, name = pck
                results.append((doc, x, name))
    return results


def get_all_rules():
    results = {"R": {}, "M": {}, "L": {}}
    dir_path = os.path.dirname(os.path.abspath(__file__))
    for doc, x, name in scan_module_docstrings(dir_path):  # 替换路径
        if x == 0:
            continue
        if x == 1:
            results["L"][name] = f'{doc}'
        if x == 2:
            results["M"][name] = f'{doc}'
        if x == 4:
            results["R"][name] = f'{doc}'
    return results
