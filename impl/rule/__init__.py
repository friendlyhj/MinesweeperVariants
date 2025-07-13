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

        if not any("Abstract" in b for b in bases_info):
            continue

        for stmt in node.body:
            if isinstance(stmt, ast.Assign):
                for target in stmt.targets:
                    if (
                        isinstance(target, ast.Name) and target.id == "name" and
                        isinstance(stmt.value, ast.Str)
                    ):
                        name_val = stmt.value.s.strip()
                        if name_val:
                            return module_doc
    return None


def scan_module_docstrings(directory):
    results = []
    for root, _, files in os.walk(directory):
        for name in files:
            if name.endswith('.py'):
                path = os.path.join(root, name)
                doc = extract_module_docstring(path)
                parent_dir_name = os.path.basename(os.path.dirname(path))  # 上级目录名
                results.append((parent_dir_name, doc))
    return results


def get_all_rules():
    results = {"R": [], "M": [], "L": []}
    dir_path = os.path.dirname(os.path.abspath(__file__))
    for path, doc in scan_module_docstrings(dir_path):  # 替换路径
        if doc is None:
            continue
        if path == "Rrule":
            results["R"].append(f'{doc}')
        if path == "Mrule":
            results["M"].append(f'{doc}')
        if path == "Lrule":
            results["L"].append(f'{doc}')
    return results
