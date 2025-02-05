from .model import ConfigFlag


def extract_flags(config_text: str) -> dict[str, ConfigFlag]:
    feature_flags = dict()

    config_lines = config_text.split('\n')
    for i, line in enumerate(config_lines):
        if not line:
            continue

        name, value = line.split('=', 1)
        name, value = name.strip(), value.strip()
        prefix = None
        if '.' in name:
            prefix = name.split('.')[0]

        feature_flags[name] = ConfigFlag(prefix, name, value, i)

    print(f"Извлекли из конфига {len(feature_flags)} флагов")
    return feature_flags
