from asgiref.sync import async_to_sync

from addon_service.addon_imp.instantiation import get_storage_addon_instance__blocking
from addon_service.configured_addon.storage.models import ConfiguredStorageAddon
from addon_toolkit import (
    credentials,
    json_arguments,
)


def build_waterbutler_config(configured_storage_addon: ConfiguredStorageAddon) -> dict:
    wb_config = _build_config(configured_storage_addon)
    creds = _build_credentials(configured_storage_addon, wb_config)
    return {
        "config": wb_config,
        "credentials": creds,
    }


def _build_config(configured_storage_addon: ConfiguredStorageAddon):
    imp = get_storage_addon_instance__blocking(
        configured_storage_addon.imp_cls,
        configured_storage_addon.base_account,
        configured_storage_addon.config,
    )
    wb_config = async_to_sync(imp.build_wb_config)()
    return wb_config


def _build_credentials(
    configured_storage_addon: ConfiguredStorageAddon, wb_config: dict
):
    _creds_data = configured_storage_addon.credentials
    match type(_creds_data):
        case credentials.AccessTokenCredentials:
            creds = {"token": _creds_data.access_token}
            if "host" in wb_config:
                creds["host"] = wb_config["host"]
            return creds
        case (
            credentials.AccessKeySecretKeyCredentials
            | credentials.UsernamePasswordCredentials
        ):
            # field names line up with waterbutler's expectations
            serialized_creds = json_arguments.json_for_dataclass(_creds_data)
            if "host" in wb_config:
                serialized_creds["host"] = wb_config["host"]
            return serialized_creds
        case _:
            raise ValueError(f"unknown credentials type: {_creds_data}")
