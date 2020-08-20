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
import datetime
from esi_leap.common import statuses
from esi_leap.objects import contract
from esi_leap.resource_objects import dummy_node
from esi_leap.tests import base
import json
import mock


start = datetime.datetime(2016, 7, 16, 19, 20, 30)


def get_test_dummy_node_1():
    return {
        "project_owner_id": "123456",
        "project_id": "654321",
        "contract_uuid": "001",
        "server_config": {
            "new attribute XYZ": "new attribute XYZ",
            "cpu_type": "Intel Xeon",
            "cores": 16,
            "ram_gb": 512,
            "storage_type": "samsung SSD",
            "storage_size_gb": 204
        }
    }


def get_test_dummy_node_2():
    return {
        "project_owner_id": "123456",
        "server_config": {
            "new attribute XYZ": "new attribute XYZ",
            "cpu_type": "Intel Xeon",
            "cores": 16,
            "ram_gb": 512,
            "storage_type": "samsung SSD",
            "storage_size_gb": 204
        }
    }


class FakeContract(object):
    def __init__(self):
        self.uuid = '001'
        self.project_id = '654321'
        self.start_time = start + datetime.timedelta(days=5)
        self.end_time = start + datetime.timedelta(days=10)
        self.status = statuses.CREATED
        self.offer_uuid = '534653c9-880d-4c2d-6d6d-f4f2a09e384'


class TestDummyNode(base.TestCase):

    def setUp(self):
        super(TestDummyNode, self).setUp()
        self.fake_dummy_node = dummy_node.DummyNode('1111')
        self.fake_contract = FakeContract()
        self.fake_admin_project_id_1 = '123'
        self.fake_admin_project_id_2 = '123456'
        self.fake_read_data_1 = json.dumps(get_test_dummy_node_1())
        self.fake_read_data_2 = json.dumps(get_test_dummy_node_2())


    def test_get_contract_uuid(self):
        mock_open = mock.mock_open(read_data=self.fake_read_data_1)
        with mock.patch('builtins.open', mock_open) as mock_file_open:
            contract_uuid = self.fake_dummy_node.get_contract_uuid()
            self.assertEqual(contract_uuid, '001')
            mock_file_open.assert_called_once()

    def test_get_project_id(self):
        mock_open = mock.mock_open(read_data=self.fake_read_data_1)
        with mock.patch('builtins.open', mock_open) as mock_file_open:
            project_id = self.fake_dummy_node.get_project_id()
            self.assertEqual(project_id, '654321')
            mock_file_open.assert_called_once()

    def test_get_node_config(self):
        mock_open = mock.mock_open(read_data=self.fake_read_data_1)
        with mock.patch('builtins.open', mock_open) as mock_file_open:
            config = self.fake_dummy_node.get_node_config()
            self.assertEqual(config, get_test_dummy_node_1()['server_config'])
            mock_file_open.assert_called_once()

    def test_set_contract(self):
        mock_open = mock.mock_open(read_data=self.fake_read_data_2)
        with mock.patch('builtins.open', mock_open) as mock_file_open:
            self.fake_dummy_node.set_contract(self.fake_contract)
            self.assertEqual(mock_file_open.call_count, 2)

    def test_expire_contract(self):
        mock_open = mock.mock_open(read_data=self.fake_read_data_1)
        with mock.patch('builtins.open', mock_open) as mock_file_open:
            self.fake_dummy_node.expire_contract(self.fake_contract)
            self.assertEqual(mock_file_open.call_count, 2)

    def test_is_resource_admin(self):
        mock_open = mock.mock_open(read_data=self.fake_read_data_1)
        with mock.patch('builtins.open', mock_open) as mock_file_open:
            res1 = self.fake_dummy_node.is_resource_admin(
                self.fake_admin_project_id_1)
            res2 = self.fake_dummy_node.is_resource_admin(
                self.fake_admin_project_id_2)
            self.assertEqual(res1, False)
            self.assertEqual(res2, True)
            self.assertEqual(mock_file_open.call_count, 2)
