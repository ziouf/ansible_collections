# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import re
import hmac
import hashlib
import codecs
import json
import time

try:
    from urllib import quote        # Python 2.x
except ImportError:
    from urllib.parse import quote  # Python 3+

from ansible.module_utils.urls import open_url
from ansible.module_utils.common.dict_transformations import dict_merge


class OpenUrlError(Exception):
    """Failed to open given url"""


class GenerateError(Exception):
    """Generate call to TPM api failed"""


class GetError(Exception):
    """Get call to TPM api failed"""


class FindError(Exception):
    """Find call to TPM api failed"""


class CreateError(Exception):
    """Create call to TPM api failed"""


class UpdateError(Exception):
    """Update call to TPM api failed"""


class DeleteError(Exception):
    """Delete call to TPM api failed"""


class TpmApiBase():
    """Base class for REST queries to TPM

    Raises:
        OpenUrlError: Failed to HTTP GET
        OpenUrlError: Failed to HTTP POST
        OpenUrlError: Failed to HTTP PUT
        OpenUrlError: Failed to HTTP DELETE

    Returns:
        json: API resposne
    """

    @staticmethod
    def default_headers():
        return {
            "Content-Type": "application/json; charset=utf-8",
        }

    @staticmethod
    def default_config():
        return {
            'tpm_ssl_verify': True,
        }

    def __init__(self, config = None):
        self.config = dict_merge(TpmApiBase.default_config(), config or {})

        # Determine which login method to use
        if all([config.get('tpm_public_key', None),
                config.get('tpm_private_key', None)]):
            self.config['use_hmac'] = True
            self.config.pop('tpm_username')
            self.config.pop('tpm_password')

    def __get_headers(self, path, data = None):
        if self.config.get('use_hmac', False):
            timestamp = str(int(time.time()))
            msg_data = [path, timestamp] + ([json.dumps(data)] if data else [])
            headers = dict_merge(TpmApiBase.default_headers(), {
                "X-Public-Key": self.config.get('tpm_public_key'),
                "X-Request-Hash": self.__sha256_signature(''.join(msg_data)),
                "X-Request-Timestamp": timestamp,
            })
            return headers
        # Else, return default headers
        return TpmApiBase.default_headers()

    def __sha256_signature(self, msg):
        key = self.config.get('tpm_private_key')

        return hmac.new(
            digestmod=hashlib.sha256,
            key=codecs.encode(key),
            msg=codecs.encode(msg),
        ).hexdigest()

    def __get_url(self, path):
        return 'https://{host}/index.php/{path}'.format(
            host=self.config.get('tpm_hostname'),
            path=path
        )

    def _http_get(self, path):
        r = open_url(self.__get_url(path), method='GET',
                     headers=self.__get_headers(path),
                     url_username=self.config.get('tpm_username', None),
                     url_password=self.config.get('tpm_password', None),
                     force_basic_auth='tpm_username' in self.config,
                     validate_certs=self.config.get('tpm_ssl_verify'),
                     )

        if r.status == 200:
            try:
                next_page_link = r.getHeader('Link', default=None)
                if next_page_link:
                    matcher = re.search('<https://.+/index.php/(.+)>; rel="next"', next_page_link)
                    next_page = self._http_get(matcher.group(1))

                return json.load(r) + next_page if next_page else json.load(r)

            except Exception:
                return json.loads(r)

        raise OpenUrlError('HTTP {s} - Failed to GET data'.format(s=r.status))

    def _http_post(self, path, body = None):
        r = open_url(self.__get_url(path), method='POST',
                     headers=self.__get_headers(path, data=body),
                     data=body,
                     url_username=self.config.get('tpm_username', None),
                     url_password=self.config.get('tpm_password', None),
                     force_basic_auth='tpm_username' in self.config,
                     validate_certs=self.config.get('tpm_ssl_verify'),
                     )

        if r.status == 201:
            return json.load(r)

        raise OpenUrlError('HTTP {s} - Failed to POST data'.format(s=r.status))

    def _http_put(self, path, body = None):
        r = open_url(self.__get_url(path), method='PUT',
                     headers=self.__get_headers(path, data=body),
                     data=body,
                     url_username=self.config.get('tpm_username', None),
                     url_password=self.config.get('tpm_password', None),
                     force_basic_auth='tpm_username' in self.config,
                     validate_certs=self.config.get('tpm_ssl_verify'),
                     )

        if r.status == 204:
            return {}

        raise OpenUrlError('HTTP {s} - Failed to PUT data'.format(s=r.status))

    def _http_delete(self, path):
        r = open_url(self.__get_url(path), method='DELETE',
                     headers=self.__get_headers(path),
                     url_username=self.config.get('tpm_username', None),
                     url_password=self.config.get('tpm_password', None),
                     force_basic_auth='tpm_username' in self.config,
                     validate_certs=self.config.get('tpm_ssl_verify'),
                     )

        if r.status == 204:
            return {}

        raise OpenUrlError('HTTP {s} - Failed to DELETE data'.format(s=r.status))


class TpmPasswordApi(TpmApiBase):
    """TPM Password API implementation"""

    def getById(self, id = 0):
        '''
        Return data found from TPM for the given ID
        '''
        try:
            return self._http_get(path='api/v4/passwords/{id}.json'.format(id=id))
        except Exception as e:
            raise GetError(e)

    def find(self, query_str = ''):
        '''
        Return data found from TPM for the given query string
        '''
        try:
            return self._http_get(
                path='api/v4/passwords/search/{q}.json'.format(
                    q=quote(query_str.encode('utf-8'))),
            )
        except Exception as e:
            raise FindError(e)

    def findFirst(self, query_str = '', default=None):
        '''
        Return first find result
        '''
        return next((i for i in self.find(query_str)), default)

    def generate(self):
        '''
        Return new generated password from TPM
        '''
        try:
            return self._http_get(path='api/v4/generate_password.json')
        except Exception as e:
            raise GenerateError(e)

    def create(self, project_name, name,
               tags = None,
               access_info = None,
               username = None,
               email = None,
               password = None,
               expiry_date = None,
               notes = None,
               custom_data1 = None,
               custom_data2 = None,
               custom_data3 = None,
               custom_data4 = None,
               custom_data5 = None,
               custom_data6 = None,
               custom_data7 = None,
               custom_data8 = None,
               custom_data9 = None,
               custom_data10 = None,
               ):
        '''
        Return newly created password
        '''
        project_api = TpmProjectApi()
        project = project_api.findFirst(project_name)

        data = dict(
            project_id=project.id,
            name=name,
            tags=','.join(tags),
            access_info=access_info,
            username=username,
            email=email,
            password=password or self.generate()['password'],
            # expiry_date=expiry_date,
            notes=notes,
            custom_data1=custom_data1,
            custom_data2=custom_data2,
            custom_data3=custom_data3,
            custom_data4=custom_data4,
            custom_data5=custom_data5,
            custom_data6=custom_data6,
            custom_data7=custom_data7,
            custom_data8=custom_data8,
            custom_data9=custom_data9,
            custom_data10=custom_data10,
        )

        try:
            r = self._http_post(
                path='api/v4/passwords.json',
                body=data
            )
            return self.getById(r['id'])

        except Exception as e:
            raise CreateError(e)

    def update(self, id, name,
               tags = None,
               access_info = None,
               username = None,
               email = None,
               password = None,
               expiry_date = None,
               notes = None,
               custom_data1 = None,
               custom_data2 = None,
               custom_data3 = None,
               custom_data4 = None,
               custom_data5 = None,
               custom_data6 = None,
               custom_data7 = None,
               custom_data8 = None,
               custom_data9 = None,
               custom_data10 = None,
               ):
        '''
        Return updated password
        '''
        entry = self.getById(id)

        data = dict(
            name=name or entry.get('name'),
            tags=','.join(set(entry.get('tags').split(',') + tags)),
            access_info=access_info or entry.get('access_info'),
            username=username or entry.get('username'),
            email=email or entry.get('email'),
            password=password or self.generate().get('password'),
            expiry_date=expiry_date or entry.get('expiry_date'),
            notes=notes or entry.get('notes'),
            custom_data1=custom_data1 or entry.get(
                'custom_field1', dict(data=None))['data'],
            custom_data2=custom_data2 or entry.get(
                'custom_field2', dict(data=None))['data'],
            custom_data3=custom_data3 or entry.get(
                'custom_field3', dict(data=None))['data'],
            custom_data4=custom_data4 or entry.get(
                'custom_field4', dict(data=None))['data'],
            custom_data5=custom_data5 or entry.get(
                'custom_field5', dict(data=None))['data'],
            custom_data6=custom_data6 or entry.get(
                'custom_field6', dict(data=None))['data'],
            custom_data7=custom_data7 or entry.get(
                'custom_field7', dict(data=None))['data'],
            custom_data8=custom_data8 or entry.get(
                'custom_field8', dict(data=None))['data'],
            custom_data9=custom_data9 or entry.get(
                'custom_field9', dict(data=None))['data'],
            custom_data10=custom_data10 or entry.get(
                'custom_field10', dict(data=None))['data'],
        )

        try:
            self._http_put(
                path='api/v4/passwords/{id}.json'.format(id=id),
                body=data
            )
            return self.getById(id)

        except Exception as e:
            raise UpdateError(e)


class TpmProjectApi(TpmApiBase):
    """TPM Project API implementation"""

    def getById(self, id):
        '''
        Return data found from TPM for the given ID
        '''
        try:
            return self._http_get(path='api/v4/projects/{id}.json'.format(id=id))
        except Exception as e:
            raise GetError(e)

    def find(self, query_str=''):
        '''
        Return data found from TPM for the given query string
        '''
        try:
            return self._http_get(
                path='api/v4/projects/search/{q}.json'.format(
                    q=quote(query_str.encode('utf-8')))
            )
        except Exception as e:
            raise FindError(e)

    def findFirst(self, query_str='', default=None):
        '''
        Return first find result
        '''
        return next((i for i in self.find(query_str)), default)

    def create(self, name, parent_id, tags = None, notes = None):
        '''
        Return newly created project
        '''
        tags = tags or []
        data = dict(
            name=name,
            parent_id=parent_id,
            tags=','.join(tags),
            notes=notes,
        )

        try:
            r = self._http_post(
                path='api/v4/projects.json',
                body=data
            )
            return self.getById(r['id'])

        except Exception as e:
            raise CreateError(e)

    def update(self, id, name, tags = None, notes = None):
        '''
        Return updated project
        '''
        tags = tags or []
        entry = self.getById(id)

        data = dict(
            name=name,
            tags=','.join(set(entry.get('tags', '').split(',') + tags)),
            notes=notes or entry.get('notes')
        )

        try:
            r = self._http_put(
                path='api/v4/projects/{id}.json'.format(id=id),
                body=data
            )
            return self.getById(r['id'])

        except Exception as e:
            raise CreateError(e)

    def delete(self, id):
        '''
        Delete specified project
        '''
        try:
            self._http_delete(
                path='api/v4/projects/{id}.json'.format(id=id)
            )
            return "Successfully deleted project"

        except Exception as e:
            raise DeleteError(e)
