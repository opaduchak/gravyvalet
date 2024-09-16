from django.db import models

from addon_service.abstract.external_storage.models import ExternalService
from addon_service.authorized_storage_account.models import AuthorizedStorageAccount
from addon_service.common.validators import validate_storage_imp_number


class ExternalStorageService(ExternalService):
    max_concurrent_downloads = models.IntegerField(null=False)
    max_upload_mb = models.IntegerField(null=False)

    def clean(self):
        super().clean()
        validate_storage_imp_number(self.int_addon_imp)

    @property
    def authorized_storage_accounts(self):
        return AuthorizedStorageAccount.objects.filter(external_service=self)

    class Meta:
        verbose_name = "External Storage Service"
        verbose_name_plural = "External Storage Services"
        app_label = "addon_service"

    class JSONAPIMeta:
        resource_name = "external-storage-services"
