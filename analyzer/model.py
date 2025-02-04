from dataclasses import dataclass
from parser.model import FeatureFlagV2, ConfigFlag
from network.model import KeAdminFlagInfo


@dataclass
class FeatureFlagV2AnalyzeResult:
    feature_v2_flag: FeatureFlagV2
    config_flag: ConfigFlag | None
    keadmin_info: KeAdminFlagInfo | None
