import csv
from dataclasses import fields
from network.constant import GITLAB_URL, KEADMIN_URL, YOUTRACK_URL
from network.model import GitLabFile
from analyzer.model import FeatureFlagV2AnalyzeResult
from .model import FeatureFlagV2RowData


def get_hyperlink(url: str, display_name: str) -> str:
    return f'=HYPERLINK("{url}";"{display_name}")'


def map_analyze_result(
    result: FeatureFlagV2AnalyzeResult,
    features_v2_file: GitLabFile,
    config_file: GitLabFile,
) -> FeatureFlagV2RowData:
    property_url = GITLAB_URL + (f"/search?search={result.feature_v2_flag.property_name}"
                                 f"&nav_source=navbar&project_id={features_v2_file.project_id}"
                                 f"&search_code=true&repository_ref={features_v2_file.reference.branch}")
    youtrack_issues_url = YOUTRACK_URL + f"/issues/Flag?q={result.feature_v2_flag.youtrack_search_name}"

    config_flag_url: str = None
    if result.config_flag:
        config_flag_url = GITLAB_URL + (f"/search?search={result.config_flag.name}"
                                        f"&nav_source=navbar&project_id={config_file.project_id}"
                                        f"&search_code=true&repository_ref={config_file.reference.branch}")

    keadmin_feature_url: str = None
    keadmin_adjustments_url: str = None
    keadmin_adjustments_new_url: str = None
    if result.keadmin_info:
        keadmin_feature_url = KEADMIN_URL + f"/Features?n={result.keadmin_info.feature_name}"
        keadmin_adjustments_url = KEADMIN_URL + (f"/Adjustments?UserId=&Name={result.keadmin_info.feature_name}&Value"
                                                 "=&Download=false&GetOnlyIds=undefined")
        keadmin_adjustments_new_url = KEADMIN_URL + f"/AdjustmentsNew?n={result.keadmin_info.feature_name}"

    return FeatureFlagV2RowData(
        property_name=result.feature_v2_flag.property_name,
        property_search_hyperlink=get_hyperlink(property_url, "ссылка"),
        consumer=result.feature_v2_flag.consumer,
        property_type=result.feature_v2_flag.value_type,
        config_flag_name=result.config_flag.name if result.config_flag else '-',
        config_search_hyperlink=get_hyperlink(config_flag_url, "ссылка") if result.config_flag else '-',
        config_value=result.config_flag.value if result.config_flag else '-',
        keadmin_feature_name=result.keadmin_info.feature_name if result.keadmin_info else '-',
        keadmin_features_hyperlink=get_hyperlink(keadmin_feature_url, result.keadmin_info.feature_count) \
            if result.keadmin_info else '-',
        keadmin_adjustments_hyperlink=get_hyperlink(keadmin_adjustments_url, result.keadmin_info.adjustments_count) \
            if result.keadmin_info else '-',
        keadmin_adjustments_new_hyperlink=get_hyperlink(
            keadmin_adjustments_new_url, result.keadmin_info.adjustments_new_count
        ) if result.keadmin_info else '-',
        youtrack_hyperlink=get_hyperlink(youtrack_issues_url, "ссылка")
    )


def write_csv(
    results: list[FeatureFlagV2AnalyzeResult],
    features_v2_file: GitLabFile,
    config_file: GitLabFile,
    filepath: str = "feature_flags.csv"
) -> None:
    with open(filepath, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        headers = [
            "FeatureFlagV2", "", "", "",
            "ClusterConfig", "", "",
            "KeAdmin", "", "", "",
            "YouTrack",
        ]
        sub_headers = [
            "Название", "Ссылка", "Consumer", "Тип",
            "Название", "Ссылка", "Значение",
            "Название", "Features", "Настройки пользователей", "Adjustments",
            "Issues",
        ]

        writer.writerow(headers)
        writer.writerow(sub_headers)

        for result in results:
            csv_data = map_analyze_result(result, features_v2_file, config_file)
            writer.writerow(list((getattr(csv_data, field.name) for field in fields(csv_data))))
