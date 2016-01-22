from unittest import TestCase
from mock import patch, call, Mock

from gossip.libs.listening_server import ListeningServer
from gossip.libs import listening_server

class TestListeningServer(TestCase):
    def setUp(self):
        self.server = ListeningServer(0, {'address': 'a', 'port': 'a'})

    def test_merge_gossip_list1(self):
        gossip_list_1 = [0, 0, 0, 0]
        gossip_list_2 = [1, 1, 1, 1]
        merged_list = [0, 0, 0, 0]

        self.assertEquals(merged_list, self.server.merge_gossip_list(gossip_list_1, gossip_list_2))

    def test_merge_gossip_list2(self):
        gossip_list_1 = [1, 1, 1, 1]
        gossip_list_2 = [0, 0, 0, 0]
        merged_list = [0, 0, 0, 0]

        self.assertEquals(merged_list, self.server.merge_gossip_list(gossip_list_1, gossip_list_2))

    def test_merge_gossip_list3(self):
        gossip_list_1 = [1, 2, 3, 4]
        gossip_list_2 = [4, 3, 2, 1]
        merged_list = [1, 2, 2, 1]

        self.assertEquals(merged_list, self.server.merge_gossip_list(gossip_list_1, gossip_list_2))

    def test_suspects_from_gossip1(self):
        gossip_list = [0, 0, 0, 0]
        listening_server.THRESHOLD = 3
        expected_suspects = [0, 0, 0, 0]

        self.assertEquals(expected_suspects, self.server.suspects_from_gossip(gossip_list))

    def test_suspects_from_gossip2(self):
        gossip_list = [0, 2, 4, 6]
        listening_server.THRESHOLD = 3
        expected_suspects = [0, 0, 1, 1]

        self.assertEquals(expected_suspects, self.server.suspects_from_gossip(gossip_list))

    def test_suspects_from_gossip3(self):
        gossip_list = [0, 2, 4, 6]
        listening_server.THRESHOLD = 5
        expected_suspects = [0, 0, 0, 1]

        self.assertEquals(expected_suspects, self.server.suspects_from_gossip(gossip_list))

    def test_create_suspect_matrix1(self):
        gossip_list_1 = [0, 0, 0, 0]
        gossip_list_2 = [1, 1, 1, 1]
        suspect_list = [5, 5, 5, 5]
        suspect_matrix_1 = [[1, 1, 1, 1],
                            [2, 2, 2, 2],
                            [3, 3, 3, 3],
                            [4, 4, 4, 4]]
        suspect_matrix_2 = [[10, 10, 10, 10],
                            [20, 20, 20, 20],
                            [30, 30, 30, 30],
                            [40, 40, 40, 40]]
        expected_matrix = [[5, 5, 5, 5],
                           [2, 2, 2, 2],
                           [3, 3, 3, 3],
                           [4, 4, 4, 4]]

        self.assertEquals(expected_matrix, self.server.create_suspect_matrix(gossip_list_1,
                                                                             gossip_list_2,
                                                                             suspect_list,
                                                                             suspect_matrix_1,
                                                                             suspect_matrix_2))

    def test_create_suspect_matrix2(self):
        self.server = ListeningServer(3, {'address': 'a', 'port': 'a'})
        gossip_list_1 = [0, 0, 0, 0]
        gossip_list_2 = [1, 1, 1, 1]
        suspect_list = [5, 5, 5, 5]
        suspect_matrix_1 = [[1, 1, 1, 1],
                            [2, 2, 2, 2],
                            [3, 3, 3, 3],
                            [4, 4, 4, 4]]
        suspect_matrix_2 = [[10, 10, 10, 10],
                            [20, 20, 20, 20],
                            [30, 30, 30, 30],
                            [40, 40, 40, 40]]
        expected_matrix = [[1, 1, 1, 1],
                           [2, 2, 2, 2],
                           [3, 3, 3, 3],
                           [5, 5, 5, 5]]

        self.assertEquals(expected_matrix, self.server.create_suspect_matrix(gossip_list_1,
                                                                             gossip_list_2,
                                                                             suspect_list,
                                                                             suspect_matrix_1,
                                                                             suspect_matrix_2))

    def test_create_suspect_matrix3(self):
        gossip_list_1 = [0, 1, 0, 1]
        gossip_list_2 = [1, 0, 1, 0]
        suspect_list = [5, 5, 5, 5]
        suspect_matrix_1 = [[1, 1, 1, 1],
                            [2, 2, 2, 2],
                            [3, 3, 3, 3],
                            [4, 4, 4, 4]]
        suspect_matrix_2 = [[10, 10, 10, 10],
                            [20, 20, 20, 20],
                            [30, 30, 30, 30],
                            [40, 40, 40, 40]]
        expected_matrix = [[5, 5, 5, 5],
                           [20, 20, 20, 20],
                           [3, 3, 3, 3],
                           [40, 40, 40, 40]]

        self.assertEquals(expected_matrix, self.server.create_suspect_matrix(gossip_list_1,
                                                                             gossip_list_2,
                                                                             suspect_list,
                                                                             suspect_matrix_1,
                                                                             suspect_matrix_2))

    def test_merge_membership_dicts1(self):
        current_membership_dict = {'server_configs':{
            'servers': [{'address': 'a', 'port': 'a'},
                        {'address': 'b', 'port': 'b'},
                        {'address': 'c', 'port': 'c'}],
            'gossip_list': [0, 0, 0],
            'suspect_list': [0, 0, 0],
            'suspect_matrix': [[0, 0, 0],
                               [0, 0, 0],
                               [0, 0, 0]]
            }
        }
        new_membership_dict = {'server_configs':{
            'servers': [{'address': 'a', 'port': 'a'},
                        {'address': 'b', 'port': 'b'},
                        {'address': 'c', 'port': 'c'}],
            'gossip_list': [10, 10, 10],
            'suspect_list': [10, 10, 10],
            'suspect_matrix': [[10, 10, 10],
                               [10, 10, 10],
                               [10, 10, 10]]
            }
        }
        merged_membership_dict = {'server_configs':{
            'servers': [{'address': 'a', 'port': 'a'},
                        {'address': 'b', 'port': 'b'},
                        {'address': 'c', 'port': 'c'}],
            'gossip_list': [0, 0, 0],
            'suspect_list': [0, 0, 0],
            'suspect_matrix': [[0, 0, 0],
                               [0, 0, 0],
                               [0, 0, 0]]
            }
        }

        self.assertEquals(merged_membership_dict,
                          self.server.merge_membership_dicts(current_membership_dict, new_membership_dict))

    def test_merge_membership_dicts2(self):
        listening_server.THRESHOLD = 7
        current_membership_dict = {'server_configs':{
            'servers': [{'address': 'a', 'port': 'a'},
                        {'address': 'b', 'port': 'b'},
                        {'address': 'c', 'port': 'c'}],
            'gossip_list': [0, 5, 10],
            'suspect_list': [0, 0, 1],
            'suspect_matrix': [[0, 0, 1],
                               [0, 0, 0],
                               [0, 0, 0]]
            }
        }
        new_membership_dict = {'server_configs':{
            'servers': [{'address': 'a', 'port': 'a'},
                        {'address': 'b', 'port': 'b'},
                        {'address': 'c', 'port': 'c'}],
            'gossip_list': [10, 0, 20],
            'suspect_list': [1, 0, 1],
            'suspect_matrix': [[0, 0, 0],
                               [1, 0, 1],
                               [0, 0, 0]]
            }
        }
        merged_membership_dict = {'server_configs':{
            'servers': [{'address': 'a', 'port': 'a'},
                        {'address': 'b', 'port': 'b'},
                        {'address': 'c', 'port': 'c'}],
            'gossip_list': [0, 0, 10],
            'suspect_list': [0, 0, 1],
            'suspect_matrix': [[0, 0, 1],
                               [1, 0, 1],
                               [0, 0, 0]]
            }
        }

        self.assertEquals(merged_membership_dict,
                          self.server.merge_membership_dicts(current_membership_dict, new_membership_dict))

    def test_merge_membership_dicts3(self):
        listening_server.THRESHOLD = 20
        current_membership_dict = {'server_configs':{
            'servers': [{'address': 'a', 'port': 'a'},
                        {'address': 'b', 'port': 'b'},
                        {'address': 'c', 'port': 'c'}],
            'gossip_list': [0, 7, 23, 25],
            'suspect_list': [0, 0, 1, 1],
            'suspect_matrix': [[0, 0, 1, 1],
                               [0, 0, 0, 0],
                               [0, 0, 0, 0],
                               [0, 0, 0, 0]]
            }
        }
        new_membership_dict = {'server_configs':{
            'servers': [{'address': 'a', 'port': 'a'},
                        {'address': 'b', 'port': 'b'},
                        {'address': 'c', 'port': 'c'},
                        {'address': 'd', 'port': 'd'}],
            'gossip_list': [7, 0, 5, 23],
            'suspect_list': [0, 0, 0, 1],
            'suspect_matrix': [[0, 0, 0, 0],
                               [0, 0, 0, 1],
                               [0, 0, 0, 1],
                               [0, 0, 0, 0]]
            }
        }
        merged_membership_dict = {'server_configs':{
            'servers': [{'address': 'a', 'port': 'a'},
                        {'address': 'b', 'port': 'b'},
                        {'address': 'c', 'port': 'c'}],
            'gossip_list': [0, 0, 5, 23],
            'suspect_list': [0, 0, 0, 1],
            'suspect_matrix': [[0, 0, 0, 1],
                               [0, 0, 0, 1],
                               [0, 0, 0, 1],
                               [0, 0, 0, 0]]
            }
        }

        self.assertEquals(merged_membership_dict,
                          self.server.merge_membership_dicts(current_membership_dict, new_membership_dict))
