import json
import requests
from .model import JsonData, KeAdminFlagInfo
from .constant import KEADMIN_API_URL
from .secret import KEADMIN_COOKIE


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


def get_keadmin_info(feature_name: str) -> KeAdminFlagInfo | None:
    feature_count = find_feature(feature_name)
    return KeAdminFlagInfo(
        feature_name=feature_name,
        feature_count=feature_count,
        adjustments_count=find_adjustments(feature_name),
        adjustments_new_count=find_adjustments_new(feature_name)
    ) if feature_count != 0 else None
