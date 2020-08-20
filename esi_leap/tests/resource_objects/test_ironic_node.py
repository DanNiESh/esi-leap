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
from esi_leap.resource_objects import ironic_node
from esi_leap.tests import base
import json
import mock

start = datetime.datetime(2016, 7, 16, 19, 20, 30)

class FakeIronicNode(object):
    def __init__(self):  
        self.created_at = start
        self.lessee = "abcdef"
        self.owner = "123456"
        self.properties = {"contract_uuid":"001"}
        self.provision_state = "available"
        self.uuid = "1111"

class FakeContract(object):
    def __init__(self):
        self.uuid = '001'
        self.project_id = '654321'
        self.start_time = start + datetime.timedelta(days=5)
        self.end_time = start + datetime.timedelta(days=10)
        self.status = statuses.ACTIVE
        self.offer_uuid = '534653c9-880d-4c2d-6d6d-f4f2a09e384'

class TestIronicNode(base.TestCase):

    def setUp(self):
        super(TestIronicNode, self).setUp()
        self.fake_contract = FakeContract()
        self.fake_admin_project_id_1 = '123'
        self.fake_admin_project_id_2 = '123456'

    @mock.patch.object(ironic_node, 'get_ironic_client', autospec=True)
    def test_get_contract_uuid(self, client_mock):
        fake_get_node = FakeIronicNode()
        client_mock.return_value.node.get.return_value = fake_get_node
        test_ironic_node = ironic_node.IronicNode("1111")
        contract_uuid = test_ironic_node.get_contract_uuid()
        expected_contract_uuid = fake_get_node.properties.get("contract_uuid")
        self.assertEqual(contract_uuid, expected_contract_uuid)
        client_mock.assert_called_once()
        client_mock.return_value.node.get.assert_called_once_with(test_ironic_node._uuid)

    

    @mock.patch.object(ironic_node, 'get_ironic_client', autospec=True)
    def test_get_project_id(self, client_mock):
        fake_get_node = FakeIronicNode()
        client_mock.return_value.node.get.return_value = fake_get_node
        test_ironic_node = ironic_node.IronicNode("1111")
        project_id = test_ironic_node.get_project_id()
        expected_project_id = fake_get_node.lessee
        self.assertEqual(project_id, expected_project_id)
        client_mock.assert_called_once()
        client_mock.return_value.node.get.assert_called_once_with(test_ironic_node._uuid)


    @mock.patch.object(ironic_node, 'get_ironic_client', autospec=True)
    def test_get_node_config(self, client_mock):
        fake_get_node = FakeIronicNode()
        client_mock.return_value.node.get.return_value = fake_get_node
        test_ironic_node = ironic_node.IronicNode("1111")
        config = test_ironic_node.get_node_config()
        expected_config = fake_get_node.properties
        expected_config.pop('contract_uuid', None)
        self.assertEqual(config, expected_config)
        client_mock.assert_called_once()
        client_mock.return_value.node.get.assert_called_once_with(test_ironic_node._uuid)
    
    @mock.patch.object(ironic_node, 'get_ironic_client', autospec=True)
    def test_set_contract(self, client_mock):
        test_ironic_node = ironic_node.IronicNode("1111")
        test_ironic_node.set_contract(self.fake_contract)
        client_mock.assert_called_once()
        client_mock.return_value.node.update.assert_called_once()
    
    @mock.patch.object(ironic_node, 'get_ironic_client', autospec=True)
    def test_expire_contract(self, client_mock):
        client_mock.return_value.node.get.return_value.provision_state = "active"
        with mock.patch.object(
            ironic_node.IronicNode, 'get_contract_uuid', autospec=True
        ) as mock_contract_uuid_true:
            mock_contract_uuid_true.return_value = self.fake_contract.uuid
            with mock.patch.object(
                ironic_node.IronicNode, 'get_project_id', autospec=True
            ) as mock_project_id_get:
                mock_project_id_get.return_value = self.fake_contract.project_id

                test_ironic_node = ironic_node.IronicNode("1111")
                test_ironic_node.expire_contract(self.fake_contract)

                mock_project_id_get.assert_called_once()
                self.assertEqual(mock_contract_uuid_true.call_count, 2)
                self.assertEqual(client_mock.call_count, 3)
                client_mock.return_value.node.update.assert_called_once()
                client_mock.return_value.node.get.assert_called_once_with(test_ironic_node._uuid)
                client_mock.return_value.node.set_provision_state.assert_called_once_with(test_ironic_node._uuid, "deleted")

        with mock.patch.object(
            ironic_node.IronicNode, 'get_contract_uuid', autospec=True
        ) as mock_contract_uuid_false:
            mock_contract_uuid_false.return_value = "none"
            test_ironic_node = ironic_node.IronicNode("1111")
            test_ironic_node.expire_contract(self.fake_contract)
            mock_contract_uuid_false.assert_called_once()

    @mock.patch.object(ironic_node, 'get_ironic_client', autospec=True)
    def test_is_resource_admin(self, client_mock):
        fake_get_node = FakeIronicNode()
        client_mock.return_value.node.get.return_value = fake_get_node
        test_ironic_node = ironic_node.IronicNode("1111")
        res1 = test_ironic_node.is_resource_admin(self.fake_admin_project_id_1)
        res2 = test_ironic_node.is_resource_admin(self.fake_admin_project_id_2)
        self.assertEqual(res1, False)
        self.assertEqual(res2, True)


            