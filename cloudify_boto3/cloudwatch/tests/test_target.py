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

import unittest
from mock import patch, MagicMock

from cloudify.state import current_ctx

from cloudify_boto3.common.tests.test_base import TestBase, CLIENT_CONFIG
from cloudify_boto3.common.tests.test_base import DELETE_RESPONSE
from cloudify_boto3.common.tests.test_base import DEFAULT_RUNTIME_PROPERTIES
from cloudify_boto3.cloudwatch.resources import target


# Constants
TARGET_TH = ['cloudify.nodes.Root',
             'cloudify.nodes.aws.cloudwatch.Target']

NODE_PROPERTIES = {
    'use_external_resource': False,
    'resource_config': {
        'kwargs': {
            'Targets': [{
                'Id': 'topic1',
                'Arn': 'topic1'
            }]
        }
    },
    'client_config': CLIENT_CONFIG
}


class TestCloudwatchTarget(TestBase):

    def test_prepare(self):
        self._prepare_check(
            type_hierarchy=TARGET_TH,
            type_name='cloudwatch',
            type_class=target
        )

    def _prepare_context(self):
        mock_rule = MagicMock()
        mock_rule.type_hierarchy = 'cloudify.relationships.depends_on'
        mock_rule.target.instance.runtime_properties = {
            'aws_resource_id': 'aws_id'
        }
        mock_rule.target.node.type_hierarchy = [
            'cloudify.nodes.Root',
            'cloudify.nodes.aws.cloudwatch.Rule'
        ]

        mock_rule.target.node.id = 'aws-rule-node'
        mock_rule.target.instance.relationships = []

        mock_topic = MagicMock()
        mock_topic.type_hierarchy = 'cloudify.relationships.depends_on'
        mock_topic.target.instance.runtime_properties = {
            'aws_resource_id': 'topic_id'
        }
        mock_topic.target.node.type_hierarchy = [
            'cloudify.nodes.Root',
            'cloudify.nodes.aws.SNS.Topic'
        ]

        mock_topic.target.node.id = 'topic1'
        mock_topic.target.instance.relationships = []

        _ctx = self.get_mock_ctx(
            'test_create',
            test_properties=NODE_PROPERTIES,
            test_runtime_properties=DEFAULT_RUNTIME_PROPERTIES,
            type_hierarchy=TARGET_TH,
            test_relationships=[mock_rule, mock_topic]
        )

        current_ctx.set(_ctx)
        return _ctx

    def test_create(self):
        _ctx = self._prepare_context()
        fake_boto, fake_client = self.fake_boto_client('events')

        with patch('boto3.client', fake_boto):
            fake_client.put_targets = MagicMock(return_value={})

            target.create(ctx=_ctx, resource_config=None, iface=None)

            fake_boto.assert_called_with('events', **CLIENT_CONFIG)

            fake_client.put_targets.assert_called_with(
                Rule='aws_id', Targets=[{'Id': 'topic1', 'Arn': 'topic1'}]
            )

            self.assertEqual(
                _ctx.instance.runtime_properties,
                DEFAULT_RUNTIME_PROPERTIES
            )

    def test_delete(self):
        _ctx = self._prepare_context()
        fake_boto, fake_client = self.fake_boto_client('events')

        with patch('boto3.client', fake_boto):
            fake_client.remove_targets = MagicMock(
                return_value=DELETE_RESPONSE
            )

            target.delete(ctx=_ctx, resource_config=None, iface=None)

            fake_boto.assert_called_with('events', **CLIENT_CONFIG)

            fake_client.remove_targets.assert_called_with(
                Ids=['topic1'], Rule='aws_id'
            )

            self.assertEqual(
                _ctx.instance.runtime_properties, DEFAULT_RUNTIME_PROPERTIES
            )

    def test_CloudwatchTarget_status(self):
        fake_boto, fake_client = self.fake_boto_client('events')
        with patch('boto3.client', fake_boto):

            test_instance = target.CloudwatchTarget("ctx_node",
                                                    resource_id='user_id',
                                                    client=fake_client,
                                                    logger=None)

            self.assertEqual(test_instance.status, None)

    def test_CloudwatchTarget_properties(self):
        fake_boto, fake_client = self.fake_boto_client('events')
        with patch('boto3.client', fake_boto):

            test_instance = target.CloudwatchTarget("ctx_node",
                                                    resource_id='user_id',
                                                    client=fake_client,
                                                    logger=None)

            self.assertEqual(test_instance.properties, None)


if __name__ == '__main__':
    unittest.main()
