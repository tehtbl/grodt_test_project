from .index import index
from .mynewappmodel import (
    MyNewAppModelCreateView,
    MyNewAppModelDeleteView,
    MyNewAppModelDetailView,
    MyNewAppModelListView,
    MyNewAppModelUpdateView,
)

__all__ = [
    "index",
    "MyNewAppModelCreateView", "MyNewAppModelDetailView", "MyNewAppModelUpdateView", "MyNewAppModelDeleteView", "MyNewAppModelListView",
]
