from addon_service.abstract.configured_addon.models import ConfiguredAddon
from addon_toolkit.interfaces.citation import CitationConfig


class ConfiguredCitationAddon(ConfiguredAddon):

    class Meta:
        verbose_name = "Configured Citation Addon"
        verbose_name_plural = "Configured Citation Addons"
        app_label = "addon_service"

    class JSONAPIMeta:
        resource_name = "configured-citation-addons"

    @property
    def config(self) -> CitationConfig:
        return self.base_account.authorizedcitationaccount.config
