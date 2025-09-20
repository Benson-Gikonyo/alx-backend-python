#!/usr/bin/env python3
"""This module contains unit tests """

import unittest
from parameterized import parameterized
from utils import access_nested_map
from utils import get_json
from unittest.mock import patch, Mock

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
            
            

class TestGetJson(unittest.TestCase):
    """unit tests for utils.get_json"""
    
    @parameterized.expand ([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    
    @patch("utils.request.get")
    
    def test_get_json(self, test_url, test_payload, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response
        
        result = get_json(test_url)
        
        self.assertEqual(result, test_payload)
        mock_get.assert_called_once_with(test_url)
