import json
import unittest
from http import HTTPStatus

from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase

from addon_service import models
from addon_service.addon_operation_invocation.views import (
    AddonOperationInvocationViewSet,
)
from addon_service.tests import _factories
from addon_service.tests._helpers import (
    MockOSF,
    get_test_request,
    jsonapi_ref,
)


class TestAddonOperationInvocationCreate(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls._configured_addon = _factories.ConfiguredStorageAddonFactory()
        cls._user = cls._configured_addon.base_account.account_owner
        cls._operation = models.AddonOperationModel.get_by_natural_key_str(
            "BLARG:blargblarg"
        )

    def setUp(self):
        super().setUp()
        self.client.cookies[settings.USER_REFERENCE_COOKIE] = self._user.user_uri
        self._mock_osf = MockOSF()
        self.enterContext(self._mock_osf.mocking())

    @property
    def _list_path(self):
        return reverse("addon-operation-invocations-list")

    def _payload_for_post(self):
        return {
            "data": {
                "type": "addon-operation-invocations",
                "attributes": {
                    "operation_kwargs": {"item": {"item_id": "foo"}},
                },
                "relationships": {
                    "operation": {
                        "data": jsonapi_ref(self._operation),
                    },
                    "thru_addon": {
                        "data": jsonapi_ref(self._configured_addon),
                    },
                },
            }
        }

    def test_post(self):
        _resp = self.client.post(
            self._list_path,
            data=json.dumps(self._payload_for_post()),
            content_type="application/vnd.api+json",
        )
        self.assertEqual(_resp.status_code, HTTPStatus.CREATED)
        self.assertEqual(
            _resp.data["operation_result"],
            {
                "item_ids": ["hello"],
                "next_cursor": None,
                "total_count": 1,
            },
        )
        self.assertEqual(
            _resp.data["invocation_status"],
            "SUCCESS",
        )


@unittest.skip("TODO")
class TestAddonOperationInvocationErrors(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls._invocation = _factories.AddonOperationInvocationFactory()

    @property
    def _detail_path(self):
        return reverse(
            "addon-operation-invocations-detail",
            kwargs={"pk": self._invocation.pk},
        )

    @property
    def _list_path(self):
        return reverse("addon-operation-invocations-list")

    def _related_path(self, related_field):
        return reverse(
            "addon-operation-invocations-related",
            kwargs={
                "pk": self._invocation.pk,
                "related_field": related_field,
            },
        )

    def test_methods_not_allowed(self):
        _methods_not_allowed = {
            self._list_path: {"get", "patch", "put"},
            self._detail_path: {"patch", "put", "post", "delete"},
            self._related_path("thru_addon"): {"patch", "put", "post", "delete"},
            self._related_path("by_user"): {"patch", "put", "post", "delete"},
            self._related_path("operation"): {"patch", "put", "post", "delete"},
        }
        for _path, _methods in _methods_not_allowed.items():
            for _method in _methods:
                with self.subTest(path=_path, method=_method):
                    _client_method = getattr(self.client, _method)
                    _resp = _client_method(_path)
                    self.assertEqual(_resp.status_code, HTTPStatus.METHOD_NOT_ALLOWED)


# unit-test data model
@unittest.skip("TODO")
class TestAddonOperationInvocationModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls._configured_addon = _factories.AddonOperationInvocationFactory()

    def test_can_load(self):
        _resource_from_db = models.AddonOperationInvocation.objects.get(
            id=self._configured_addon.id
        )
        self.assertEqual(self._configured_addon.pk, _resource_from_db.pk)


# unit-test viewset (call the view with test requests)
@unittest.skip("TODO")
class TestAddonOperationInvocationViewSet(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls._invocation = _factories.AddonOperationInvocationFactory()
        cls._view = AddonOperationInvocationViewSet.as_view(
            {
                "post": "create",
                "get": "retrieve",
                "delete": "destroy",
            }
        )

    def test_get(self):
        _resp = self._view(
            get_test_request(),
            pk=self._invocation.pk,
        )
        self.assertEqual(_resp.status_code, HTTPStatus.OK)
        _content = json.loads(_resp.rendered_content)
        self.assertEqual(
            set(_content["data"]["attributes"].keys()),
            {
                "root_folder",
                "connected_capabilities",
            },
        )
        self.assertEqual(
            _content["data"]["attributes"]["connected_capabilities"],
            ["ACCESS"],
        )
        self.assertEqual(
            set(_content["data"]["relationships"].keys()),
            {
                "authorized_resource",
                "base_account",
                "connected_operations",
            },
        )

    @unittest.expectedFailure  # TODO
    def test_unauthorized(self):
        _anon_resp = self._view(get_test_request(), pk=self._user.pk)
        self.assertEqual(_anon_resp.status_code, HTTPStatus.UNAUTHORIZED)

    @unittest.expectedFailure  # TODO
    def test_wrong_user(self):
        _another_user = _factories.UserReferenceFactory()
        _resp = self._view(
            get_test_request(user=_another_user),
            pk=self._user.pk,
        )
        self.assertEqual(_resp.status_code, HTTPStatus.FORBIDDEN)

    # def test_create(self):
    #     _post_req = get_test_request(user=self._user, method='post')
    #     self._view(_post_req, pk=


@unittest.skip("TODO")
class TestAddonOperationInvocationRelatedView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls._invocation = _factories.AddonOperationInvocationFactory()
        cls._related_view = AddonOperationInvocationViewSet.as_view(
            {"get": "retrieve_related"},
        )

    def test_get_related(self):
        _resp = self._related_view(
            get_test_request(),
            pk=self._invocation.pk,
            related_field="base_account",
        )
        self.assertEqual(_resp.status_code, HTTPStatus.OK)
        _content = json.loads(_resp.rendered_content)
        self.assertEqual(
            _content["data"]["id"],
            str(self._invocation.base_account_id),
        )