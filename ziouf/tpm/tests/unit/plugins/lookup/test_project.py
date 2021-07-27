# -*- coding: utf-8 -*-
# (c) 2020, Adam Migus <adam@migus.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# Make coding more python3-ish
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from unittest import TestCase

try:                                # Python 3+
    from unittest.mock import (
        patch,
        MagicMock,
    )
except ImportError:                 # Python 2.x
    from mock import (
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

def mock_find(*args, **kwargs):
    return MOCK_RESPONSE_FIND


class TestLookupModule(TestCase):
    def setUp(self):
        self.lookup = lookup_loader.get('ziouf.tpm.project')

    def test_get_all_id(self):
        with patch.object(self.lookup, 'find', new=mock_find):

            self.assertListEqual(
                [i['id'] for i in MOCK_RESPONSE_FIND], 
                self.lookup.run(['test query'], {}, wantlist=True)
            )

    def test_get_all_name(self):
        with patch.object(self.lookup, 'find', new=mock_find):

            self.assertListEqual(
                [i['name'] for i in MOCK_RESPONSE_FIND], 
                self.lookup.run(['test query'], {}, wantlist=True, field='name')
            )

    def test_get_all_full_project(self):
        with patch.object(self.lookup, 'find', new=mock_find):

            self.assertListEqual(
                [i for i in MOCK_RESPONSE_FIND], 
                self.lookup.run(['test query'], {}, wantlist=True, field='all')
            )

    def test_get_first_id(self):
        with patch.object(self.lookup, 'find', new=mock_find):

            self.assertListEqual(
                [MOCK_RESPONSE_FIND[0]['id']], 
                self.lookup.run(['test query'], {})
            )

    def test_get_first_name(self):
        with patch.object(self.lookup, 'find', new=mock_find):

            self.assertListEqual(
                [MOCK_RESPONSE_FIND[0]['name']],
                self.lookup.run(['test query'], {}, field='name')
            )

    def test_get_first_full_project(self):
        with patch.object(self.lookup, 'find', new=mock_find):

            self.assertListEqual(
                [MOCK_RESPONSE_FIND[0]], 
                self.lookup.run(['test query'], {}, field='all')
            )
    