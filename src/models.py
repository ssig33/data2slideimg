from typing import List, Optional, Literal
from pydantic import BaseModel


class TextBlock(BaseModel):
    text: str


class GraphData(BaseModel):
    type: Literal["bar", "line", "pie"]
    data: List[float]
    labels: List[str]


class TableData(BaseModel):
    headers: List[str]
    rows: List[List[str]]


class SlideRequest(BaseModel):
    title: Optional[str] = None
    textBlocks: Optional[List[TextBlock]] = None
    graph: Optional[GraphData] = None  # Single graph only
    table: Optional[TableData] = None