# @Author: weirdgiser
# @Date: 2025/1/10
# @Function:
from typing import List, Optional
from abc import ABC, abstractmethod
from pydantic import BaseModel
from pydantic.fields import Field


class InterpretResult(BaseModel):
    result: str = Field(description="解释结果")
    reason: Optional[str] = Field(description="解释原因")

class Chain(ABC):
    @abstractmethod
    def interpret(self, *args, **kwargs) -> InterpretResult:
        pass

class Engine(ABC):
    @abstractmethod
    def run(self, *args, **kwargs):
        pass
