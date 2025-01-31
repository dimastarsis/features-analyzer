from dataclasses import dataclass


@dataclass
class ConfigFeatureFlag:
    name: str
    value: str


@dataclass
class ModelFeatureFlagV2:
    name: str
    type: str


# todo
#
# [FeatureFlag(
#             consumer: FeatureConsumer.KeAbon,
#             consumerSettingName: "MultiUser.WorkGroupsEnabled.GroupSigner",
#             globalSettingName: "Features.MultiUser.GroupSigner")]

@dataclass
class ProjectFile:
    project_name: str
    file_path: str
    branch: str
