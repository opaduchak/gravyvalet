from enum import StrEnum

from addon_service.common.enum_decorators import enum_names_subset
from addon_service.common.known_imps import KnownAddonImps


@enum_names_subset(KnownAddonImps)
class ExternalAccountKeys(StrEnum):
    ZOTERO_ORG = "userID"
