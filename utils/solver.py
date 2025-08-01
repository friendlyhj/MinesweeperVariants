#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# @Time    : 2025/06/07 21:31
# @Author  : Wu_RH
# @FileName: solver.py

import gc
import threading

from ortools.sat.python import cp_model

MODEL = None
model_lock = threading.Lock()


def get_model() -> cp_model.CpModel:
    global MODEL
    if MODEL is None:
        with model_lock:
            MODEL = reset_model()
    return MODEL


def reset_model() -> cp_model.CpModel:
    global MODEL
    with model_lock:
        del MODEL
        gc.collect()
        MODEL = cp_model.CpModel()
        return MODEL
