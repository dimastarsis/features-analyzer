from dataclasses import dataclass
from typing import Any


@dataclass
class ProjectFile:
    project_name: str
    file_path: str
    branch: str


@dataclass
class KeAdminFlagInfo:
    feature_name: str
    feature_count: int
    adjustments_count: int
    adjustments_new_count: int

    @property
    def empty(self) -> bool:
        return not (self.feature_count or self.adjustments_count or self.adjustments_new_count)


DictJsonData = dict[str, Any]
ListJsonData = list[Any]
JsonData = DictJsonData | ListJsonData
