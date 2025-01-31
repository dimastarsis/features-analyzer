import re
from model import ConfigFeatureFlag, ModelFeatureFlagV2


def extract_flags_from_config(config_text: str) -> dict[str, ConfigFeatureFlag]:
    feature_flags = dict()

    config_lines = config_text.split('\n')
    for line_number, line in enumerate(config_lines):  # todo line_number
        if not line:
            continue

        flag_name, flag_value = line.split('=', 1)
        flag_name, flag_value = flag_name.strip(), flag_value.strip()

        feature_flags[flag_name] = ConfigFeatureFlag(name=flag_name, value=flag_value)

    return feature_flags


def extract_flags_from_features_v2(features_v2_text: str) -> dict[str, ModelFeatureFlagV2]:
    pattern = re.compile(
        r'\[FeatureFlag(?:\(([\s\S]*?)\))?\]\s*'  # Опциональный `(...)` внутри `FeatureFlag`
        r'public\s+([\w?]+)\s+(\w+)',  # public {тип} {название}
    )

    flags_matches = pattern.findall(features_v2_text)

    public_modifier_count = features_v2_text.count("public")
    if len(flags_matches) != public_modifier_count - 1:
        raise RuntimeError(f"Число потенциальных флагов {public_modifier_count - 1}, распарсили {len(flags_matches)}")

    # parsed_flags = [
    #     {"attributes": attr.strip() if attr else "", "type": ftype, "name": fname}
    #     for attr, ftype, fname in feature_flags
    # ]

    feature_flags = dict()
    for attr, ftype, fname in flags_matches:
        feature_flags[fname] = ModelFeatureFlagV2(name=fname, type=ftype)

    return feature_flags
