import typing

from django.core.exceptions import ValidationError
from django.db import models

from addon_service.common import encryption
from addon_service.common.base_model import AddonsServiceBaseModel
from addon_service.common.dibs import dibs
from addon_toolkit.json_arguments import json_for_dataclass


_DATACLASS = typing.TypeVar("_DATACLASS")


class EncryptedDataclassModel(AddonsServiceBaseModel, typing.Generic[_DATACLASS]):
    class Meta:
        abstract = True

    encrypted_json = models.BinaryField()
    _salt = models.BinaryField()
    _scrypt_block_size = models.IntegerField()
    _scrypt_cost_log2 = models.IntegerField()
    _scrypt_parallelization = models.IntegerField()

    @classmethod
    def new(cls):
        # initialize key-parameter fields with fresh defaults
        _new = cls()
        _new.encryption_key_parameters = encryption.KeyParameters()
        return _new

    @property
    def dataclass_type(self) -> type[_DATACLASS]:
        raise NotImplementedError(
            f"{self.__class__} requires a `dataclass_type` attribute or property"
        )

    def rotate_encryption(self):
        with dibs(self):
            self.encrypted_json, self.encryption_key_parameters = (
                encryption.pls_rotate_encryption(
                    encrypted=self.encrypted_json,
                    stored_params=self.encryption_key_parameters,
                )
            )
            self.save()

    @property
    def decrypted_dataclass(self) -> _DATACLASS:
        return self.dataclass_type(**self.decrypted_json)

    @decrypted_dataclass.setter
    def decrypted_dataclass(self, value: _DATACLASS):
        if not isinstance(value, self.dataclass_type):
            raise ValidationError(
                f"expected instance of {self.dataclass_type}, got {value}"
            )
        self.decrypted_json = json_for_dataclass(value)

    @property
    def decrypted_json(self):
        return encryption.pls_decrypt_json(
            self.encrypted_json, self.encryption_key_parameters
        )

    @decrypted_json.setter
    def decrypted_json(self, value):
        self.encrypted_json = encryption.pls_encrypt_json(
            value, self.encryption_key_parameters
        )

    @property
    def encryption_key_parameters(self) -> encryption.KeyParameters:
        return encryption.KeyParameters(
            salt=self._salt,
            scrypt_block_size=self._scrypt_block_size,
            scrypt_cost_log2=self._scrypt_cost_log2,
            scrypt_parallelization=self._scrypt_parallelization,
        )

    @encryption_key_parameters.setter
    def encryption_key_parameters(self, value: encryption.KeyParameters) -> None:
        self._salt = value.salt
        self._scrypt_block_size = value.scrypt_block_size
        self._scrypt_cost_log2 = value.scrypt_cost_log2
        self._scrypt_parallelization = value.scrypt_parallelization
