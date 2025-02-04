from dataclasses import dataclass
from typing import Any
import re
from .constant import GITLAB_URL


@dataclass
class ProjectFile:
    group: str | None
    project_name: str
    file_path: str
    branch: str

    @staticmethod
    def parse(url: str) -> 'ProjectFile':
        pattern = re.compile(
            rf"{re.escape(GITLAB_URL)}/"  # Экранируем URL
            r"(?P<group>[^/]+(?:/[^/]+)*/)?"  # Необязательная группа
            r"(?P<project>[^/]+)/-/blob/"  # Имя проекта
            r"(?P<branch>[^/]+)/"  # Ветка
            r"(?P<file_path>.+)"  # Путь до файла
        )

        match = pattern.match(url)
        if not match:
            raise ValueError(url)

        return ProjectFile(
            match.group("group"),
            match.group("project"),
            match.group("file_path"),
            match.group("branch")
        )


@dataclass
class KeAdminFlagInfo:
    feature_name: str
    feature_count: int
    adjustments_count: int
    adjustments_new_count: int


DictJsonData = dict[str, Any]
ListJsonData = list[Any]
JsonData = DictJsonData | ListJsonData
