# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import traceback

from ansible.module_utils.basic import (
    AnsibleModule,
    env_fallback,
)
from ansible.module_utils.common.dict_transformations import dict_merge

from .api import TpmApiBase, FindError


class AlreadyExistsError(Exception):
    """Creation failed. Item already exists"""


class StateNotImplementedError(Exception):
    """Specified state is not implemented"""


class TpmModuleBase(AnsibleModule):
    """TPM Module base implementation"""

    __arg_spec_base: dict = dict(
        # Expected state
        state=dict(
            type='str',
            choices=['present', 'absent', 'update'],
            required=True,
        ),
        # Api connection informations
        tpm_hostname=dict(
            type='str',
            required=True,
            fallback=(env_fallback, ['TPM_HOST']),
        ),
        tpm_ssl_verify=dict(
            type='bool',
            required=False,
            default=True,
        ),
        # Basic auth
        tpm_username=dict(
            type='str',
            fallback=(env_fallback, ['TPM_USER']),
        ),
        tpm_password=dict(
            type='str',
            fallback=(env_fallback, ['TPM_PASS']),
            no_log=True,
        ),
        # HMAC auth
        tpm_public_key=dict(
            type='str',
            fallback=(env_fallback, ['TPM_PUBLIC_KEY']),
        ),
        tpm_private_key=dict(
            type='str',
            fallback=(env_fallback, ['TPM_PRIVATE_KEY']),
            no_log=True,
        ),
    )
    __mutually_exclusive: list = [
        ('tpm_username', 'tpm_public_key'),
        ('tpm_password', 'tpm_private_key'),
    ]
    __required_together: list = [
        ('tpm_username', 'tpm_password'),
        ('tpm_public_key', 'tpm_private_key'),
    ]
    __required_one_of: list = [
        ('tpm_username', 'tpm_public_key'),
        ('tpm_password', 'tpm_private_key'),
    ]

    def __init__(self,
                 argument_spec=None,
                 bypass_checks=False,
                 no_log=False,
                 mutually_exclusive=None,
                 required_together=None,
                 required_one_of=None,
                 add_file_common_args=False,
                 supports_check_mode=False,
                 required_if=None,
                 required_by=None):
        argument_spec = argument_spec or {}
        required_by = required_by or {}
        mutually_exclusive = mutually_exclusive or []
        required_together = required_together or []
        required_one_of = required_one_of or []

        argument_spec = dict_merge(TpmModuleBase.__arg_spec_base, argument_spec)
        mutually_exclusive.extend(TpmModuleBase.__mutually_exclusive)
        required_together.extend(TpmModuleBase.__required_together)
        required_one_of.extend(TpmModuleBase.__required_one_of)

        super().__init__(
            argument_spec,
            bypass_checks=bypass_checks,
            no_log=no_log,
            mutually_exclusive=mutually_exclusive,
            required_together=required_together,
            required_one_of=required_one_of,
            add_file_common_args=add_file_common_args,
            supports_check_mode=supports_check_mode,
            required_if=required_if,
            required_by=required_by
        )

        self.config = dict_merge(TpmApiBase.default_config(), {
            'tpm_hostname': self.params.get('tpm_hostname'),
            'tpm_public_key': self.params.get('tpm_public_key'),
            'tpm_private_key': self.params.get('tpm_private_key'),
            'tpm_username': self.params.get('tpm_username'),
            'tpm_password': self.params.get('tpm_password'),
            'tpm_ssl_verify': self.params.get('tpm_ssl_verify'),
            'use_hmac': all(['tpm_public_key' in self.params, 'tpm_private_key' in self.params]),
        })

    def run(self):
        """Run create/update actions"""
        fn = {
            'present': self.fn_present,
            'absent': self.fn_absent,
            'update': self.fn_update,
        }.get(self.params.get('state', self.fn_default))

        try:
            r = fn()

        except AlreadyExistsError as e:
            self.exit_json(
                changed=False,
                result={'tpm': e.args}
            )

        except Exception as e:
            self.fail_json(
                changed=False,
                error=str(e),
                stacktrace=traceback.format_exc().splitlines(),
            )

        else:
            self.exit_json(
                changed=True,
                result={'tpm': r},
            )

    def fn_default(self) -> dict:
        raise StateNotImplementedError()

    def fn_present(self) -> dict:
        data: dict = self.params.get('data', {})

        try:
            # First find existing secret with the verysame name
            item = self.findFirst(data.get('name'), default=None)

        except FindError:
            return self.create(**data)

        else:
            raise AlreadyExistsError(item)

    def fn_absent(self) -> dict:
        data: dict = self.params.get('data', {})

        try:
            # First find existing secret with the verysame name
            item = self.findFirst(data.get('name'), default=None)

        except FindError as e:
            raise e

        else:
            return self.delete(item['id'])

    def fn_update(self) -> dict:
        data: dict = self.params.get('data', {})

        try:
            # First find existing secret with the verysame name
            item = self.findFirst(data.get('name'), default=None)

        except FindError as e:
            raise e

        else:
            return self.update(item['id'], **data)
