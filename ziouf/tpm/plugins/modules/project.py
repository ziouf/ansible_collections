#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) 2017 Geodis IT SAS - ISSC
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# Make coding more python3-ish
from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = r'''
module: project
author: Cyril Marin (@ziouf)
short_description: Create or update project
description: This module create or updates password entry in TeamPasswordManager instance
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
            Fallback to TPM_USER  environment variable if not defined
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
        description: Project name
        type: str
        required: true
    parent_id:
        description: Project parent id
        type: int
    tags:
        description: Tag list of the project
        type: list
        elements: str
    notes:
        description: Free text notes
        type: str
'''

EXAMPLES = r'''

'''

RETURN = r'''
tpm:
    description: ''
    returned: success
    type: dict
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
            sample: 1234
        parent_id:
            description: Parent id of the project
            returned: success
            type: int
        tags:
            description: Tag list (comma separated)
            returned: success
            type: str
        notes:
            description: Notes
            returned: success
            type: str
        archived:
            description: Archived
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

from ..module_utils.api import TpmProjectApi
from ..module_utils.base_module import TpmModuleBase


class TpmModule(TpmModuleBase, TpmProjectApi):
    pass


def main():
    TpmModule(
        argument_spec=dict(
            name=dict(type='str', required=True),
            parent_id=dict(type='int', default=0),
            tags=dict(type='list', default=[], elements='str'),
            notes=dict(type='str', default=None),
        ),
        supports_check_mode=False,
    ).run()


if __name__ == "__main__":
    main()
