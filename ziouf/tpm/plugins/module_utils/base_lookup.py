# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os


class TpmLookupBase():
    """TPM Lookup Module base implementation"""

    @staticmethod
    def task_keys(variables):
        keys = {
            'hostname': 'TPM_HOST',
            'public_key': 'TPM_PUBLIC_KEY',
            'private_key': 'TPM_PRIVATE_KEY',
            'username': 'TPM_USER',
            'password': 'TPM_PASS',
        }
        return {k: variables.get('tpm_{k}'.format(k=k), os.getenv(v)) for k, v in keys.items()}
