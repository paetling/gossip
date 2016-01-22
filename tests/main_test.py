from unittest import TestCase
from mock import patch, call, Mock

from gossip.main import initial_membership_dict

class TestMain(TestCase):
    def test_initial_membership_dict1(self):
        expected_dict = {
            'server_configs':{
                'servers': [{'address': 'localhost', 'port': 80},
                            {'address': 'localhost', 'port': 81},
                            {'address': 'localhost', 'port': 82}],
                'gossip_list': [0, 0, 0],
                'suspect_list': [0, 0, 0],
                'suspect_matrix': [[0, 0, 0],
                                   [0, 0, 0],
                                   [0, 0, 0]]
            }
        }
        self.assertEquals(expected_dict, initial_membership_dict(3))

    def test_initial_membership_dict2(self):
        expected_dict = {
            'server_configs':{
                'servers': [{'address': 'localhost', 'port': 80},
                            {'address': 'localhost', 'port': 81},
                            {'address': 'localhost', 'port': 82},
                            {'address': 'localhost', 'port': 83},
                            {'address': 'localhost', 'port': 84}],
                'gossip_list': [0, 0, 0, 0, 0],
                'suspect_list': [0, 0, 0, 0, 0],
                'suspect_matrix': [[0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0]]
            }
        }
        self.assertEquals(expected_dict, initial_membership_dict(5))

    def test_initial_membership_dict3(self):
        expected_dict = {
            'server_configs':{
                'servers': [{'address': 'localhost', 'port': 80}],
                'gossip_list': [0],
                'suspect_list': [0],
                'suspect_matrix': [[0]]
            }
        }
        self.assertEquals(expected_dict, initial_membership_dict(1))
