from dataclasses import dataclass
from typing import Any


@dataclass
class ProjectFile:
    project_name: str
    file_path: str
    branch: str


DictJsonData = dict[str, Any]
ListJsonData = list[Any]
JsonData = DictJsonData | ListJsonData
