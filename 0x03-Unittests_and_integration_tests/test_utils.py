#!/usr/bin/env python3
"""This module contains unit tests"""

import unittest
from parameterized import parameterized
from utils import access_nested_map
from utils import get_json
from unittest.mock import patch, Mock
from utils import memoize


class TestAccessNestedMap(unittest.TestCase):
    """Unit tests for utils.access_nested_map"""

    @parameterized.expand(
        [
            ({"a": 1}, ("a",), 1),
            ({"a": {"b": 2}}, ("a",), {"b": 2}),
            ({"a": {"b": 2}}, ("a", "b"), 2),
        ]
    )
    def test_access_nested_map(self, nested_map, path, expected):
        """tests for expected output given nested map and path"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand(
        [
            ({}, ("a",)),
            ({"a": 1}, ("a", "b")),
        ]
    )
    def test_access_nested_map_exception(self, nested_map, path):
        """tests for error given nested map and path"""
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """unit tests for utils.get_json"""

    @parameterized.expand(
        [
            ("http://example.com", {"payload": True}),
            ("http://holberton.io", {"payload": False}),
        ]
    )
    @patch("utils.request.get")
    def test_get_json(self, test_url, test_payload, mock_get):
        """test get_json method"""
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        result = get_json(test_url)

        self.assertEqual(result, test_payload)
        mock_get.assert_called_once_with(test_url)


class TestClass:
    """has a_method which returns 42"""

    def a_method(self):
        """returns 42"""
        return 42

    @memoize
    def a_property(self):
        """memoizes a_method"""
        return self.a_method()


class TestMemoize(unittest.TestCase):
    """Unit tests for utils.memoize"""

    def test_memoize(self):
        """test utils.memoize"""
        with patch.object(TestClass, "a_method", return_value=42) as mock_method:
            obj = TestClass()
            result1 = obj.a_property
            result2 = obj.a_property

            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            mock_method.assert_called_once()
