from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

from django.core.exceptions import ValidationError as ModelValidationError
from rest_framework_json_api import serializers

from addon_service.common.credentials_formats import CredentialsFormats
from addon_service.osf_models.fields import encrypt_string
from addon_service.serializer_fields import (
    CredentialsField,
    EnumNameMultipleChoiceField,
)
from addon_toolkit import AddonCapabilities


if TYPE_CHECKING:
    from addon_service.abstract.authorized_account.models import AuthorizedAccount

REQUIRED_FIELDS = frozenset(["url", "account_owner", "authorized_operations"])


class AuthorizedAccountSerializer(serializers.HyperlinkedModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Check whether subclasses declare all of required fields
        if not REQUIRED_FIELDS.issubset(set(self.fields.keys())):
            raise Exception(
                f"{self.__class__.__name__} requires {self.REQUIRED_FIELDS} to be instantiated"
            )

        # Check if it's a POST request and remove the field as it's not in our FE spec
        if "context" in kwargs and kwargs["context"]["request"].method == "POST":
            self.fields.pop("configured_storage_addons", None)

    display_name = serializers.CharField(
        allow_blank=True, allow_null=True, required=False, max_length=256
    )
    authorized_capabilities = EnumNameMultipleChoiceField(enum_cls=AddonCapabilities)
    authorized_operation_names = serializers.ListField(
        child=serializers.CharField(),
        read_only=True,
    )
    auth_url = serializers.CharField(read_only=True)
    api_base_url = serializers.URLField(
        allow_blank=True, required=False, allow_null=True
    )

    credentials = CredentialsField(write_only=True, required=False)
    initiate_oauth = serializers.BooleanField(write_only=True, required=False)

    included_serializers = {
        "account_owner": "addon_service.serializers.UserReferenceSerializer",
        "external_storage_service": "addon_service.serializers.ExternalStorageServiceSerializer",
        "configured_storage_addons": "addon_service.serializers.ConfiguredStorageAddonSerializer",
        "authorized_operations": "addon_service.serializers.AddonOperationSerializer",
    }

    @abstractmethod
    def create_authorized_account(
        self,
        **kwargs,
    ) -> AuthorizedAccount:
        """Handles creation of the appropriate AuthorizedAccount subclass"""

    def create(self, validated_data: dict) -> AuthorizedAccount:
        authorized_account = self.create_authorized_account(**validated_data)
        return self.process_and_set_auth(authorized_account, validated_data)

    def process_and_set_auth(
        self,
        authorized_account: AuthorizedAccount,
        validated_data: dict,
    ) -> AuthorizedAccount:
        if validated_data.get("initiate_oauth", False):
            if authorized_account.credentials_format is CredentialsFormats.OAUTH2:
                authorized_account.initiate_oauth2_flow(
                    validated_data.get("authorized_scopes")
                )
            elif authorized_account.credentials_format is CredentialsFormats.OAUTH1A:
                authorized_account.initiate_oauth1_flow()
                self.context["request"].session["oauth1a_account_id"] = encrypt_string(
                    authorized_account.pk
                )
            else:
                raise serializers.ValidationError(
                    {
                        "initiate_oauth": "this external service is not configured for oauth"
                    }
                )
        elif validated_data.get("credentials"):
            authorized_account.credentials = validated_data["credentials"]

        try:
            authorized_account.save()
        except ModelValidationError as e:
            raise serializers.ValidationError(e)

        if authorized_account.credentials_format.is_direct_from_user:
            authorized_account.execute_post_auth_hook()

        return authorized_account

    def update(self, instance, validated_data):
        # only these fields may be PATCHed:
        if "display_name" in validated_data:
            instance.display_name = validated_data["display_name"]
        if "authorized_capabilities" in validated_data:
            instance.authorized_capabilities = validated_data["authorized_capabilities"]
        if "api_base_url" in validated_data:
            instance.api_base_url = validated_data["api_base_url"]
        if "default_root_folder" in validated_data:
            instance.default_root_folder = validated_data["default_root_folder"]
        if validated_data.get("credentials"):
            instance.credentials = validated_data["credentials"]
        instance.save()  # may raise ValidationError
        if (
            validated_data.get("initiate_oauth", False)
            and instance.credentials_format is CredentialsFormats.OAUTH2
        ):
            instance.initiate_oauth2_flow(validated_data.get("authorized_scopes"))
        return instance

    class Meta:
        fields = [
            "id",
            "url",
            "display_name",
            "account_owner",
            "api_base_url",
            "auth_url",
            "authorized_capabilities",
            "authorized_operations",
            "authorized_operation_names",
            "credentials",
            "initiate_oauth",
            "credentials_available",
        ]
