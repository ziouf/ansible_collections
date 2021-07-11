#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) 2017 Geodis IT SAS - ISSC
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# Make coding more python3-ish
from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = r'''
module: password
author: Cyril Marin (@ziouf)
short_description: Create or update password
description: This module create or updates password entry in your Team Password Manager instance
version_added: "2.10.4"
options:
    state:
        description: ""
        choices: [present, absent, update]
        type: str
        required: true
    tpm_hostname:
        description: |
            TeamPasswordManager api hostname (ex: my.compagny.com/tpm)
            Fallback to TPM_HOST environment variable if not defined
        type: str
        required: true
    tpm_username:
        description: |
            TeamPasswordManager login for Basic auth
            Fallback to TPM_USER environment variable if not defined
        type: str
    tpm_password:
        description: |
            TeamPasswordManager password for Basic auth
            Fallback to TPM_PASS environment variable if not defined
        type: str
    tpm_public_key:
        description: |
            TeamPasswordManager public key for HMAC auth
            Fallback to TPM_PUBLIC_KEY environment variable if not defined
        type: str
    tpm_private_key:
        description: |
            TeamPasswordManager private key for HMAC auth
            Fallback to TPM_PRIVATE_KEY environment variable if not defined
        type: str
    tpm_ssl_verify:
        description: Validate or not SSL certificates on API connection
        type: bool
        default: true
    name:
        description: Password name
        type: str
        required: true
    project_name:
        description: Project name
        type: str
    tags:
        description: Tag list
        type: list
        elements: str
    access_info:
        description: Url
        type: str
    username:
        description: Username
        type: str
    email:
        description: email
        type: str
    password:
        description: If not defined, the value is generated with Team Password Manager api
        type: str
    expiry_date:
        description: "Expiration date (fmt: yyyy-mm-dd)"
        type: str
    notes:
        description: Free text note
        type: str
    custom_data1:
        description: Custom data field
        type: str
    custom_data2:
        description: Custom data field
        type: str
    custom_data3:
        description: Custom data field
        type: str
    custom_data4:
        description: Custom data field
        type: str
    custom_data5:
        description: Custom data field
        type: str
    custom_data6:
        description: Custom data field
        type: str
    custom_data7:
        description: Custom data field
        type: str
    custom_data8:
        description: Custom data field
        type: str
    custom_data9:
        description: Custom data field
        type: str
    custom_data10:
        description: Custom data field
        type: str
'''

EXAMPLES = r'''

'''

RETURN = r'''
tpm:
    description: ''
    returned: success
    type: complex
    contains:
        id:
            description: Internal ID of the password entry
            returned: success
            type: int
            sample: 1234
        name:
            description: Name of the password entry
            returned: success
            type: str
        project:
            description: Project
            returned: success
            type: complex
            contains:
                id:
                    description: Project ID
                    returned: success
                    type: int
                    sample: 1234
                name:
                    description: Project name
                    returned: success
                    type: str
        tags:
            description: Tag list (comma separated)
            returned: success
            type: str
        access_info:
            description: Url
            returned: success
            type: str
        username:
            description: Username
            returned: success
            type: str
        email:
            description: email
            returned: success
            type: str
        password:
            description: Password value
            returned: success
            type: str
        expiry_date:
            description: Expiry date
            returned: success
            type: str
        expiry_status:
            description: 'has the following values: 0=no date or not expired, 1=expires today, 2=expired, 3=will expire soon'
            returned: success
            type: int
        notes:
            description: Notes
            returned: success
            type: str
        custom_fieldN:
            description: Custom field
            returned: success
            type: complex
            contains:
                type:
                    description: Can be one of 'Text', 'Encrypted text', 'E-mail' or 'email, 'Password', 'Notes', 'Encrypted notes'
                    returned: success
                    type: str
                label:
                    description: Custom type label
                    returned: success
                    type: str
                data:
                    description: Custom type data
                    returned: success
                    type: str
        archived:
            description: Archived
            returned: success
            type: bool
        locked:
            description: Locked
            returned: success
            type: bool
        created_on:
            description: Creation date
            returned: success
            type: str
        updated_on:
            description: Last update date
            returned: success
            type: str
'''

from ..module_utils.api import TpmPasswordApi
from ..module_utils.base_module import TpmModuleBase


class TpmModule(TpmModuleBase, TpmPasswordApi):
    pass


def main():
    TpmModule(
        argument_spec=dict(
            name=dict(type='str', required=True),
            project_name=dict(type='str'),
            tags=dict(type='list', default=[], elements='str'),
            access_info=dict(type='str', default=None),
            username=dict(type='str', default=None),
            email=dict(type='str', default=None),
            password=dict(type='str', default=None, no_log=True),
            expiry_date=dict(type='str', default=None),
            notes=dict(type='str', default=None),
            custom_data1=dict(type='str', default=None),
            custom_data2=dict(type='str', default=None),
            custom_data3=dict(type='str', default=None),
            custom_data4=dict(type='str', default=None),
            custom_data5=dict(type='str', default=None),
            custom_data6=dict(type='str', default=None),
            custom_data7=dict(type='str', default=None),
            custom_data8=dict(type='str', default=None),
            custom_data9=dict(type='str', default=None),
            custom_data10=dict(type='str', default=None),
        ),
        required_if=[
            ('state', 'present', ('name', 'project_name')),
            ('state', 'absent', ('name',)),
            ('state', 'update', ('name',)),
        ],
        supports_check_mode=False,
    ).run()


if __name__ == "__main__":
    main()
