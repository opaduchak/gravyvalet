import json
from http import HTTPStatus

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase

from addon_service import models as db
from addon_service.credentials import CredentialsFormats
from addon_service.external_storage_service.views import ExternalStorageServiceViewSet
from addon_service.tests import _factories
from addon_service.tests._helpers import get_test_request


class TestExternalStorageServiceAPI(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls._ess = _factories.ExternalStorageServiceFactory()

    @property
    def _detail_path(self):
        return reverse("external-storage-services-detail", kwargs={"pk": self._ess.pk})

    @property
    def _list_path(self):
        return reverse("external-storage-services-list")

    @property
    def _related_authorized_storage_accounts_path(self):
        return reverse(
            "external-storage-services-related",
            kwargs={
                "pk": self._ess.pk,
                "related_field": "authorized_storage_accounts",
            },
        )

    def test_get(self):
        _resp = self.client.get(self._detail_path)
        self.assertEqual(_resp.status_code, HTTPStatus.OK)
        self.assertEqual(_resp.data["auth_uri"], self._ess.auth_uri)

    def test_methods_not_allowed(self):
        _methods_not_allowed = {
            self._detail_path: {"post"},
            self._list_path: {"patch", "put", "post"},
            self._related_authorized_storage_accounts_path: {"patch", "put", "post"},
        }
        for _path, _methods in _methods_not_allowed.items():
            for _method in _methods:
                with self.subTest(path=_path, method=_method):
                    _client_method = getattr(self.client, _method)
                    _resp = _client_method(_path)
                    self.assertEqual(_resp.status_code, HTTPStatus.METHOD_NOT_ALLOWED)


# unit-test data model
class TestExternalStorageServiceModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls._ess = _factories.ExternalStorageServiceFactory()

    def test_can_load(self):
        _resource_from_db = db.ExternalStorageService.objects.get(id=self._ess.id)
        self.assertEqual(self._ess.auth_uri, _resource_from_db.auth_uri)

    def test_authorized_storage_accounts__empty(self):
        self.assertEqual(
            list(self._ess.authorized_storage_accounts.all()),
            [],
        )

    def test_authorized_storage_accounts__several(self):
        _accounts = set(
            _factories.AuthorizedStorageAccountFactory.create_batch(
                size=3,
                external_storage_service=self._ess,
            )
        )
        self.assertEqual(
            set(self._ess.authorized_storage_accounts.all()),
            _accounts,
        )

    def test_validation__invalid_format(self):
        service = _factories.ExternalStorageServiceFactory()
        service.int_credentials_format = -1
        with self.assertRaises(ValidationError):
            service.save()

    def test_validation__unsupported_format(self):
        service = _factories.ExternalStorageServiceFactory()
        service.int_credentials_format = CredentialsFormats.UNSPECIFIED.value
        with self.assertRaises(ValidationError):
            service.save()

    def test_validation__oauth_creds_require_client_config(self):
        service = _factories.ExternalStorageServiceFactory(
            credentials_format=CredentialsFormats.OAUTH2
        )
        service.oauth2_client_config = None
        with self.assertRaises(ValidationError):
            service.save()


# unit-test viewset (call the view with test requests)
class TestExternalStorageServiceViewSet(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls._ess = _factories.ExternalStorageServiceFactory()
        cls._view = ExternalStorageServiceViewSet.as_view({"get": "retrieve"})
        cls._user = _factories.UserReferenceFactory()

    def test_get(self):
        _resp = self._view(
            get_test_request(),
            pk=self._ess.pk,
        )
        self.assertEqual(_resp.status_code, HTTPStatus.OK)
        _content = json.loads(_resp.rendered_content)
        self.assertEqual(
            set(_content["data"]["attributes"].keys()),
            {
                "auth_uri",
                "max_concurrent_downloads",
                "max_upload_mb",
                "credentials_format",
                "service_name",
            },
        )
        self.assertEqual(
            set(_content["data"]["relationships"].keys()),
            {
                "addon_imp",
            },
        )

    def test_unauthorized(self):
        """Is public resource Unauth is OK!"""
        _anon_resp = self._view(get_test_request(), pk=self._ess.pk)
        self.assertEqual(_anon_resp.status_code, HTTPStatus.OK)

    def test_wrong_user(self):
        """Is public resource, so OK!"""
        _another_user = _factories.UserReferenceFactory()
        _resp = self._view(
            get_test_request(user=_another_user),
            pk=self._ess.pk,
        )
        self.assertEqual(_resp.status_code, HTTPStatus.OK)


class TestExternalStorageServiceRelatedView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls._ess = _factories.ExternalStorageServiceFactory()
        cls._related_view = ExternalStorageServiceViewSet.as_view(
            {"get": "retrieve_related"},
        )

    def test_get_related(self):
        _resp = self._related_view(
            get_test_request(),
            pk=self._ess.pk,
            related_field="addon_imp",
        )
        self.assertEqual(_resp.status_code, HTTPStatus.OK)
        self.assertEqual(_resp.data["name"], self._ess.addon_imp.name)