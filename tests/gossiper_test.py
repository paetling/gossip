from unittest import TestCase
from mock import patch, call
from gossip.libs.gossiper import Gossiper

class TestGossiper(TestCase):
    def test_members_excluding_self1(self):
        server_configs ={
            'servers':
                [{'address': 'a', 'port': 'a'},
                 {'address': 'a', 'port': 'b'},
                 {'address': 'a', 'port': 'c'}]}
        my_config = {'address': 'a', 'port': 'b'}
        current_membership = {'server_configs': server_configs, 'my_config': my_config}
        gossiper = Gossiper(1)

        self.assertEquals(gossiper.members_excluding_self(current_membership), [0,2])

    def test_members_excluding_self2(self):
        server_configs ={
            'servers':
                [{'address': 'a', 'port': 'a'},
                 {'address': 'a', 'port': 'b'},
                 {'address': 'a', 'port': 'c'}]}
        my_config = {'address': 'a', 'port': 'a'}
        current_membership = {'server_configs': server_configs, 'my_config': my_config}
        gossiper = Gossiper(0)

        self.assertEquals(gossiper.members_excluding_self(current_membership), [1,2])

    def test_get_random_peer1(self):
        server_configs ={
            'servers':
                [{'address': 'a', 'port': 'a'},
                 {'address': 'b', 'port': 'b'},
                 {'address': 'c', 'port': 'c'}],
             'gossip_list': [0, 0, 0],
             'suspect_list': [0, 0, 0],
             'suspect_matrix': [[0, 0, 0],
                                [0, 0, 0],
                                [0, 0, 0]]}
        my_config = {'address': 'a', 'port': 'a'}
        current_membership = {'server_configs': server_configs, 'my_config': my_config}
        gossiper = Gossiper(0)

        address, port = gossiper.get_random_peer(current_membership)
        self.assertIn(address, ['b', 'c'])
        self.assertIn(port, ['b', 'c'])

    def test_get_random_peer2(self):
        server_configs ={
            'servers':
                [{'address': 'a', 'port': 'a'},
                 {'address': 'b', 'port': 'b'},
                 {'address': 'c', 'port': 'c'}],
             'gossip_list': [0, 0, 0],
             'suspect_list': [0, 0, 0],
             'suspect_matrix': [[0, 0, 0],
                                [0, 0, 0],
                                [0, 0, 0]]}
        my_config = {'address': 'b', 'port': 'b'}
        current_membership = {'server_configs': server_configs, 'my_config': my_config}
        gossiper = Gossiper(1)

        address, port = gossiper.get_random_peer(current_membership)
        self.assertIn(address, ['a', 'c'])
        self.assertIn(port, ['a', 'c'])

    @patch('gossip.libs.gossiper.save_membership')
    def test_update_heartbeat1(self, fake_save_membership):
        server_configs ={
             'gossip_list': [0, 0, 0]}
        my_config = {'address': 'b', 'port': 'b'}
        current_membership = {'server_configs': server_configs, 'my_config': my_config}
        expected_list = [0, 1, 1]
        gossiper = Gossiper(0)

        gossiper.config_file_name = "test_config"
        gossiper.update_heartbeat(current_membership)

        self.assertEquals(current_membership['server_configs']['gossip_list'], expected_list)
        fake_save_membership.assert_has_calls([call("test_config", current_membership)])

    @patch('gossip.libs.gossiper.save_membership')
    def test_update_heartbeat2(self, fake_save_membership):
        server_configs ={
             'gossip_list': [0, 0, 0]}
        my_config = {'address': 'b', 'port': 'b'}
        current_membership = {'server_configs': server_configs, 'my_config': my_config}
        expected_list = [1, 0, 1]
        gossiper = Gossiper(1)

        gossiper.config_file_name = "test_config"
        gossiper.update_heartbeat(current_membership)

        self.assertEquals(current_membership['server_configs']['gossip_list'], expected_list)
        fake_save_membership.assert_has_calls([call("test_config", current_membership)])

    @patch('gossip.libs.gossiper.save_membership')
    def test_update_heartbeat3(self, fake_save_membership):
        server_configs ={
             'gossip_list': [1, 2, 3]}
        my_config = {'address': 'b', 'port': 'b'}
        current_membership = {'server_configs': server_configs, 'my_config': my_config}
        expected_list = [0, 3, 4]
        gossiper = Gossiper(0)

        gossiper.config_file_name = "test_config"
        gossiper.update_heartbeat(current_membership)

        self.assertEquals(current_membership['server_configs']['gossip_list'], expected_list)
        fake_save_membership.assert_has_calls([call("test_config", current_membership)])




