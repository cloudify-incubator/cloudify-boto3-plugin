# Copyright (c) 2017 GigaSpaces Technologies Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
#    * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    * See the License for the specific language governing permissions and
#    * limitations under the License.

from cloudify_awssdk.rds.resources import subnet_group
from botocore.exceptions import UnknownServiceError

from mock import patch, MagicMock
import unittest

from cloudify.state import current_ctx

from cloudify_awssdk.common.tests.test_base import TestBase, CLIENT_CONFIG
from cloudify_awssdk.common.tests.test_base import DELETE_RESPONSE

# Constants
SUBNET_GROUP_TH = ['cloudify.nodes.Root',
                   'cloudify.nodes.aws.rds.SubnetGroup']

NODE_PROPERTIES = {
    'use_external_resource': False,
    'resource_id': 'zzzzzz-subnet-group',
    'client_config': CLIENT_CONFIG
}

RUNTIME_PROPERTIES = {
    'resource_config': {
        'SubnetIds': ['subnet-xxxxxxxx', 'subnet-yyyyyyyy'],
        'DBSubnetGroupDescription': 'MySQL5.7 Subnet Group',
        'DBSubnetGroupName': 'zzzzzz-subnet-group'
    }
}


class TestRDSSubnetGroup(TestBase):

    def setUp(self):
        super(TestRDSSubnetGroup, self).setUp()

        self.fake_boto, self.fake_client = self.fake_boto_client('rds')

        self.mock_patch = patch('boto3.client', self.fake_boto)
        self.mock_patch.start()

    def tearDown(self):
        self.mock_patch.stop()
        self.fake_boto = None
        self.fake_client = None

        super(TestRDSSubnetGroup, self).tearDown()

    def test_create_raises_UnknownServiceError(self):
        _test_node_properties = {
            'use_external_resource': False
        }
        _test_runtime_properties = {
            'resource_config': {}
        }
        _ctx = self.get_mock_ctx(
            'test_create_UnknownServiceError',
            test_properties=_test_node_properties,
            test_runtime_properties=_test_runtime_properties,
            type_hierarchy=SUBNET_GROUP_TH
        )
        current_ctx.set(_ctx)

        with self.assertRaises(UnknownServiceError) as error:
            subnet_group.create(ctx=_ctx, resource_config=None, iface=None)

        self.assertEqual(
            str(error.exception),
            "Unknown service: 'rds'. Valid service names are: ['rds']"
        )

        self.fake_boto.assert_called_with('rds', region_name=None)

    def test_create(self):
        _ctx = self.get_mock_ctx(
            'test_create',
            test_properties=NODE_PROPERTIES,
            test_runtime_properties=RUNTIME_PROPERTIES,
            type_hierarchy=SUBNET_GROUP_TH
        )

        current_ctx.set(_ctx)

        self.fake_client.describe_db_subnet_groups = MagicMock(
            return_value={'DBSubnetGroups': [{
                'SubnetGroupStatus': 'Complete',
                'DBSubnetGroup': {
                    'DBSubnetGroupName': 'zzzzzz-subnet-group',
                    'DBSubnetGroupArn': 'DBSubnetGroupArn'
                }
            }]}
        )

        self.fake_client.create_db_subnet_group = MagicMock(
            return_value={'DBSubnetGroup': {
                'DBSubnetGroupName': 'zzzzzz-subnet-group',
                'DBSubnetGroupArn': 'DBSubnetGroupArn'}
            }
        )

        subnet_group.create(ctx=_ctx, resource_config=None, iface=None)

        self.fake_boto.assert_called_with(
            'rds', **CLIENT_CONFIG
        )
        self.fake_client.create_db_subnet_group.assert_called_with(
            DBSubnetGroupDescription='MySQL5.7 Subnet Group',
            DBSubnetGroupName='zzzzzz-subnet-group',
            SubnetIds=['subnet-xxxxxxxx', 'subnet-yyyyyyyy']
        )
        self.fake_client.describe_db_subnet_groups.assert_called_with(
            DBSubnetGroupName='zzzzzz-subnet-group'
        )

        self.assertEqual(
            _ctx.instance.runtime_properties, {
                'aws_resource_arn': 'DBSubnetGroupArn',
                'aws_resource_id': 'zzzzzz-subnet-group',
                'resource_config': {
                    'DBSubnetGroupDescription':
                                    'MySQL5.7 Subnet Group',
                    'DBSubnetGroupName': 'zzzzzz-subnet-group',
                    'SubnetIds': ['subnet-xxxxxxxx', 'subnet-yyyyyyyy']
                }
            }
        )

    def test_prepare(self):
        self._prepare_check(
            type_hierarchy=SUBNET_GROUP_TH,
            type_name='rds',
            type_class=subnet_group
        )

    def test_delete(self):
        _ctx = self.get_mock_ctx(
            'test_delete',
            test_properties=NODE_PROPERTIES,
            test_runtime_properties=RUNTIME_PROPERTIES,
            type_hierarchy=SUBNET_GROUP_TH
        )

        current_ctx.set(_ctx)

        self.fake_client.delete_db_subnet_group = MagicMock(
            return_value=DELETE_RESPONSE
        )
        subnet_group.delete(ctx=_ctx, resource_config=None, iface=None)

        self.fake_client.delete_db_subnet_group.assert_called_with(
            DBSubnetGroupName='zzzzzz-subnet-group'
        )

        self.assertEqual(
            _ctx.instance.runtime_properties, {
                '__deleted': True,
            }
        )

    def _create_subnet_relationships(self, node_id):
        _source_ctx = self.get_mock_ctx(
            'test_assoc_source',
            test_properties=NODE_PROPERTIES,
            test_runtime_properties=RUNTIME_PROPERTIES,
            type_hierarchy=SUBNET_GROUP_TH
        )

        _target_ctx = self.get_mock_ctx(
            'test_assoc_target',
            test_properties={},
            test_runtime_properties={
                'resource_id': 'prepare_assoc_resource',
                'aws_resource_id': 'aws_resource_mock_id',
                '_set_changed': True
            },
            type_hierarchy=['cloudify.nodes.Root',
                            'cloudify.aws.nodes.Subnet']
        )

        _ctx = self.get_mock_relationship_ctx(
            node_id,
            test_properties={},
            test_runtime_properties={},
            test_source=_source_ctx,
            test_target=_target_ctx,
            type_hierarchy=['cloudify.nodes.Root']
        )

        return _source_ctx, _target_ctx, _ctx

    def test_prepare_assoc(self):
        _source_ctx, _target_ctx, _ctx = self._create_subnet_relationships(
            'test_prepare_assoc'
        )
        current_ctx.set(_ctx)

        subnet_group.prepare_assoc(
            ctx=_ctx, resource_config=None, iface=None
        )
        self.assertEqual(_source_ctx.instance.runtime_properties, {
            'resource_config': {
                'SubnetIds': [
                    'subnet-xxxxxxxx',
                    'subnet-yyyyyyyy',
                    'aws_resource_mock_id'
                ],
                'DBSubnetGroupDescription': 'MySQL5.7 Subnet Group',
                'DBSubnetGroupName': 'zzzzzz-subnet-group'
            }
        })

    def test_detach_from(self):
        _source_ctx, _target_ctx, _ctx = self._create_subnet_relationships(
            'test_detach_from'
        )
        current_ctx.set(_ctx)

        subnet_group.detach_from(
            ctx=_ctx, resource_config=None, iface=None
        )
        self.assertEqual(_source_ctx.instance.runtime_properties, {
            'resource_config': {
                'SubnetIds': ['subnet-xxxxxxxx', 'subnet-yyyyyyyy'],
                'DBSubnetGroupDescription': 'MySQL5.7 Subnet Group',
                'DBSubnetGroupName': 'zzzzzz-subnet-group'
            }
        })


if __name__ == '__main__':
    unittest.main()
