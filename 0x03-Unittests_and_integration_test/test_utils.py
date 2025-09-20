#!/usr/bin/env python3
""" This module parameterizes a unit test"""

import unittest
import parameterized as parameterized
from utils import access_nested_map

class TestAccessNestedMap(unittest.TestCase):
    """" """
    
    @parameterized.expand([
    ({"a": 1}, ("a",), 1),
    ({"a": {"b": 2}}, ("a",), {"b": 2} ),
    ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    
    def test_access_nested_map(self,nested_map, path, expected):
        """ tests that the method returns an expected value    """
        self.assertEqual(access_nested_map(nested_map, path), expected)
