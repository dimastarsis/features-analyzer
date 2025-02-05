from network.model import KeAdminFlagInfo, YouTrackFlagInfo
from parser.model import ConfigFlag, FeatureFlagV2
from .model import FeatureFlagV2AnalyzeResult


def analyze(
    features_v2_flags: dict[str, FeatureFlagV2],
    config_flags: dict[str, ConfigFlag],
    keadmin_flag_infos: dict[str, KeAdminFlagInfo],
    youtrack_flag_infos: dict[str, YouTrackFlagInfo]
) -> list[FeatureFlagV2AnalyzeResult]:
    undetected_features_v2_flag_keys = set(features_v2_flags.keys())
    undetected_config_flag_keys = set(config_flags.keys())
    analyze_results: list[FeatureFlagV2AnalyzeResult] = list()
    for features_v2_key in features_v2_flags.keys():
        config_flag: ConfigFlag = None
        config_search_name = features_v2_flags[features_v2_key].config_search_name
        if config_search_name in config_flags:
            config_flag = config_flags[config_search_name]

            undetected_features_v2_flag_keys.remove(features_v2_key)
            undetected_config_flag_keys.remove(config_search_name)

        keadmin_flag_info: KeAdminFlagInfo = None
        keadmin_search_name = features_v2_flags[features_v2_key].keadmin_search_name
        if keadmin_search_name in keadmin_flag_infos:
            keadmin_flag_info = keadmin_flag_infos[keadmin_search_name]
            if features_v2_key in undetected_features_v2_flag_keys:
                undetected_features_v2_flag_keys.remove(features_v2_key)

        youtrack_flag_info: YouTrackFlagInfo = None
        youtrack_search_name = features_v2_flags[features_v2_key].youtrack_search_name
        if youtrack_search_name in youtrack_flag_infos:
            youtrack_flag_info = youtrack_flag_infos[youtrack_search_name]
            # не обновляем 'undetected_features_v2_flag_keys'

        analyze_results.append(
            FeatureFlagV2AnalyzeResult(
                features_v2_flags[features_v2_key],
                config_flag,
                keadmin_flag_info,
                youtrack_flag_info
            )
        )

    print(f"Не нашли информации по следующим флагам из модели v2:")
    for features_v2_key in undetected_features_v2_flag_keys:
        print(f"- {features_v2_flags[features_v2_key].property_name}")

    print(f"Не нашли информации по следующим флагам из конфига:")
    for config_key in undetected_config_flag_keys:
        print(f"- {config_flags[config_key].name}")

    return analyze_results
