# -*- coding: utf-8 -*-

# Make coding more python3-ish
from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = r'''
name: project
author: Cyril Marin (@ziouf)
version_added: "2.10.4"
short_description: Retrieve project data
description: Retrieve project data
options:
    _terms:
        description:
            - List of TPM queries to find desired project informations
        required: True
    hostname:
        description: |
            TeamPasswordManager api hostname
            Fallback to TPM_HOST environment variable if not defined
            Expected format : hostname.domain:port/app-path-if-needed
            Examples: teampasswordmanager.com:443 or my-corporate-domainname.com/tpm-path
        required: False
    public_key:
        description: Team Password Manager api public key for HMAC authentication
        required: False
    private_key:
        description: Team Password Manager api private key for HMAC authentication
        required: False
    username:
        description: Team Password Manager api login for Basic authentication
        required: False
    password:
        description: Team Password Manager api password for Basic authentication
        required: False
    field:
        description: Field to be return
        required: False
        default: id
    wantlist:
        description: Return all results
        required: False
        type: bool
        default: False
'''

EXAMPLES = r'''
# First result
- debug: msg="{{ lookup('ziouf.tpm.project', 'myproject') }}"
# returns : dict
- debug: msg="{{ lookup('ziouf.tpm.project', 'myproject', field='name') }}"
# returns : str

# All matching results
- debug: msg="{{ lookup('ziouf.tpm.project', 'myproject', all=True) }}"
# returns : [dict, ...]
- debug: msg="{{ lookup('ziouf.tpm.project', 'myproject', all=True, field='name') }}"
# returns : [str, ...]
'''

RETURN = r'''
  _list:
    description:
        - TeamPasswordManager data matching spcified query
    type: list
    elements: json
'''

from ansible.errors import AnsibleError
from ansible.utils.display import Display
from ansible.plugins.lookup import LookupBase
from ansible.module_utils.common.dict_transformations import dict_merge
from ..module_utils.api import TpmProjectApi
from ..module_utils.base_lookup import TpmLookupBase


class LookupModule(LookupBase, TpmProjectApi):
    display = Display()

    def run(self, terms, variables=None, **kwargs):
        self.set_options(task_keys=TpmLookupBase.task_keys(
            variables), var_options=variables, direct=kwargs)

        self.config = dict_merge(TpmProjectApi.default_config(), {
            'tpm_hostname': self.get_option('hostname'),
            'tpm_public_key': self.get_option('public_key'),
            'tpm_private_key': self.get_option('private_key'),
            'tpm_username': self.get_option('username'),
            'tpm_password': self.get_option('password'),
            'use_hmac': all([self.get_option('public_key'), self.get_option('private_key')]),
        })

        return [self.fn_map(item) for item in self.fn_find(next(query for query in terms))]

    def fn_map(self, item):
        print(self._options)
        if self.get_option('field') == 'all':
            return item
        if self.get_option('field') in item:
            return item[self.get_option('field')]
        return item

    def fn_find(self, query):
        try:
            self.display.vv(
                msg='Searching matching projects for query : "{q}"'.format(q=query))

            # Find matching passwords
            result = self.find(query_str=query)
            result.sort(key=lambda x: x['name'])

            self.display.vv(msg='Found {l} results for query "{q}"'.format(
                q=query, l=len(result)))
            self.display.debug(
                msg='Query: "{q}" | Result: {r}'.format(q=query, r=result))

            if self.get_option('wantlist') or False:
                return result

            return [next(r for r in result)]

        except Exception as e:
            msg = 'Query "{q}" did not match any result'.format(q=query)
            raise AnsibleError(e, msg)
