from dataclasses import dataclass


@dataclass
class FeatureFlagV2RowData:
    property_hyperlink: str
    consumer: str
    value_type: str
    config_flag_hyperlink: str | None
    config_value: str | None
    keadmin_feature_hyperlink: str | None
    keadmin_adjustments_hyperlink: int | None
    keadmin_adjustments_new_hyperlink: int | None
