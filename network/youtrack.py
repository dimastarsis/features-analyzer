import json
from tqdm.asyncio import tqdm
from typing import Iterator, Union
from .model import YouTrackFlagInfo
from .constant import YOUTRACK_API_URL
from .secret import YOUTRACK_AUTHORIZATION
from .base import API


async def fetch_info(key: str, search_names: Iterator[str]) -> tuple[str, Union[YouTrackFlagInfo, None]]:
    for search_name in search_names:
        url = YOUTRACK_API_URL + (
            f"/sortedIssues?$top=-1&fields=tree(id,matches,ordered,parentId,summaryTextSearchResult("
            f"highlightRanges(endOffset,startOffset),textRange(endOffset,"
            f"startOffset)))&flatten=true&folderId=39-910&query="
            f"{search_name}&skipRoot=0&topRoot=101&unresolvedOnly=false"
        )
        headers = {'Authorization': YOUTRACK_AUTHORIZATION}

        response = await API.get(url, headers=headers)
        json_data = json.loads(response)

        if json_data:
            issues_count = len(json_data['tree'])
            if issues_count == 0:
                continue

            return key, YouTrackFlagInfo(
                feature_name=search_name,
                issues_count=issues_count
            )

        raise ValueError(response.text)

    return key, None


async def fetch_infos(search_names_map: dict[str, Iterator[str]]) -> dict[str, YouTrackFlagInfo]:
    tasks = [fetch_info(search_names_key, search_names_map[search_names_key]) for search_names_key in search_names_map]

    results = [await task for task in
               tqdm.as_completed(tasks, total=len(tasks), desc="Загружаем информацию из youtrack")]
    return {search_names_key: flag_info for search_names_key, flag_info in results if flag_info is not None}
