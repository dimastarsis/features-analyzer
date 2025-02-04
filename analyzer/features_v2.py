from network.model import ProjectFile, KeAdminFlagInfo
from parser.model import ConfigFlag, FeatureFlagV2
from network import gitlab, keadmin
from parser import features_v2, config
from .model import FeatureFlagV2AnalyzeResult
from tqdm import tqdm

CONFIG = ProjectFile(project_name="clusterconfig_storage_production", file_path="ft/config", branch="default")  # todo парсить из констант и импортировать
FEATURES_V2 = ProjectFile(
    project_name="ft",
    file_path="FileTransfer.Lib/Providers/FeaturesV2/FeatureFlagsModel.cs",
    branch="master"
)


def analyze() -> list[FeatureFlagV2AnalyzeResult]:
    config_text = gitlab.fetch_file(CONFIG)  # todo рефакторинг, нужно вытащить от сюда этот код
    config_flags = config.extract_flags(config_text)
    print(f"Извлекли из конфига {len(config_flags)} флагов")

    features_v2_text = gitlab.fetch_file(FEATURES_V2)
    features_v2_flags = features_v2.extract_flags(features_v2_text)
    print(f"Извлекли из модели v2 {len(features_v2_flags)} флагов")

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
        if not keadmin_flag_info.empty and features_v2_key in undetected_features_v2_flag_keys:
            undetected_features_v2_flag_keys.remove(features_v2_key)

        analyze_results.append(
            FeatureFlagV2AnalyzeResult(
                features_v2_flags[features_v2_key],
                config_flag,
                keadmin_flag_info
            )
        )

    print(f"Нашли значение для {len(features_v2_flags) - len(undetected_features_v2_flag_keys)} флагов v2")
    print(f"Не нашли значение для {len(undetected_features_v2_flag_keys)} флагов v2:")
    for features_v2_key in undetected_features_v2_flag_keys:
        print(f"- {features_v2_flags[features_v2_key]}")

    print(f"Не нашли исходный флаг для:")
    for config_key in undetected_config_flag_keys:
        print(f"- {config_flags[config_key]}")

    return analyze_results
