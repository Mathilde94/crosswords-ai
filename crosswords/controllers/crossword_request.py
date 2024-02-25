from pydantic import BaseModel
from typing import List

from crosswords.models.context import CrosswordContext


class CrosswordRequest(BaseModel):
    context: CrosswordContext
    concepts: List[str]


class CrosswordVerifyRequest(BaseModel):
    id: str
    matrix: List[List[str]]
