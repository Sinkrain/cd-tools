# -*- coding:utf-8 -*-

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any


class BaseHandler(ABC):
    
    @abstractmethod
    def pre_check(self) -> None:
        pass

    @abstractmethod
    def update_value(self, d_mf: Any, value: Any) -> None:
        pass

    @abstractmethod
    def notes(self) -> None:
        pass
