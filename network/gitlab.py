import json
from tqdm.asyncio import tqdm
from urllib.parse import quote
from .model import GitLabFileReference, GitLabFile
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


async def fetch_file(file_ref: GitLabFileReference) -> GitLabFile:
    project_id = await get_project_id(file_ref.project_name)

    encoded_path = quote(file_ref.file_path, safe='')
    url = f"{GITLAB_API_URL}/projects/{project_id}/repository/files/{encoded_path}/raw?ref={file_ref.branch}"
    headers = {"PRIVATE-TOKEN": GITLAB_ACCESS_TOKEN}

    return GitLabFile(file_ref, project_id, content=await API.get(url, headers=headers))


async def fetch_files(*file_refs: Iterable[GitLabFileReference]) -> Iterable[GitLabFile]:
    tasks = [fetch_file(file_ref) for file_ref in file_refs]

    results_map: dict[GitLabFileReference, GitLabFile] = dict()
    for task in tqdm.as_completed(tasks, total=len(tasks), desc="Загружаем информацию из gitlab"):
        file = await task
        results_map[file.reference] = file  # todo поаккуратнее

    return (results_map[file_ref] for file_ref in file_refs)
