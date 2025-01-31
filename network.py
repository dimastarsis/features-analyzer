import os
import requests
from dotenv import load_dotenv
from urllib.parse import quote
from model import ProjectFile


load_dotenv(".env")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
BASE_URL = "https://git.skbkontur.ru"


def get_project_id(project_name: str) -> int:
    url = f"{BASE_URL}/api/v4/projects?search={quote(project_name)}"
    headers = {"PRIVATE-TOKEN": ACCESS_TOKEN}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise requests.exceptions.HTTPError(f"Ошибка: {response.status_code}, {response.text}")

    json_data = response.json()
    if json_data:
        return int(json_data[0]['id'])
    raise ValueError(response.text)


def fetch_gitlab_file(project_file: ProjectFile) -> str:
    project_id = get_project_id(project_file.project_name)

    encoded_path = quote(project_file.file_path, safe='')
    url = f"{BASE_URL}/api/v4/projects/{project_id}/repository/files/{encoded_path}/raw?ref={project_file.branch}"
    headers = {"PRIVATE-TOKEN": ACCESS_TOKEN}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise requests.exceptions.HTTPError(f"Ошибка при загрузке {url}: {response.status_code}, {response.text}")
    return response.text
