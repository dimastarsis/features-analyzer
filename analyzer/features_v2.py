from network.model import KeAdminFlagInfo
from parser.model import ConfigFlag, FeatureFlagV2
from network import keadmin
from .model import FeatureFlagV2AnalyzeResult
from tqdm import tqdm


def analyze(
    features_v2_flags: dict[str, FeatureFlagV2], config_flags: dict[str, ConfigFlag]
) -> list[FeatureFlagV2AnalyzeResult]:
    undetected_features_v2_flag_keys = set(features_v2_flags.keys())
    undetected_config_flag_keys = set(config_flags.keys())
    analyze_results: list[tuple[FeatureFlagV2, ConfigFlag, KeAdminFlagInfo]] = list()
    for features_v2_key in tqdm(features_v2_flags.keys(), desc='Обрабатываем фича флаги'):
        config_flag: ConfigFlag = None
        config_search_name = features_v2_flags[features_v2_key].config_search_name
        if config_search_name in config_flags.keys():
            config_flag = config_flags[config_search_name]

            undetected_features_v2_flag_keys.remove(features_v2_key)
            undetected_config_flag_keys.remove(config_search_name)

        keadmin_flag_info = keadmin.get_keadmin_info(features_v2_flags[features_v2_key].keadmin_search_name)
        if keadmin_flag_info and features_v2_key in undetected_features_v2_flag_keys:
            undetected_features_v2_flag_keys.remove(features_v2_key)

        analyze_results.append(
            FeatureFlagV2AnalyzeResult(
                features_v2_flags[features_v2_key],
                config_flag,
                keadmin_flag_info
            )
        )

    print(f"Не нашли информации по следующим флагам из модели v2:")
    for features_v2_key in undetected_features_v2_flag_keys:
        print(f"- {features_v2_flags[features_v2_key].property_name}")

    print(f"Не нашли информации по следующим флагам из конфига:")
    for config_key in undetected_config_flag_keys:
        print(f"- {config_flags[config_key].name}")

    return analyze_results
