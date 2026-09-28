import unittest
from recursive_json_search import *
from test_data import *


class json_search_test(unittest.TestCase):
    '''test module to test search function in recursive_json_search.py'''

    def test_search_found(self):
        '''key should be found, return list should not be empty'''
        self.assertTrue([] != json_search(key1, data, role="viewer"))

    def test_search_not_found(self):
        '''key should not be found, should return an empty list'''
        self.assertTrue([] == json_search(key2, data, role="viewer"))

    def test_is_a_list(self):
        '''Should return a list'''
        self.assertIsInstance(json_search(key1, data, role="viewer"), list)

    def test_viewer_cannot_read_api_key(self):
       '''viewer khong co quyen doc  apiKey'''
       result = json_search("apiKey", data, role="viewer")
       self.assertEqual([], result)

    def test_authorized_role_can_read_secret(self):
       """Role hop le duoc cap quyen doc nhay cam"""
       result = json_search("apiKey", data, role="admin")
       self.assertTrue([] != result)

    def test_invalid_role_cannot_read_secret(self):
       """Role khong hop le khong duoc doc"""
       result = json_search("apiKey", data, role="invalid_role")
       self.assertEqual([], result)

if __name__ == '__main__':
    unittest.main()
