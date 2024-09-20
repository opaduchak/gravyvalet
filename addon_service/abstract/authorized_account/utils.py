from addon_service.abstract.authorized_account.models import AuthorizedAccount
from addon_toolkit.interfaces.citation import CitationAddonImp
from addon_toolkit.interfaces.storage import StorageAddonImp


def get_config_for_account(account: AuthorizedAccount):
    if issubclass(account.imp_cls, StorageAddonImp):
        return account.authorizedstorageaccount.config
    elif issubclass(account.imp_cls, CitationAddonImp):
        return account.authorizedcitationaccount.config

    raise ValueError(f"this function implementation does not support {account.imp_cls}")
