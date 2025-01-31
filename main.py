from model import ProjectFile
from network import fetch_gitlab_file
from parser import extract_flags_from_config, extract_flags_from_features_v2


CONFIG = ProjectFile(project_name="clusterconfig_storage_production", file_path="ft/config", branch="default")
FEATURES_V2 = ProjectFile(
    project_name="ft",
    file_path="FileTransfer.Lib/Providers/FeaturesV2/FeatureFlagsModel.cs",
    branch="master"
)


def main() -> None:
    config_text = fetch_gitlab_file(CONFIG)
    config_flags = extract_flags_from_config(config_text)
    print("Извлечённые флаги из конфига:")
    for key in config_flags.keys():
        print(config_flags[key])

    features_v2_text = fetch_gitlab_file(FEATURES_V2)
    features_v2_flags = extract_flags_from_features_v2(features_v2_text)
    print("Извлечённые флаги из модели v2:")
    for key in features_v2_flags.keys():
        print(features_v2_flags[key])


if __name__ == "__main__":
    main()
