# -*- coding: utf-8 -*-
# (c) 2020, Adam Migus <adam@migus.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# Make coding more python3-ish
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from unittest import TestCase
from unittest.mock import (
    patch,
    MagicMock,
)

# from ansible_collections.ziouf.tpm.plugins.lookup import password
from ansible.plugins.loader import lookup_loader

MOCK_RESPONSE_FIND = [
    {
        "id": 0,
        "name": "test0",
    },
    {
        "id": 1,
        "name": "test1",
    },
]
MOCK_RESPONSE_GET = {
    0: {
        "id": 0,
        "name": "test0",
        "password": "My5uperP@$$w0rd",
    },
    1: {
        "id": 1,
        "name": "test1",
        "password": "My0therP@$$w0rd",
    },
}

def mock_find(*args, **kwargs):
    return MOCK_RESPONSE_FIND

def mock_getById(id, *args, **kwargs):
    return MOCK_RESPONSE_GET[id]


class TestLookupModule(TestCase):
    def setUp(self):
        self.lookup = lookup_loader.get('ziouf.tpm.password')

    def test_get_all_password(self):
        with patch.object(self.lookup, 'find', new=mock_find), \
             patch.object(self.lookup, 'getById', new=mock_getById):

            self.assertListEqual(
                [i['password'] for i in MOCK_RESPONSE_GET.values()], 
                self.lookup.run(['test query'], {}, wantlist=True)
            )

    def test_get_all_secret_field(self):
        with patch.object(self.lookup, 'find', new=mock_find), \
             patch.object(self.lookup, 'getById', new=mock_getById):

            self.assertListEqual(
                [i['name'] for i in MOCK_RESPONSE_GET.values()], 
                self.lookup.run(['test query'], {}, wantlist=True, field='name')
            )

    def test_get_all_full_secret(self):
        with patch.object(self.lookup, 'find', new=mock_find), \
             patch.object(self.lookup, 'getById', new=mock_getById):

            self.assertListEqual(
                [i for i in MOCK_RESPONSE_GET.values()], 
                self.lookup.run(['test query'], {}, wantlist=True, field='all')
            )

    def test_get_first_password(self):
        with patch.object(self.lookup, 'find', new=mock_find), \
             patch.object(self.lookup, 'getById', new=mock_getById):

            self.assertListEqual(
                [MOCK_RESPONSE_GET[0]['password']], 
                self.lookup.run(['test query'], {})
            )

    def test_get_first_secret_field(self):
        with patch.object(self.lookup, 'find', new=mock_find), \
             patch.object(self.lookup, 'getById', new=mock_getById):

            self.assertListEqual(
                [MOCK_RESPONSE_GET[0]['name']],
                self.lookup.run(['test query'], {}, field='name')
            )

    def test_get_first_full_secret(self):
        with patch.object(self.lookup, 'find', new=mock_find), \
             patch.object(self.lookup, 'getById', new=mock_getById):

            self.assertListEqual(
                [MOCK_RESPONSE_GET[0]], 
                self.lookup.run(['test query'], {}, field='all')
            )
    