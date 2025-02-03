import csv
from dataclasses import asdict
from model import CSVFeatureFlagV2Record
from typing import List

from network.model import KeAdminFlagInfo
from parser.model import FeatureFlagV2, ConfigFlag


def write_excel_feature_flags_to_csv(filepath: str, flags: List[CSVFeatureFlagV2Record]):
    with open(filepath, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        # Заголовок с секциями
        headers = [
            "FeatureFlagV2", "", "", "", "", "",
            "ConfigFlag", "", "", "",
            "KeAdminFlagInfo", "", "", ""
        ]
        sub_headers = [
            "global_name", "consumer_name", "consumer", "property_name", "value_type", "line_number",
            "prefix", "name", "value", "line_number",
            "feature_name", "feature_count", "adjustments_count", "adjustments_new_count"
        ]

        # Записываем шапку с секциями
        writer.writerow(headers)
        writer.writerow(sub_headers)

        # Записываем данные
        for flag in flags:
            row = [
                flag.feature_v2_flag.global_name,
                flag.feature_v2_flag.consumer_name,
                flag.feature_v2_flag.consumer,
                flag.feature_v2_flag.property_name,
                flag.feature_v2_flag.value_type,
                flag.feature_v2_flag.line_number,

                flag.config_flag.prefix if flag.config_flag else "",
                flag.config_flag.name if flag.config_flag else "",
                flag.config_flag.value if flag.config_flag else "",
                flag.config_flag.line_number if flag.config_flag else "",

                flag.keadmin_info.feature_name,
                flag.keadmin_info.feature_count,
                flag.keadmin_info.adjustments_count,
                flag.keadmin_info.adjustments_new_count
            ]
            writer.writerow(row)

# Пример вызова
flags = [
    CSVFeatureFlagV2Record(
        feature_v2_flag=FeatureFlagV2('=HYPERLINK("http://example.com", "Документация")', "ConsumerX", "KeAbon", "MyFeature", "bool", 12),
        config_flag=ConfigFlag("Feature", "MyFeature", "true", 45),
        keadmin_info=KeAdminFlagInfo("MyFeature", 3, 2, 1)
    )
]

write_excel_feature_flags_to_csv("feature_flags.csv", flags)
