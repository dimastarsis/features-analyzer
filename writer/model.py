from dataclasses import dataclass


@dataclass
class FeatureFlagV2RowData:
    property_name: str
    property_search_hyperlink: str
    consumer: str
    property_type: str
    config_flag_name: str | None
    config_search_hyperlink: str | None
    config_value: str | None
    keadmin_feature_name: str | None
    keadmin_features_hyperlink: str | None
    keadmin_adjustments_hyperlink: str | None
    keadmin_adjustments_new_hyperlink: str | None
    youtrack_flag_name: str | None
    youtrack_issues_hyperlink: str | None
