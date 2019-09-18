# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from datetime import datetime, timedelta
from knack.util import CLIError
from azure.mgmt.media.models import AssetContainerPermission


def create_asset(client, account_name, resource_group_name, asset_name, alternate_id=None, description=None,
                 storage_account=None, container=None):
    from azure.mgmt.media.models import Asset

    asset = Asset(alternate_id=alternate_id, description=description, storage_account_name=storage_account,
                  container=container)

    return client.create_or_update(resource_group_name, account_name, asset_name, asset)


def get_sas_urls(client, resource_group_name, account_name, asset_name, permissions=AssetContainerPermission.read.value,
                 expiry_time=(datetime.now() + timedelta(hours=23))):
    return client.list_container_sas(resource_group_name, account_name,
                                     asset_name, permissions, expiry_time).asset_container_sas_urls


def get_asset(client, account_name, resource_group_name, asset_name):
    asset = client.get(resource_group_name, account_name, asset_name)
    if not asset:
        raise CLIError('The asset resource was not found.')

    return asset


def update_asset(instance, alternate_id=None, description=None):
    if not instance:
        raise CLIError('The asset resource was not found.')

    if alternate_id:
        instance.alternate_id = alternate_id

    if description:
        instance.description = description

    return instance


def get_encryption_key(client, account_name, resource_group_name, asset_name):
    import binascii
    storage_encrypted_asset = client.get_encryption_key(resource_group_name, account_name, asset_name)
    storage_encrypted_asset.key = binascii.b2a_base64(storage_encrypted_asset.key, newline=False)
    return storage_encrypted_asset
