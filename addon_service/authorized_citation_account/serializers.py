from django.core.exceptions import ValidationError as ModelValidationError
from rest_framework_json_api import serializers
from rest_framework_json_api.relations import (
    HyperlinkedRelatedField,
    ResourceRelatedField,
)
from rest_framework_json_api.utils import get_resource_type_from_model

from addon_service.abstract.authorized_account.serializers import (
    AuthorizedAccountSerializer,
)
from addon_service.addon_operation.models import AddonOperationModel
from addon_service.common import view_names
from addon_service.common.serializer_fields import (
    DataclassRelatedLinkField,
    ReadOnlyResourceRelatedField,
)
from addon_service.models import (
    AuthorizedCitationAccount,
    ConfiguredCitationAddon,
    ExternalCitationService,
    UserReference,
)
from addon_toolkit import AddonCapabilities


RESOURCE_TYPE = get_resource_type_from_model(AuthorizedCitationAccount)


class AuthorizedCitationAccountSerializer(AuthorizedAccountSerializer):
    external_citation_service = ResourceRelatedField(
        queryset=ExternalCitationService.objects.all(),
        many=False,
        source="external_service",
        related_link_view_name=view_names.related_view(RESOURCE_TYPE),
    )
    configured_citation_addons = HyperlinkedRelatedField(
        many=True,
        queryset=ConfiguredCitationAddon.objects.active(),
        related_link_view_name=view_names.related_view(RESOURCE_TYPE),
        required=False,
    )
    url = serializers.HyperlinkedIdentityField(
        view_name=view_names.detail_view(RESOURCE_TYPE), required=False
    )
    account_owner = ReadOnlyResourceRelatedField(
        many=False,
        queryset=UserReference.objects.all(),
        related_link_view_name=view_names.related_view(RESOURCE_TYPE),
    )
    authorized_operations = DataclassRelatedLinkField(
        dataclass_model=AddonOperationModel,
        related_link_view_name=view_names.related_view(RESOURCE_TYPE),
    )

    included_serializers = {
        "account_owner": "addon_service.serializers.UserReferenceSerializer",
        "external_citation_service": "addon_service.serializers.ExternalCitationServiceSerializer",
        "configured_citation_addons": "addon_service.serializers.ConfiguredCitationAddonSerializer",
        "authorized_operations": "addon_service.serializers.AddonOperationSerializer",
    }

    def create_authorized_account(
        self,
        external_service: ExternalCitationService,
        authorized_capabilities: AddonCapabilities,
        display_name: str = "",
        api_base_url: str = "",
        **kwargs,
    ) -> AuthorizedCitationAccount:
        session_user_uri = self.context["request"].session.get("user_reference_uri")
        account_owner, _ = UserReference.objects.get_or_create(
            user_uri=session_user_uri
        )
        try:
            return AuthorizedCitationAccount.objects.create(
                _display_name=display_name,
                external_service=external_service,
                account_owner=account_owner,
                authorized_capabilities=authorized_capabilities,
                api_base_url=api_base_url,
            )
        except ModelValidationError as e:
            raise serializers.ValidationError(e)

    class Meta:
        model = AuthorizedCitationAccount
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
            "configured_citation_addons",
            "credentials",
            "default_root_folder",
            "external_citation_service",
            "initiate_oauth",
            "credentials_available",
        ]
