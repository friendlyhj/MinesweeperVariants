#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# @Time    : 2025/06/07 21:31
# @Author  : Wu_RH
# @FileName: solver.py
import threading

from ortools.sat.python import cp_model


class ModelManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._model = cp_model.CpModel()
                cls._instance._lock = threading.Lock()
            return cls._instance

    def get_model(self):
        with self._lock:
            return self._model

    def reset_model(self):
        with self._lock:
            # 创建新模型而不立即删除旧模型
            # 让垃圾回收器自动处理旧实例
            self._model = cp_model.CpModel()
            return self._model


# 使用示例
def get_model() -> cp_model.CpModel:
    return ModelManager().get_model()


def reset_model() -> cp_model.CpModel:
    return ModelManager().reset_model()