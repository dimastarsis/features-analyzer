import json
from typing import Iterable
from tqdm.asyncio import tqdm
from .model import JsonData, KeAdminFlagInfo
from .constant import KEADMIN_API_URL
from .secret import KEADMIN_COOKIE
from .base import API


async def _fetch_keadmin(url: str) -> JsonData:
    headers = {"Cookie": KEADMIN_COOKIE}
    response = await API.get(url, headers=headers)
    return json.loads(response)


async def find_feature(feature_name: str) -> int:
    return len(await _fetch_keadmin(f"{KEADMIN_API_URL}/Features?n={feature_name}"))


async def find_adjustments(feature_name: str) -> int:
    return (await _fetch_keadmin(
        f"{KEADMIN_API_URL}/Adjustments/GetAdjustments"
        f"?UserId=&Name={feature_name}&Value=&Download=false&GetOnlyIds=true"
    ))["amount"]


async def find_adjustments_new(feature_name: str) -> int:
    return (await _fetch_keadmin(f"{KEADMIN_API_URL}/AdjustmentsNew?n={feature_name}"))["TotalItemCount"]


async def fetch_info(feature_name: str) -> KeAdminFlagInfo | None:
    feature_count = await find_feature(feature_name)
    return KeAdminFlagInfo(
        feature_name=feature_name,
        feature_count=feature_count,
        adjustments_count=await find_adjustments(feature_name),
        adjustments_new_count=await find_adjustments_new(feature_name)
    ) if feature_count != 0 else None


async def fetch_infos(feature_names: Iterable[str]) -> dict[str, KeAdminFlagInfo]:
    tasks = [fetch_info(feature_name) for feature_name in feature_names]
    results = [await task for task in
               tqdm.as_completed(tasks, total=len(tasks), desc="Загружаем информацию из keadmin")]
    return {info.feature_name: info for info in results if info is not None}
