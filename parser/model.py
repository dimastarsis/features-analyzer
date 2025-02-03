from dataclasses import dataclass


@dataclass
class ConfigFlag:
    prefix: str | None
    name: str
    value: str
    line_number: int


@dataclass
class FeatureFlagV2:
    global_name: str | None
    consumer_name: str | None
    consumer: str
    property_name: str
    value_type: str

    @property
    def net_search_name(self) -> str:
        return self.consumer_name if self.consumer_name else self.property_name

    @property
    def config_search_name(self) -> str:
        if self.global_name:
            return self.global_name
        return "Features." + self.net_search_name
