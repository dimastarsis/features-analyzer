import asyncio
import aiohttp
from typing import Iterable
from tqdm.asyncio import tqdm
from .model import JsonData, KeAdminFlagInfo
from .constant import KEADMIN_API_URL
from .secret import KEADMIN_COOKIE


async def _fetch_keadmin(session: aiohttp.ClientSession, url: str, timeout=3) -> JsonData:
    headers = {"Cookie": KEADMIN_COOKIE}

    for i in range(timeout):
        try:
            async with session.get(url, headers=headers) as response:
                if response.status != 200:
                    text = await response.text()
                    raise aiohttp.ClientResponseError(
                        request_info=response.request_info,
                        history=response.history,
                        status=response.status,
                        message=f"Ошибка при загрузке {url}: {response.status}, {text}"
                    )
                return await response.json()
        except ConnectionError:
            pass

    raise ConnectionError(url)


async def find_feature(session: aiohttp.ClientSession, feature_name: str) -> int:
    return len(await _fetch_keadmin(session, f"{KEADMIN_API_URL}/Features?n={feature_name}"))


async def find_adjustments(session: aiohttp.ClientSession, feature_name: str) -> int:
    return (await _fetch_keadmin(
        session,
        f"{KEADMIN_API_URL}/Adjustments/GetAdjustments"
        f"?UserId=&Name={feature_name}&Value=&Download=false&GetOnlyIds=true"
    ))["amount"]


async def find_adjustments_new(session: aiohttp.ClientSession, feature_name: str) -> int:
    return (await _fetch_keadmin(session, f"{KEADMIN_API_URL}/AdjustmentsNew?n={feature_name}"))["TotalItemCount"]


async def limited_fetch_info(
    feature_name: str, session: aiohttp.ClientSession, semaphore: asyncio.Semaphore
) -> KeAdminFlagInfo | None:
    async with semaphore:
        feature_count = await find_feature(session, feature_name)
        return KeAdminFlagInfo(
            feature_name=feature_name,
            feature_count=feature_count,
            adjustments_count=await find_adjustments(session, feature_name),
            adjustments_new_count=await find_adjustments_new(session, feature_name)
        ) if feature_count != 0 else None


async def fetch_infos(feature_names: Iterable[str]) -> dict[str, KeAdminFlagInfo]:
    semaphore = asyncio.Semaphore(10)
    async with aiohttp.ClientSession() as session:
        tasks = [limited_fetch_info(feature_name, session, semaphore) for feature_name in feature_names]
        results = [await task for task in tqdm(
            asyncio.as_completed(tasks),
            total=len(tasks),
            desc="Загружаем информацию из keadmin"
        )]
        return {info.feature_name: info for info in results if info is not None}
