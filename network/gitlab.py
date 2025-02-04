import requests
from urllib.parse import quote
from .model import ProjectFile
from .constant import GITLAB_API_URL
from .secret import GITLAB_ACCESS_TOKEN


def get_project_id(project_name: str) -> int:
    url = f"{GITLAB_API_URL}/projects?search={quote(project_name)}"
    headers = {"PRIVATE-TOKEN": GITLAB_ACCESS_TOKEN}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise requests.exceptions.HTTPError(f"Ошибка при загрузке {url}: {response.status_code}, {response.text}")

    json_data = response.json()
    if json_data:
        return int(json_data[0]['id'])
    raise ValueError(response.text)


def fetch_file(project_file: ProjectFile) -> str:
    project_id = get_project_id(project_file.project_name)

    encoded_path = quote(project_file.file_path, safe='')
    url = f"{GITLAB_API_URL}/projects/{project_id}/repository/files/{encoded_path}/raw?ref={project_file.branch}"
    headers = {"PRIVATE-TOKEN": GITLAB_ACCESS_TOKEN}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise requests.exceptions.HTTPError(f"Ошибка при загрузке {url}: {response.status_code}, {response.text}")
    return response.text
