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
from __future__ import unicode_literals

import unittest

from mock import patch, MagicMock

from cloudify_awssdk.common.tests.test_base import TestBase, mock_decorator
from cloudify_awssdk.ec2.resources.vpc_peering import EC2VpcPeering
from cloudify_awssdk.ec2.resources import vpc_peering
from cloudify_awssdk.common import constants


class TestEC2VpcPeering(TestBase):

    def setUp(self):
        super(TestEC2VpcPeering, self).setUp()
        self.vpc_peering = EC2VpcPeering("ctx_node", resource_id=True,
                                         client=True, logger=None)
        mock1 = patch(
            'cloudify_awssdk.common.decorators.aws_resource', mock_decorator)

        mock1.start()
        reload(vpc_peering)

    def test_class_properties(self):
        effect = self.get_client_error_exception(
            name=vpc_peering.RESOURCE_TYPE)

        self.vpc_peering.client = \
            self.make_client_function('describe_vpc_peering_connections',
                                      side_effect=effect)
        self.assertIsNone(self.vpc_peering.properties)

        response = \
            {
                vpc_peering.VPC_PEERING_CONNECTIONS: [
                    {
                        'AccepterVpcInfo': {
                            'CidrBlock': 'cidr_block_test',
                            'Ipv6CidrBlockSet': [
                                {
                                    'Ipv6CidrBlock': 'ip_6_cidr_block_test'
                                },
                            ],
                            'CidrBlockSet': [
                                {
                                    'CidrBlock': 'cidr_block_test'
                                },
                            ],
                            'OwnerId': 'owner_id_test',
                            'VpcId': 'vpc_id_test',
                            'Region': 'region_test'
                        },
                        'RequesterVpcInfo': {
                            'CidrBlock': 'cidr_block_test',
                            'Ipv6CidrBlockSet': [
                                {
                                    'Ipv6CidrBlock': 'ip_6_cidr_block_test'
                                },
                            ],
                            'CidrBlockSet': [
                                {
                                    'CidrBlock': 'cidr_block_test'
                                },
                            ],
                            'OwnerId': 'owner_id_test',
                            'VpcId': 'vpc_id_test',
                            'Region': 'region_test'
                        },
                        'Status': {
                            'Code': 'test_status_code',
                            'Message': 'test_status_message'
                        },
                        'VpcPeeringConnectionId': 'test_peering_connection_id'
                    },
                ]
            }

        self.vpc_peering.describe_vpc_peering_filter = {
            vpc_peering.VPC_PEERING_CONNECTION_IDS:
                ['test_peering_connection_id']
        }
        self.vpc_peering.client = self.make_client_function(
            'describe_vpc_peering_connections', return_value=response)

        self.assertEqual(
            self.vpc_peering.properties[
                vpc_peering.VPC_PEERING_CONNECTION_ID],
            'test_peering_connection_id'
        )

    def test_class_status(self):
        response = \
            {
                vpc_peering.VPC_PEERING_CONNECTIONS: [
                    {
                        'AccepterVpcInfo': {
                            'CidrBlock': 'cidr_block_test',
                            'Ipv6CidrBlockSet': [
                                {
                                    'Ipv6CidrBlock': 'ip_6_cidr_block_test'
                                },
                            ],
                            'CidrBlockSet': [
                                {
                                    'CidrBlock': 'cidr_block_test'
                                },
                            ],
                            'OwnerId': 'owner_id_test',
                            'VpcId': 'vpc_id_test',
                            'Region': 'region_test'
                        },
                        'RequesterVpcInfo': {
                            'CidrBlock': 'cidr_block_test',
                            'Ipv6CidrBlockSet': [
                                {
                                    'Ipv6CidrBlock': 'ip_6_cidr_block_test'
                                },
                            ],
                            'CidrBlockSet': [
                                {
                                    'CidrBlock': 'cidr_block_test'
                                },
                            ],
                            'OwnerId': 'owner_id_test',
                            'VpcId': 'vpc_id_test',
                            'Region': 'region_test'
                        },
                        'Status': {
                            'Code': 'test_status_code',
                            'Message': 'test_status_message'
                        },
                        'VpcPeeringConnectionId': 'test_peering_connection_id'
                    },
                ]
            }

        self.vpc_peering.client = self.make_client_function(
            'describe_vpc_peering_connections', return_value=response)

        self.assertEqual(self.vpc_peering.status['Code'], 'test_status_code')

    def test_class_create(self):
        params = \
            {
                'DryRun': True,
                'PeerOwnerId': 'peer_owner_id_test',
                'PeerVpcId': 'test_peering_connection_id',
                'VpcId': 'vpc_id_test',
                'PeerRegion': 'peer_region_test'
            }

        response = \
            {
                vpc_peering.VPC_PEERING_CONNECTION: {
                    'AccepterVpcInfo': {
                        'CidrBlock': 'cidr_block_test',
                        'Ipv6CidrBlockSet': [
                            {
                                'Ipv6CidrBlock': 'ip_6_cidr_block_test'
                            },
                        ],
                        'CidrBlockSet': [
                            {
                                'CidrBlock': 'cidr_block_test'
                            },
                        ],
                        'OwnerId': 'owner_id_test',
                        'VpcId': 'vpc_id_test',
                        'Region': 'region_test'
                    },
                    'RequesterVpcInfo': {
                        'CidrBlock': 'cidr_block_test',
                        'Ipv6CidrBlockSet': [
                            {
                                'Ipv6CidrBlock': 'ip_6_cidr_block_test'
                            },
                        ],
                        'CidrBlockSet': [
                            {
                                'CidrBlock': 'cidr_block_test'
                            },
                        ],
                        'OwnerId': 'owner_id_test',
                        'VpcId': 'vpc_id_test',
                        'Region': 'region_test'
                    },
                    'Status': {
                        'Code': 'test_status_code',
                        'Message': 'test_status_message'
                    },
                    'VpcPeeringConnectionId': 'test_peering_connection_id'
                },
            }

        self.vpc_peering.client = self.make_client_function(
            'create_vpc_peering_connection', return_value=response)

        self.assertEqual(self.vpc_peering.create(params),
                         response.get(vpc_peering.VPC_PEERING_CONNECTION))

    def test_class_delete(self):
        params = \
            {
                'DryRun': True,
                'VpcPeeringConnectionId': 'test_peering_connection_id',
            }

        response = {'Return': True, }
        self.vpc_peering.client = self.make_client_function(
            'delete_vpc_peering_connection', return_value=response)
        self.assertEqual(self.vpc_peering.delete(params), response)

    def test_class_accept(self):
        params = \
            {
                'DryRun': True,
                'VpcPeeringConnectionId': 'test_peering_connection_id',
            }

        response = {'Return': True, }
        self.vpc_peering.client = self.make_client_function(
            'accept_vpc_peering_connection', return_value=response)
        self.assertEqual(self.vpc_peering.accept(params), response)

    def test_class_reject(self):
        params = \
            {
                'DryRun': True,
                'VpcPeeringConnectionId': 'test_peering_connection_id',
            }

        response = {'Return': True, }
        self.vpc_peering.client = self.make_client_function(
            'reject_vpc_peering_connection', return_value=response)
        self.assertEqual(self.vpc_peering.reject(params), response)

    def test_class_update(self):
        params = {
            vpc_peering.ACCEPTER_VPC_PEERING_CONNECTION: {
                'AllowDnsResolutionFromRemoteVpc': True,
                'AllowEgressFromLocalClassicLinkToRemoteVpc': False,
                'AllowEgressFromLocalVpcToRemoteClassicLink': False,
            },
            vpc_peering.REQUESTER_VPC_PEERING_CONNECTION: {
                'AllowDnsResolutionFromRemoteVpc': True,
                'AllowEgressFromLocalClassicLinkToRemoteVpc': False,
                'AllowEgressFromLocalVpcToRemoteClassicLink': False,
            },

            vpc_peering.VPC_PEERING_CONNECTION_ID:
                'test_peering_connection_id',

        }

        response = \
            {
                vpc_peering.ACCEPTER_VPC_PEERING_CONNECTION: {
                    'AllowDnsResolutionFromRemoteVpc': True,
                    'AllowEgressFromLocalClassicLinkToRemoteVpc': False,
                    'AllowEgressFromLocalVpcToRemoteClassicLink': False
                },
                vpc_peering.REQUESTER_VPC_PEERING_CONNECTION: {
                    'AllowDnsResolutionFromRemoteVpc': True,
                    'AllowEgressFromLocalClassicLinkToRemoteVpc': False,
                    'AllowEgressFromLocalVpcToRemoteClassicLink': False
                }
            }

        self.vpc_peering.client = self.make_client_function(
            'modify_vpc_peering_connection_options', return_value=response)
        self.assertEqual(self.vpc_peering.update(params), response)

    def test_prepare(self):
        ctx = self.get_mock_ctx("EC2VpcPeering")
        vpc_peering.prepare(ctx, 'config')
        self.assertEqual(
            ctx.instance.runtime_properties['resource_config'],
            'config')

    def test_create(self):
        iface = MagicMock()
        ctx = self.get_mock_ctx("EC2VpcPeering")
        config = \
            {
                'DryRun': True,
                'PeerVpcId': 'peer_vpc_id_test',
                'VpcId': 'vpc_id_test',
                'PeerRegion': 'peer_region_test'
            }

        response = \
            {
                vpc_peering.VPC_PEERING_CONNECTION: {
                    'AccepterVpcInfo': {
                        'CidrBlock': 'cidr_block_test',
                        'Ipv6CidrBlockSet': [
                            {
                                'Ipv6CidrBlock': 'ip_6_cidr_block_test'
                            },
                        ],
                        'CidrBlockSet': [
                            {
                                'CidrBlock': 'cidr_block_test'
                            },
                        ],
                        'OwnerId': 'owner_id_test',
                        'VpcId': 'vpc_id_test',
                        'Region': 'region_test'
                    },
                    'RequesterVpcInfo': {
                        'CidrBlock': 'cidr_block_test',
                        'Ipv6CidrBlockSet': [
                            {
                                'Ipv6CidrBlock': 'ip_6_cidr_block_test'
                            },
                        ],
                        'CidrBlockSet': [
                            {
                                'CidrBlock': 'cidr_block_test'
                            },
                        ],
                        'OwnerId': 'owner_id_test',
                        'VpcId': 'vpc_id_test',
                        'Region': 'region_test'
                    },
                    'Status': {
                        'Code': 'test_status_code',
                        'Message': 'test_status_message'
                    },
                    'VpcPeeringConnectionId': 'test_peering_connection_id'
                },
            }

        ctx.instance.runtime_properties['resource_config'] = config
        iface.create = self.mock_return(
            response.get(vpc_peering.VPC_PEERING_CONNECTION))
        vpc_peering.create(ctx, iface, config)
        self.assertEqual(
            ctx.instance.runtime_properties[constants.EXTERNAL_RESOURCE_ID],
            'test_peering_connection_id'
        )

    def test_modify(self):
        iface = MagicMock()
        ctx = self.get_mock_ctx("EC2VpcPeering")
        config = {
            vpc_peering.ACCEPTER_VPC_PEERING_CONNECTION: {
                'AllowDnsResolutionFromRemoteVpc': True,
                'AllowEgressFromLocalClassicLinkToRemoteVpc': False,
                'AllowEgressFromLocalVpcToRemoteClassicLink': False,
            },
            vpc_peering.REQUESTER_VPC_PEERING_CONNECTION: {
                'AllowDnsResolutionFromRemoteVpc': True,
                'AllowEgressFromLocalClassicLinkToRemoteVpc': False,
                'AllowEgressFromLocalVpcToRemoteClassicLink': False,
            },
        }

        ctx.instance.runtime_properties[constants.EXTERNAL_RESOURCE_ID] =\
            'test_peering_connection_id'

        response = \
            {
                vpc_peering.ACCEPTER_VPC_PEERING_CONNECTION: {
                    'AllowDnsResolutionFromRemoteVpc': True,
                    'AllowEgressFromLocalClassicLinkToRemoteVpc': False,
                    'AllowEgressFromLocalVpcToRemoteClassicLink': False
                },
                vpc_peering.REQUESTER_VPC_PEERING_CONNECTION: {
                    'AllowDnsResolutionFromRemoteVpc': True,
                    'AllowEgressFromLocalClassicLinkToRemoteVpc': False,
                    'AllowEgressFromLocalVpcToRemoteClassicLink': False
                }
            }

        iface.update = self.mock_return(response)
        vpc_peering.modify(ctx, iface, config)
        self.assertTrue(iface.update.called)

    def test_delete(self):
        iface = MagicMock()
        ctx = self.get_mock_ctx("EC2VpcPeering")
        ctx.instance.runtime_properties[constants.EXTERNAL_RESOURCE_ID]\
            = 'test_peering_connection_id'
        vpc_peering.delete(ctx, iface, {})
        self.assertTrue(iface.delete.called)

    def test_accept(self):
        iface = MagicMock()
        ctx = self.get_mock_ctx("EC2VpcPeering")
        config = \
            {
                'DryRun': True,
                'VpcPeeringConnectionId': 'test_peering_connection_id',
            }

        response = {'Return': True, }
        iface.accept = self.mock_return(response)
        vpc_peering.accept(ctx, iface, config)
        self.assertEqual(
            ctx.instance.runtime_properties[constants.EXTERNAL_RESOURCE_ID],
            'test_peering_connection_id'
        )

    def test_reject(self):
        iface = MagicMock()
        ctx = self.get_mock_ctx("EC2VpcPeering")
        config = \
            {
                'DryRun': True,
                'VpcPeeringConnectionId': 'test_peering_connection_id',
            }

        response = {'Return': True, }
        iface.reject = self.mock_return(response)
        vpc_peering.reject(ctx, iface, config)
        self.assertEqual(
            ctx.instance.runtime_properties[constants.EXTERNAL_RESOURCE_ID],
            'test_peering_connection_id'
        )


if __name__ == '__main__':
    unittest.main()