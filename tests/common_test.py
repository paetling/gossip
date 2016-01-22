import os
from unittest import TestCase
from mock import Mock
from gossip.libs.common import get_config_file_name, load_membership, save_membership
from gossip.libs import common

class TestCommon(TestCase):
    def test_get_config_file_name(self):
        common.BASE_CONFIG_FILE = 'base_config_file'
        self.assertEquals(get_config_file_name(0), 'base_config_file_0')
        self.assertEquals(get_config_file_name(10), 'base_config_file_10')
        self.assertEquals(get_config_file_name(100), 'base_config_file_100')

    def test_load_membership(self):
        self.assertEquals(load_membership(os.path.join(os.path.dirname(__file__),
                                                       'example_test_files/file1.yml')),
                                          {'key1': ['these', 'are', 'values'],
                                           'key2': [{'key3': 'value1'}, 'value2']})

        self.assertEquals(load_membership(os.path.join(os.path.dirname(__file__),
                                                       'example_test_files/file2.yml')),
                                          {'key1': 'value1',
                                           'key2': 'value2',
                                           'key3': {'key4': 'value3',
                                                    'key5': 'value4'}})

    def test_save_membership1(self):
        blank_file_name = os.path.join(os.path.dirname(__file__), 'example_test_files/blank.yml')
        save_doc = {}
        save_membership(blank_file_name, save_doc)
        self.assertEquals(load_membership(blank_file_name), save_doc)

        open(blank_file_name, 'w').close()

    def test_save_membership2(self):
        blank_file_name = os.path.join(os.path.dirname(__file__), 'example_test_files/blank.yml')
        save_doc = {'key1': 'value1', 'key2': ['value2', 'value3'], 'key3': {'key4': 'value4'}}
        save_membership(blank_file_name, save_doc)
        self.assertEquals(load_membership(blank_file_name), save_doc)

        open(blank_file_name, 'w').close()


