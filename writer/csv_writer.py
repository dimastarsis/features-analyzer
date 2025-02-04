import csv
from network.constant import FEATURES_V2_URL, CONFIG_URL, KEADMIN_URL
from analyzer.model import FeatureFlagV2AnalyzeResult
from .model import FeatureFlagV2RowData


def get_hyperlink(url: str, display_name: str) -> str:
    return f'=HYPERLINK("{url}";"{display_name}")'


def map_analyze_result(result: FeatureFlagV2AnalyzeResult) -> FeatureFlagV2RowData:
    property_url = FEATURES_V2_URL + f"#L{result.feature_v2_flag.line_number + 1}"
    config_flag_url = CONFIG_URL + f"#L{result.config_flag.line_number + 1}" if result.config_flag else None

    keadmin_feature_url: str = None
    keadmin_adjustments_url: str = None
    keadmin_adjustments_new_url: str = None
    if result.keadmin_info:
        keadmin_feature_url = KEADMIN_URL + f"/Features?n={result.keadmin_info.feature_name}"
        keadmin_adjustments_url = KEADMIN_URL + (f"/Adjustments?UserId=&Name={result.keadmin_info.feature_name}&Value"
                                                 "=&Download=false&GetOnlyIds=undefined")
        keadmin_adjustments_new_url = KEADMIN_URL + f"/AdjustmentsNew?n={result.keadmin_info.feature_name}"

    return FeatureFlagV2RowData(
        property_hyperlink=get_hyperlink(property_url, result.feature_v2_flag.property_name),
        consumer=result.feature_v2_flag.consumer,
        value_type=result.feature_v2_flag.value_type,
        config_flag_hyperlink=get_hyperlink(config_flag_url, result.config_flag.name) if result.config_flag else '-',
        config_value=result.config_flag.value if result.config_flag else '-',
        keadmin_feature_hyperlink=get_hyperlink(keadmin_feature_url, result.keadmin_info.feature_name) \
            if result.keadmin_info else '-',
        keadmin_adjustments_hyperlink=get_hyperlink(keadmin_adjustments_url, result.keadmin_info.adjustments_count) \
            if result.keadmin_info else '-',
        keadmin_adjustments_new_hyperlink=get_hyperlink(
            keadmin_adjustments_new_url, result.keadmin_info.adjustments_new_count
        ) if result.keadmin_info else '-'
    )


def write(results: list[FeatureFlagV2AnalyzeResult], filepath: str = "feature_flags.csv") -> None:
    with open(filepath, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        headers = [
            "FeatureFlagV2", "", "",
            "ClusterConfig", "",
            "KeAdmin", "", "",
        ]
        sub_headers = [
            "Name", "Consumer", "Value type",
            "Name", "Value",
            "Name", "Adjustments", "User settings"
        ]

        writer.writerow(headers)
        writer.writerow(sub_headers)

        for result in results:
            csv_data = map_analyze_result(result)
            writer.writerow(
                [
                    csv_data.property_hyperlink,
                    csv_data.consumer,
                    csv_data.value_type,
                    csv_data.config_flag_hyperlink,
                    csv_data.config_value,
                    csv_data.keadmin_feature_hyperlink,
                    csv_data.keadmin_adjustments_hyperlink,
                    csv_data.keadmin_adjustments_new_hyperlink
                ]
            )
