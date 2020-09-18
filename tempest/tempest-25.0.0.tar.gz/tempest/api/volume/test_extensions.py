# Copyright 2013 IBM Corp.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from oslo_log import log as logging

from tempest.api.volume import base
from tempest import config
from tempest.lib import decorators

CONF = config.CONF


LOG = logging.getLogger(__name__)


class ExtensionsTestJSON(base.BaseVolumeTest):
    """Test volume extensions"""

    @decorators.idempotent_id('94607eb0-43a5-47ca-82aa-736b41bd2e2c')
    def test_list_extensions(self):
        """Test listing volume extensions"""
        extensions = (self.volumes_extension_client.list_extensions()
                      ['extensions'])
        if not CONF.volume_feature_enabled.api_extensions:
            raise self.skipException('There are not any extensions configured')
        extension_list = [extension.get('alias') for extension in extensions]
        LOG.debug("Cinder extensions: %s", ','.join(extension_list))
        ext = CONF.volume_feature_enabled.api_extensions[0]
        if ext == 'all':
            self.assertIn('Hosts', map(lambda x: x['name'], extensions))
        elif ext:
            self.assertIn(ext, map(lambda x: x['alias'], extensions))
        else:
            raise self.skipException('There are not any extensions configured')
