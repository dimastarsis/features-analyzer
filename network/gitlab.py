import json
from tqdm.asyncio import tqdm
from urllib.parse import quote
from .model import ProjectFile
from typing import Iterable
from .constant import GITLAB_API_URL
from .secret import GITLAB_ACCESS_TOKEN
from .base import API


async def get_project_id(project_name: str) -> int:
    url = f"{GITLAB_API_URL}/projects?search={quote(project_name)}"
    headers = {"PRIVATE-TOKEN": GITLAB_ACCESS_TOKEN}

    response = await API.get(url, headers=headers)
    json_data = json.loads(response)

    if json_data:
        return int(json_data[0]['id'])
    raise ValueError(response.text)


async def fetch_file(project_file: ProjectFile) -> tuple[ProjectFile, str]:
    project_id = await get_project_id(project_file.project_name)

    encoded_path = quote(project_file.file_path, safe='')
    url = f"{GITLAB_API_URL}/projects/{project_id}/repository/files/{encoded_path}/raw?ref={project_file.branch}"
    headers = {"PRIVATE-TOKEN": GITLAB_ACCESS_TOKEN}

    return project_file, await API.get(url, headers=headers)


async def fetch_files(*project_files: Iterable[ProjectFile]) -> Iterable[str]:
    tasks = [fetch_file(project_file) for project_file in project_files]

    results_map: dict[ProjectFile, str] = dict()
    for task in tqdm.as_completed(tasks, total=len(tasks), desc="Загружаем информацию из gitlab"):
        project_file, content = await task
        results_map[project_file] = content

    return (results_map[project_file] for project_file in project_files)
