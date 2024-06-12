import factory
from django.conf import settings
from factory.django import DjangoModelFactory

from addon_service import models as db
from addon_service.common import known_imps
from addon_service.common.credentials_formats import CredentialsFormats
from addon_service.common.service_types import ServiceTypes
from addon_toolkit import AddonCapabilities


class UserReferenceFactory(DjangoModelFactory):
    class Meta:
        model = db.UserReference

    user_uri = factory.Sequence(lambda n: f"{settings.OSF_BASE_URL}/user{n}")


class ResourceReferenceFactory(DjangoModelFactory):
    class Meta:
        model = db.ResourceReference

    resource_uri = factory.Sequence(lambda n: f"{settings.OSF_BASE_URL}/thing{n}")


class OAuth2ClientConfigFactory(DjangoModelFactory):
    class Meta:
        model = db.OAuth2ClientConfig

    auth_uri = factory.Sequence(lambda n: f"https://api.example/auth/{n}")
    auth_callback_url = "https://osf.example/auth/callback"
    token_endpoint_url = "https://api.example.com/oauth/token"
    client_id = factory.Faker("word")
    client_secret = factory.Faker("word")


class AddonOperationInvocationFactory(DjangoModelFactory):
    class Meta:
        model = db.AddonOperationInvocation

    operation_identifier = "BLARG:get_item_info"
    operation_kwargs = {"item_id": "foo"}
    thru_account = factory.SubFactory(
        "addon_service.tests._factories.AuthorizedStorageAccountFactory"
    )
    thru_addon = factory.SubFactory(
        "addon_service.tests._factories.ConfiguredStorageAddonFactory",
        base_account=factory.SelfAttribute("..thru_account"),
    )
    by_user = factory.SubFactory(UserReferenceFactory)


###
# "Storage" models


class ExternalStorageServiceFactory(DjangoModelFactory):
    class Meta:
        model = db.ExternalStorageService

    display_name = factory.Faker("word")
    max_concurrent_downloads = factory.Faker("pyint")
    max_upload_mb = factory.Faker("pyint")
    int_addon_imp = known_imps.get_imp_number(known_imps.get_imp_by_name("BLARG"))
    oauth2_client_config = factory.SubFactory(OAuth2ClientConfigFactory)
    supported_scopes = ["service.url/grant_all"]

    @classmethod
    def _create(
        cls,
        model_class,
        credentials_format=CredentialsFormats.OAUTH2,
        service_type=ServiceTypes.PUBLIC,
        *args,
        **kwargs,
    ):
        api_base_url = ""
        if ServiceTypes.PUBLIC in service_type:
            api_base_url = "https://api.example.url/v1"
        return super()._create(
            model_class=model_class,
            int_credentials_format=credentials_format.value,
            int_service_type=service_type.value,
            api_base_url=api_base_url,
            *args,
            **kwargs,
        )


class AuthorizedStorageAccountFactory(DjangoModelFactory):
    class Meta:
        model = db.AuthorizedStorageAccount

    display_name = factory.Faker("word")
    default_root_folder = "/"
    authorized_capabilities = AddonCapabilities.ACCESS | AddonCapabilities.UPDATE

    @classmethod
    def _create(
        cls,
        model_class,
        external_storage_service=None,
        account_owner=None,
        credentials=None,
        credentials_format=CredentialsFormats.OAUTH2,
        authorized_scopes=None,
        *args,
        **kwargs,
    ):
        account = super()._create(
            model_class=model_class,
            external_storage_service=external_storage_service
            or ExternalStorageServiceFactory(credentials_format=credentials_format),
            account_owner=account_owner or UserReferenceFactory(),
            *args,
            **kwargs,
        )
        if credentials_format is CredentialsFormats.OAUTH2:
            account.initiate_oauth2_flow(authorized_scopes)
        else:
            account.credentials = credentials
            account.save()
        return account


class ConfiguredStorageAddonFactory(DjangoModelFactory):
    class Meta:
        model = db.ConfiguredStorageAddon

    root_folder = "/"
    connected_capabilities = AddonCapabilities.ACCESS

    @classmethod
    def _create(
        cls,
        model_class,
        authorized_resource=None,
        external_storage_service=None,
        credentials_format=CredentialsFormats.OAUTH2,
        base_account=None,
        account_owner=None,
        credentials=None,
        *args,
        **kwargs,
    ):
        authorized_resource = authorized_resource or ResourceReferenceFactory()
        base_account = base_account or AuthorizedStorageAccountFactory(
            external_storage_service=external_storage_service,
            credentials_format=credentials_format,
            account_owner=account_owner,
            credentials=credentials,
        )

        return super()._create(
            model_class=model_class,
            authorized_resource=authorized_resource,
            base_account=base_account,
            *args,
            **kwargs,
        )
