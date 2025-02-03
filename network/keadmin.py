import json
import requests
from . import KEADMIN_COOKIE
from .model import JsonData
from .constant import KEADMIN_API_URL


def _fetch_keadmin(url: str) -> JsonData:
    headers = {"Cookie": KEADMIN_COOKIE}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise requests.exceptions.HTTPError(f"Ошибка при загрузке {url}: {response.status_code}, {response.text}")

    return json.loads(response.text)


def find_feature(feature_name: str) -> int:
    return len(_fetch_keadmin(f"{KEADMIN_API_URL}/Features?n={feature_name}"))


def find_adjustments(feature_name: str) -> int:
    return _fetch_keadmin(
        f"{KEADMIN_API_URL}/Adjustments/GetAdjustments"
        f"?UserId=&Name={feature_name}&Value=&Download=false&GetOnlyIds=true"
    )["amount"]


def find_adjustments_new(feature_name: str) -> int:
    return _fetch_keadmin(f"{KEADMIN_API_URL}/AdjustmentsNew?n={feature_name}")["TotalItemCount"]
