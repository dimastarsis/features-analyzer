from dataclasses import dataclass
from typing import Iterator


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
    line_number: int

    @property
    def keadmin_search_name(self) -> str:
        return self.consumer_name if self.consumer_name else self.property_name

    @property
    def config_search_name(self) -> str:
        if self.global_name:
            return self.global_name
        return "Features." + self.keadmin_search_name

    @property
    def youtrack_search_name(self) -> str:
        if self.global_name:
            return self.global_name
        return self.keadmin_search_name
        # todo
        # if self.global_name:
        #     yield self.global_name
        # if self.consumer_name:
        #     yield "Features." + self.consumer_name
        #     yield self.consumer_name
        # yield "Features." + self.property_name
        # yield self.property_name
