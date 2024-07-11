import hashlib

from django.db import models

from addon_service.common.base_model import AddonsServiceBaseModel
from addon_service.common.encrypted_dataclass_model import EncryptedDataclassModel
from addon_toolkit.credentials import OAuth1Credentials


class OAuth1ClientConfig(AddonsServiceBaseModel):
    """
    Model for storing attributes that are required for managing
    OAuth1 credentials exchanges with an ExternalService on behalf
    of a registered client (e.g. the OSF)
    """

    # URI that allows to obtain temporary request token to proceed with user auth
    request_token_url = models.URLField(null=False)
    # URI to which user will be redirected to authenticate
    auth_url = models.URLField(null=False)
    # URI to which user will be redirected after authentication
    auth_callback_url = models.URLField(null=False)
    # URI to obtain access token
    access_token_url = models.URLField(null=False)

    client_key = models.CharField(null=True)
    client_secret = models.CharField(null=True)

    class Meta:
        verbose_name = "OAuth1 Client Config"
        verbose_name_plural = "OAuth1 Client Configs"
        app_label = "addon_service"

    def __repr__(self):
        return f'<{self.__class__.__qualname__}(pk="{self.pk}", auth_uri="{self.auth_url}, access_token_url="{self.access_token_url}", request_token_url="{self.request_token_url}", client_key="{self.client_key}")>'

    __str__ = __repr__


class Oauth1TemporaryCredentialsManager(models.Manager):
    def filter_by_oauth1_temporary_token(self, oauth1_temporary_token: str):
        return self.filter(
            oauth1_temporary_token_hash=_hash_temp_token(oauth1_temporary_token)
        )


class OAuth1TemporaryCredentials(EncryptedDataclassModel[OAuth1Credentials]):
    dataclass_type = OAuth1Credentials

    oauth1_temporary_token_hash = models.CharField()

    class Meta:
        verbose_name = "OAuth1 Temporary Credentials"
        verbose_name_plural = "OAuth1 Temporary Credentialss"
        app_label = "addon_service"
        indexes = [
            models.Index(fields="temporary_token_hash"),
        ]

    def set_hashed_temporary_token(self, oauth1_temporary_token: str):
        self.oauth1_temporary_token_hash = _hash_temp_token(oauth1_temporary_token)


def _hash_temp_token(oauth1_temporary_token: str):
    return hashlib.sha384(oauth1_temporary_token.encode())
