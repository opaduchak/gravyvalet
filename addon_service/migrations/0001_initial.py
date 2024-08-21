# Generated by Django 4.2.7 on 2024-08-20 09:47

import django.contrib.postgres.fields
import django.db.models.deletion
from django.db import (
    migrations,
    models,
)

import addon_service.common.str_uuid_field
import addon_service.common.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="AuthorizedAccount",
            fields=[
                (
                    "id",
                    addon_service.common.str_uuid_field.StrUUIDField(
                        default=addon_service.common.str_uuid_field.str_uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created", models.DateTimeField(editable=False)),
                ("modified", models.DateTimeField()),
                ("_display_name", models.CharField(blank=True, default="")),
                ("external_account_id", models.CharField(blank=True, default="")),
                (
                    "int_authorized_capabilities",
                    models.IntegerField(
                        validators=[
                            addon_service.common.validators.validate_addon_capability
                        ]
                    ),
                ),
                ("_api_base_url", models.URLField(blank=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ConfiguredAddon",
            fields=[
                (
                    "id",
                    addon_service.common.str_uuid_field.StrUUIDField(
                        default=addon_service.common.str_uuid_field.str_uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created", models.DateTimeField(editable=False)),
                ("modified", models.DateTimeField()),
                ("_display_name", models.CharField(blank=True, default="")),
                (
                    "int_connected_capabilities",
                    models.IntegerField(
                        validators=[
                            addon_service.common.validators.validate_addon_capability
                        ]
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="OAuth1ClientConfig",
            fields=[
                (
                    "id",
                    addon_service.common.str_uuid_field.StrUUIDField(
                        default=addon_service.common.str_uuid_field.str_uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created", models.DateTimeField(editable=False)),
                ("modified", models.DateTimeField()),
                ("request_token_url", models.URLField()),
                ("auth_url", models.URLField()),
                ("auth_callback_url", models.URLField()),
                ("access_token_url", models.URLField()),
                ("client_key", models.CharField(null=True)),
                ("client_secret", models.CharField(null=True)),
            ],
            options={
                "verbose_name": "OAuth1 Client Config",
                "verbose_name_plural": "OAuth1 Client Configs",
            },
        ),
        migrations.CreateModel(
            name="OAuth2ClientConfig",
            fields=[
                (
                    "id",
                    addon_service.common.str_uuid_field.StrUUIDField(
                        default=addon_service.common.str_uuid_field.str_uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created", models.DateTimeField(editable=False)),
                ("modified", models.DateTimeField()),
                ("auth_uri", models.URLField()),
                ("auth_callback_url", models.URLField()),
                ("token_endpoint_url", models.URLField()),
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
                    addon_service.common.str_uuid_field.StrUUIDField(
                        default=addon_service.common.str_uuid_field.str_uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created", models.DateTimeField(editable=False)),
                ("modified", models.DateTimeField()),
                ("state_nonce", models.CharField(blank=True, null=True)),
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
                    addon_service.common.str_uuid_field.StrUUIDField(
                        default=addon_service.common.str_uuid_field.str_uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
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
                    addon_service.common.str_uuid_field.StrUUIDField(
                        default=addon_service.common.str_uuid_field.str_uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
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
        migrations.CreateModel(
            name="AuthorizedCitationAccount",
            fields=[
                (
                    "authorizedaccount_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="addon_service.authorizedaccount",
                    ),
                ),
                ("default_root_folder", models.CharField(blank=True)),
            ],
            options={
                "verbose_name": "Authorized Citation Account",
                "verbose_name_plural": "Authorized Citation Accounts",
            },
            bases=("addon_service.authorizedaccount",),
        ),
        migrations.CreateModel(
            name="AuthorizedStorageAccount",
            fields=[
                (
                    "authorizedaccount_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="addon_service.authorizedaccount",
                    ),
                ),
                ("default_root_folder", models.CharField(blank=True)),
            ],
            options={
                "verbose_name": "Authorized Storage Account",
                "verbose_name_plural": "Authorized Storage Accounts",
            },
            bases=("addon_service.authorizedaccount",),
        ),
        migrations.CreateModel(
            name="ExternalStorageService",
            fields=[
                (
                    "id",
                    addon_service.common.str_uuid_field.StrUUIDField(
                        default=addon_service.common.str_uuid_field.str_uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created", models.DateTimeField(editable=False)),
                ("modified", models.DateTimeField()),
                ("display_name", models.CharField()),
                (
                    "int_credentials_format",
                    models.IntegerField(
                        validators=[
                            addon_service.common.validators.validate_credentials_format
                        ],
                        verbose_name="Credentials format",
                    ),
                ),
                (
                    "int_service_type",
                    models.IntegerField(
                        default=1,
                        validators=[
                            addon_service.common.validators.validate_service_type
                        ],
                        verbose_name="Service type",
                    ),
                ),
                (
                    "supported_scopes",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(), blank=True, null=True, size=None
                    ),
                ),
                ("api_base_url", models.URLField(blank=True, default="")),
                (
                    "int_addon_imp",
                    models.IntegerField(
                        validators=[
                            addon_service.common.validators.validate_storage_imp_number
                        ],
                        verbose_name="Addon implementation",
                    ),
                ),
                ("max_concurrent_downloads", models.IntegerField()),
                ("max_upload_mb", models.IntegerField()),
                ("wb_key", models.CharField(blank=True, default="")),
                (
                    "oauth1_client_config",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="external_storage_services",
                        to="addon_service.oauth1clientconfig",
                    ),
                ),
                (
                    "oauth2_client_config",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="external_storage_services",
                        to="addon_service.oauth2clientconfig",
                    ),
                ),
            ],
            options={
                "verbose_name": "External Storage Service",
                "verbose_name_plural": "External Storage Services",
            },
        ),
        migrations.CreateModel(
            name="ExternalCredentials",
            fields=[
                (
                    "id",
                    addon_service.common.str_uuid_field.StrUUIDField(
                        default=addon_service.common.str_uuid_field.str_uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created", models.DateTimeField(editable=False)),
                ("modified", models.DateTimeField()),
                ("encrypted_json", models.BinaryField()),
                ("_salt", models.BinaryField()),
                ("_scrypt_block_size", models.IntegerField()),
                ("_scrypt_cost_log2", models.IntegerField()),
                ("_scrypt_parallelization", models.IntegerField()),
            ],
            options={
                "verbose_name": "External Credentials",
                "verbose_name_plural": "External Credentials",
                "indexes": [
                    models.Index(
                        fields=["modified"], name="addon_servi_modifie_20d811_idx"
                    )
                ],
            },
        ),
        migrations.CreateModel(
            name="ExternalCitationService",
            fields=[
                (
                    "id",
                    addon_service.common.str_uuid_field.StrUUIDField(
                        default=addon_service.common.str_uuid_field.str_uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created", models.DateTimeField(editable=False)),
                ("modified", models.DateTimeField()),
                ("display_name", models.CharField()),
                (
                    "int_credentials_format",
                    models.IntegerField(
                        validators=[
                            addon_service.common.validators.validate_credentials_format
                        ],
                        verbose_name="Credentials format",
                    ),
                ),
                (
                    "int_service_type",
                    models.IntegerField(
                        default=1,
                        validators=[
                            addon_service.common.validators.validate_service_type
                        ],
                        verbose_name="Service type",
                    ),
                ),
                (
                    "supported_scopes",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(), blank=True, null=True, size=None
                    ),
                ),
                ("api_base_url", models.URLField(blank=True, default="")),
                (
                    "int_addon_imp",
                    models.IntegerField(
                        validators=[
                            addon_service.common.validators.validate_citation_imp_number
                        ],
                        verbose_name="Addon implementation",
                    ),
                ),
                (
                    "oauth1_client_config",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="external_citation_services",
                        to="addon_service.oauth1clientconfig",
                    ),
                ),
                (
                    "oauth2_client_config",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="external_citation_services",
                        to="addon_service.oauth2clientconfig",
                    ),
                ),
            ],
            options={
                "verbose_name": "External Citation Service",
                "verbose_name_plural": "External Citation Services",
            },
        ),
        migrations.CreateModel(
            name="ConfiguredStorageAddon",
            fields=[
                (
                    "configuredaddon_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="addon_service.configuredaddon",
                    ),
                ),
                ("root_folder", models.CharField(blank=True)),
                (
                    "authorized_resource",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="configured_storage_addons",
                        to="addon_service.resourcereference",
                    ),
                ),
                (
                    "base_account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="configured_storage_addons",
                        to="addon_service.authorizedstorageaccount",
                    ),
                ),
            ],
            options={
                "verbose_name": "Configured Storage Addon",
                "verbose_name_plural": "Configured Storage Addons",
            },
            bases=("addon_service.configuredaddon",),
        ),
        migrations.CreateModel(
            name="ConfiguredCitationAddon",
            fields=[
                (
                    "configuredaddon_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="addon_service.configuredaddon",
                    ),
                ),
                (
                    "authorized_resource",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="configured_citation_addons",
                        to="addon_service.resourcereference",
                    ),
                ),
                (
                    "base_account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="configured_citation_addons",
                        to="addon_service.authorizedcitationaccount",
                    ),
                ),
            ],
            options={
                "verbose_name": "Configured Citation Addon",
                "verbose_name_plural": "Configured Citation Addons",
            },
            bases=("addon_service.configuredaddon",),
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
            name="_temporary_oauth1_credentials",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="temporary_authorized_storage_account",
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
            model_name="authorizedcitationaccount",
            name="_credentials",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="authorized_citation_account",
                to="addon_service.externalcredentials",
            ),
        ),
        migrations.AddField(
            model_name="authorizedcitationaccount",
            name="_temporary_oauth1_credentials",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="temporary_authorized_citation_account",
                to="addon_service.externalcredentials",
            ),
        ),
        migrations.AddField(
            model_name="authorizedcitationaccount",
            name="account_owner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="authorized_citation_accounts",
                to="addon_service.userreference",
            ),
        ),
        migrations.AddField(
            model_name="authorizedcitationaccount",
            name="external_citation_service",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="authorized_citation_accounts",
                to="addon_service.externalcitationservice",
            ),
        ),
        migrations.AddField(
            model_name="authorizedcitationaccount",
            name="oauth2_token_metadata",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="authorized_citation_accounts",
                to="addon_service.oauth2tokenmetadata",
            ),
        ),
        migrations.CreateModel(
            name="AddonOperationInvocation",
            fields=[
                (
                    "id",
                    addon_service.common.str_uuid_field.StrUUIDField(
                        default=addon_service.common.str_uuid_field.str_uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created", models.DateTimeField(editable=False)),
                ("modified", models.DateTimeField()),
                (
                    "int_invocation_status",
                    models.IntegerField(
                        default=1,
                        validators=[
                            addon_service.common.validators.validate_invocation_status
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
                (
                    "by_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="addon_service.userreference",
                    ),
                ),
                (
                    "thru_account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="addon_service.authorizedaccount",
                    ),
                ),
                (
                    "thru_addon",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="addon_service.configuredaddon",
                    ),
                ),
            ],
            options={
                "indexes": [
                    models.Index(
                        fields=["operation_identifier"],
                        name="addon_servi_operati_4bdf63_idx",
                    ),
                    models.Index(
                        fields=["exception_type"], name="addon_servi_excepti_35dee4_idx"
                    ),
                ],
            },
        ),
    ]
