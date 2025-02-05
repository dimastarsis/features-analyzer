import json
from tqdm.asyncio import tqdm
from typing import Iterable
from .model import YouTrackFlagInfo
from .constant import YOUTRACK_API_URL
from .secret import YOUTRACK_AUTHORIZATION
from .base import API


async def fetch_info_old(feature_name: str) -> YouTrackFlagInfo | None:
    url = YOUTRACK_API_URL + "/issuesGetter/count?$top=-1&fields=count"
    headers = {
        'Authorization': YOUTRACK_AUTHORIZATION,
        'Referer': f'https://yt.skbkontur.ru/issues/Flag?q={feature_name}',
    }
    json_data = {
        'folder': {
            '$type': 'Project',
            'id': '39-910',
        },
        'query': feature_name,
        'unresolvedOnly': False,
    }

    response = await API.post(url, headers=headers, json_data=json_data)
    json_data = json.loads(response)

    if json_data:
        issues_count = int(json_data['count'])
        if issues_count == -1:
            raise ConnectionRefusedError("Авторизация на youtrack протухла")

        return YouTrackFlagInfo(
            feature_name=feature_name,
            issues_count=issues_count
        ) if issues_count != 0 else None

    raise ValueError(response.text)


async def fetch_info(feature_name: str) -> YouTrackFlagInfo | None:
    url = YOUTRACK_API_URL + (
        f"/sortedIssues?$top=-1&fields=tree(id,matches,ordered,parentId,summaryTextSearchResult("
        f"highlightRanges(endOffset,startOffset),textRange(endOffset,"
        f"startOffset)))&flatten=true&folderId=39-910&query="
        f"{feature_name}&skipRoot=0&topRoot=101&unresolvedOnly=false"
    )
    headers = {
        'Authorization': YOUTRACK_AUTHORIZATION,
    }

    response = await API.get(url, headers=headers)
    json_data = json.loads(response)

    if json_data:
        issues_count = len(json_data['tree'])

        return YouTrackFlagInfo(
            feature_name=feature_name,
            issues_count=issues_count
        ) if issues_count != 0 else None

    raise ValueError(response.text)


async def fetch_infos(search_names: Iterable[str]) -> dict[str, YouTrackFlagInfo]:
    tasks = [fetch_info(search_name) for search_name in search_names]

    results = [await task for task in
               tqdm.as_completed(tasks, total=len(tasks), desc="Загружаем информацию из youtrack")]
    return {result.feature_name: result for result in results if result is not None}
