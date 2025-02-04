import network
import parser
import analyzer
import writer


def main() -> None:
    features_v2_file = network.ProjectFile.parse(network.FEATURES_V2_URL)
    config_file = network.ProjectFile.parse(network.CONFIG_URL)

    features_v2_text = network.gitlab.fetch_file(features_v2_file)
    features_v2_flags = parser.features_v2.extract_flags(features_v2_text)
    print(f"Извлекли из модели v2 {len(features_v2_flags)} флагов")

    config_text = network.gitlab.fetch_file(config_file)
    config_flags = parser.config.extract_flags(config_text)
    print(f"Извлекли из конфига {len(config_flags)} флагов")

    analyze_results = analyzer.features_v2.analyze(features_v2_flags, config_flags)
    writer.csv_writer.write(analyze_results)


if __name__ == "__main__":
    main()
