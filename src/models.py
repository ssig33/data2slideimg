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


class ImageData(BaseModel):
    url: str


class MapData(BaseModel):
    lat: float  # Latitude
    lon: float  # Longitude
    zoom: int = 14  # Zoom level (1-20, default 14)
    language: Optional[str] = "ja"  # Language code
    width: Optional[int] = 800  # Map image width
    height: Optional[int] = 600  # Map image height


class SlideRequest(BaseModel):
    title: Optional[str] = None
    textBlocks: Optional[List[TextBlock]] = None
    graph: Optional[GraphData] = None  # Single graph only
    table: Optional[TableData] = None
    image: Optional[ImageData] = None
    map: Optional[MapData] = None
    format: Optional[Literal["horizontal", "vertical"]] = "horizontal"