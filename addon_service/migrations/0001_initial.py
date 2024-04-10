# Generated by Django 4.2.7 on 2024-04-10 21:57

import django.contrib.postgres.fields
import django.db.models.deletion
from django.db import (
    migrations,
    models,
)

import addon_service.common.enums.validators
import addon_service.credentials.validators


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="AddonOperationInvocation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(editable=False)),
                ("modified", models.DateTimeField()),
                (
                    "int_invocation_status",
                    models.IntegerField(
                        default=1,
                        validators=[
                            addon_service.common.enums.validators.validate_invocation_status
                        ],
                    ),
                ),
                ("operation_identifier", models.TextField()),
                ("operation_kwargs", models.JSONField(blank=True, default=dict)),
                (
                    "operation_result",
                    models.JSONField(blank=True, default=None, null=True),
                ),
                ("exception_type", models.TextField(blank=True, default="")),
                ("exception_message", models.TextField(blank=True, default="")),
                ("exception_context", models.TextField(blank=True, default="")),
            ],
        ),
        migrations.CreateModel(
            name="AuthorizedStorageAccount",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(editable=False)),
                ("modified", models.DateTimeField()),
                ("account_name", models.CharField(blank=True, default="")),
                (
                    "int_authorized_capabilities",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.IntegerField(
                            validators=[
                                addon_service.common.enums.validators.validate_addon_capability
                            ]
                        ),
                        size=None,
                    ),
                ),
                ("default_root_folder", models.CharField(blank=True)),
            ],
            options={
                "verbose_name": "Authorized Storage Account",
                "verbose_name_plural": "Authorized Storage Accounts",
            },
        ),
        migrations.CreateModel(
            name="ConfiguredStorageAddon",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(editable=False)),
                ("modified", models.DateTimeField()),
                ("root_folder", models.CharField(blank=True)),
                (
                    "int_connected_capabilities",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.IntegerField(
                            validators=[
                                addon_service.common.enums.validators.validate_addon_capability
                            ]
                        ),
                        size=None,
                    ),
                ),
            ],
            options={
                "verbose_name": "Configured Storage Addon",
                "verbose_name_plural": "Configured Storage Addons",
            },
        ),
        migrations.CreateModel(
            name="ExternalCredentials",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(editable=False)),
                ("modified", models.DateTimeField()),
                ("credentials_blob", models.JSONField(blank=True, default=dict)),
            ],
            options={
                "verbose_name": "External Credentials",
                "verbose_name_plural": "External Credentials",
            },
        ),
        migrations.CreateModel(
            name="ExternalStorageService",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(editable=False)),
                ("modified", models.DateTimeField()),
                ("service_name", models.CharField()),
                (
                    "int_addon_imp",
                    models.IntegerField(
                        validators=[
                            addon_service.common.enums.validators.validate_storage_imp_number
                        ]
                    ),
                ),
                (
                    "int_credentials_format",
                    models.IntegerField(
                        validators=[
                            addon_service.credentials.validators.validate_credentials_format
                        ]
                    ),
                ),
                ("max_concurrent_downloads", models.IntegerField()),
                ("max_upload_mb", models.IntegerField()),
                ("auth_callback_url", models.URLField(default="")),
                (
                    "supported_scopes",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(), blank=True, null=True, size=None
                    ),
                ),
                ("api_base_url", models.URLField()),
            ],
            options={
                "verbose_name": "External Storage Service",
                "verbose_name_plural": "External Storage Services",
            },
        ),
        migrations.CreateModel(
            name="OAuth2ClientConfig",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(editable=False)),
                ("modified", models.DateTimeField()),
                ("auth_uri", models.URLField()),
                ("client_id", models.CharField(null=True)),
                ("client_secret", models.CharField(null=True)),
            ],
            options={
                "verbose_name": "OAuth2 Client Config",
                "verbose_name_plural": "OAuth2 Client Configs",
            },
        ),
        migrations.CreateModel(
            name="OAuth2TokenMetadata",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(editable=False)),
                ("modified", models.DateTimeField()),
                ("state_token", models.CharField(blank=True, db_index=True, null=True)),
                ("user_id", models.CharField(blank=True, null=True)),
                (
                    "refresh_token",
                    models.CharField(blank=True, db_index=True, null=True),
                ),
                (
                    "access_token_expiration",
                    models.DateTimeField(blank=True, null=True),
                ),
                (
                    "authorized_scopes",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(), size=None
                    ),
                ),
            ],
            options={
                "verbose_name": "OAuth2 Token Metadata",
                "verbose_name_plural": "OAuth2 Token Metadata",
            },
        ),
        migrations.CreateModel(
            name="ResourceReference",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(editable=False)),
                ("modified", models.DateTimeField()),
                ("resource_uri", models.URLField(db_index=True, unique=True)),
            ],
            options={
                "verbose_name": "Resource Reference",
                "verbose_name_plural": "Resource References",
            },
        ),
        migrations.CreateModel(
            name="UserReference",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(editable=False)),
                ("modified", models.DateTimeField()),
                ("user_uri", models.URLField(db_index=True, unique=True)),
                ("deactivated", models.DateTimeField(blank=True, null=True)),
            ],
            options={
                "verbose_name": "User Reference",
                "verbose_name_plural": "User References",
            },
        ),
        migrations.AddConstraint(
            model_name="oauth2tokenmetadata",
            constraint=models.UniqueConstraint(
                fields=("state_token",), name="unique state token"
            ),
        ),
        migrations.AddField(
            model_name="externalstorageservice",
            name="oauth2_client_config",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="external_storage_services",
                to="addon_service.oauth2clientconfig",
            ),
        ),
        migrations.AddField(
            model_name="configuredstorageaddon",
            name="authorized_resource",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="configured_storage_addons",
                to="addon_service.resourcereference",
            ),
        ),
        migrations.AddField(
            model_name="configuredstorageaddon",
            name="base_account",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="configured_storage_addons",
                to="addon_service.authorizedstorageaccount",
            ),
        ),
        migrations.AddField(
            model_name="authorizedstorageaccount",
            name="_credentials",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="authorized_storage_account",
                to="addon_service.externalcredentials",
            ),
        ),
        migrations.AddField(
            model_name="authorizedstorageaccount",
            name="account_owner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="authorized_storage_accounts",
                to="addon_service.userreference",
            ),
        ),
        migrations.AddField(
            model_name="authorizedstorageaccount",
            name="external_storage_service",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="authorized_storage_accounts",
                to="addon_service.externalstorageservice",
            ),
        ),
        migrations.AddField(
            model_name="authorizedstorageaccount",
            name="oauth2_token_metadata",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="authorized_storage_accounts",
                to="addon_service.oauth2tokenmetadata",
            ),
        ),
        migrations.AddField(
            model_name="addonoperationinvocation",
            name="by_user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="addon_service.userreference",
            ),
        ),
        migrations.AddField(
            model_name="addonoperationinvocation",
            name="thru_addon",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="addon_service.configuredstorageaddon",
            ),
        ),
        migrations.AddIndex(
            model_name="addonoperationinvocation",
            index=models.Index(
                fields=["operation_identifier"], name="addon_servi_operati_4bdf63_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="addonoperationinvocation",
            index=models.Index(
                fields=["exception_type"], name="addon_servi_excepti_35dee4_idx"
            ),
        ),
    ]
