import logging
from http import HTTPStatus

from asgiref.sync import async_to_sync
from django.http import HttpResponse

from addon_service.authorized_storage_account.models import AuthorizedStorageAccount
from addon_service.common import known_imps
from addon_service.oauth1.extrenal_account_keys import ExternalAccountKeys
from addon_service.oauth1.utils import get_access_token
from addon_service.oauth_utlis import update_external_account_id
from addon_service.osf_models.fields import decrypt_string


logger = logging.getLogger(__name__)


def oauth1_callback_view(request):
    oauth_token = request.GET["oauth_token"]
    oauth_verifier = request.GET["oauth_verifier"]

    pk = decrypt_string(request.session.get("oauth1a_account_id"))
    del request.session["oauth1a_account_id"]

    account = AuthorizedStorageAccount.objects.get(pk=pk)

    oauth1_client_config = account.external_service.oauth1_client_config
    final_credentials, other_info = async_to_sync(get_access_token)(
        access_token_url=oauth1_client_config.access_token_url,
        oauth_consumer_key=oauth1_client_config.client_key,
        oauth_consumer_secret=oauth1_client_config.client_secret,
        oauth_token=oauth_token,
        oauth_token_secret=account.temporary_oauth1_credentials.oauth_token_secret,
        oauth_verifier=oauth_verifier,
    )
    account.credentials = final_credentials
    account.save()
    update_account_with_additional_data(account, other_info)
    return HttpResponse(status=HTTPStatus.OK)  # TODO: redirect


def update_account_with_additional_data(account: AuthorizedStorageAccount, data: dict):
    imp_name = known_imps.get_imp_name(account.external_service.imp_cls)
    try:
        account.external_account_id = data[ExternalAccountKeys[imp_name]]
        account.save()
    except KeyError:
        logger.debug(
            f"Have not found external account key for {imp_name=}\n"
            f"Either this account doesn't receive external account id from oauth exchange"
            f"or there is a misconfiguration"
        )
    async_to_sync(update_external_account_id)(account)
