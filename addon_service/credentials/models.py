from django.core.exceptions import ValidationError
from django.db import models

from addon_service.common.encrypted_dataclass_model import EncryptedDataclassModel
from addon_toolkit.credentials import Credentials


class ExternalCredentials(EncryptedDataclassModel[Credentials]):
    # Attributes inherited from back-references:
    # authorized_storage_account (AuthorizedStorageAccount._credentials, One2One)

    class Meta:
        verbose_name = "External Credentials"
        verbose_name_plural = "External Credentials"
        app_label = "addon_service"
        indexes = (
            models.Index(fields=["modified"]),  # for schedule_encryption_rotation
        )

    @property
    def dataclass_type(self) -> type[Credentials]:
        return self.format.dataclass

    @property
    def authorized_accounts(self):
        """Returns the list of all accounts that point to this set of credentials.

        For now, this will just be a single AuthorizedStorageAccount, but in the future
        other types of accounts for the same user could point to the same set of credentials
        """
        try:
            return [
                *filter(
                    bool,
                    [
                        getattr(self, "authorized_storage_account", None),
                        getattr(self, "temporary_authorized_storage_account", None),
                    ],
                )
            ]
        except ExternalCredentials.authorized_storage_account.RelatedObjectDoesNotExist:
            return None

    @property
    def format(self):
        if not self.authorized_accounts:
            return None
        return self.authorized_accounts[0].external_service.credentials_format

    def clean_fields(self, *args, **kwargs):
        super().clean_fields(*args, **kwargs)
        self._validate_credentials()

    def _validate_credentials(self):
        if not self.authorized_accounts:
            return
        try:
            self.decrypted_dataclass
        except TypeError as e:
            raise ValidationError(e)
