from dataclasses import dataclass


@dataclass
class ConfigFeatureFlag:
    prefix: str | None
    name: str
    value: str
    line_number: int


@dataclass
class ModelFeatureFlagV2:
    global_name: str | None
    consumer_name: str | None
    consumer: str
    property_name: str
    value_type: str

    @property
    def config_search_name(self) -> str:
        if self.global_name:
            return self.global_name
        return "Features." + (self.consumer_name if self.consumer_name else self.property_name)
