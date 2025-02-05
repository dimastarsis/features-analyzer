import re
from .model import FeatureFlagV2

GLOBAL_SETTING_NAME = 'globalSettingName'
CONSUMER_SETTING_NAME = 'consumerSettingName'
CONSUMER = 'consumer'


def _parse_attribute(attr: str) -> dict[str, str]:
    attr = attr.strip()
    attr_dict = {
        GLOBAL_SETTING_NAME: "null",
        CONSUMER_SETTING_NAME: "null",
        CONSUMER: "FeatureConsumer.KeUser"
    }

    if not attr:
        return attr_dict

    attr_parts: list[str] = attr.split(',') if ',' in attr else [attr]
    for i, part in enumerate(attr_parts):
        part = part.strip()
        if ':' in part:
            attr_key, attr_value = part.split(':', 1)
            attr_dict[attr_key.strip()] = attr_value.strip()
        elif len(attr_parts) < 2 or (len(attr_parts) == 2 and 'FeatureConsumer' in attr_parts[-1]):
            if i == 0:
                attr_dict[CONSUMER_SETTING_NAME] = part
            else:
                attr_dict[CONSUMER] = part
        else:
            if i == 0:
                attr_dict[GLOBAL_SETTING_NAME] = part
            elif i == 1:
                attr_dict[CONSUMER_SETTING_NAME] = part
            else:
                attr_dict[CONSUMER] = part

    return attr_dict


def _get_line_number(lines: list[str], target: str, start: int) -> int:
    for i in range(start, len(lines)):
        for part in lines[i].split():
            if part == target:
                return i
    else:
        raise ValueError(f"{target} не найден начиная с индекса строки {start}")


def extract_flags(features_v2_text: str) -> dict[str, FeatureFlagV2]:
    pattern = re.compile(
        r'\[FeatureFlag(?:\(([\s\S]*?)\))?]\s*'  # Опциональный `(...)` внутри `FeatureFlag`
        r'public\s+([\w?]+)\s+(\w+)',  # public {тип} {название}
    )
    flags_matches = pattern.findall(features_v2_text)

    public_modifier_count = features_v2_text.count("public")
    if len(flags_matches) != public_modifier_count - 1:
        raise RuntimeError(f"Число потенциальных флагов {public_modifier_count - 1}, распарсили {len(flags_matches)}")

    lines = features_v2_text.splitlines()
    line_number = -1
    feature_flags = dict()
    for attr, value_type, property_name in flags_matches:
        attr_dict = _parse_attribute(attr)
        property_line_number = line_number = _get_line_number(lines, property_name, line_number + 1)

        feature_flags[property_name] = FeatureFlagV2(
            attr_dict[GLOBAL_SETTING_NAME].replace('\"', '') if attr_dict[GLOBAL_SETTING_NAME] != "null" else None,
            attr_dict[CONSUMER_SETTING_NAME].replace('\"', '') if attr_dict[CONSUMER_SETTING_NAME] != "null" else None,
            attr_dict[CONSUMER].split('.', 1)[1],
            property_name,
            value_type,
            property_line_number
        )

    print(f"Извлекли из модели v2 {len(feature_flags)} флагов")
    return feature_flags
