#!/usr/bin/env python3
"""This module contains unit tests that tests for expected output given map and path"""

import unittest
from parameterized import parameterized
from utils import access_nested_map

class TestAccessNestedMap(unittest.TestCase):
    """Unit tests for utils.access_nested_map"""
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """tests for expected output given nested map and path"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),

    ])

    def test_access_nested_map_exception(self, nested_map, path):
        """tests for error given nested map and path"""
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)