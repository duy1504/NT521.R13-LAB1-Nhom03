"""Functional and security regression tests for recursive JSON search."""

from copy import deepcopy
import unittest

from policy import POLICY
from recursive_json_search import json_search
from test_data import data, key1, key2


class json_search_test(unittest.TestCase):
    def test_search_found(self):
        """An authorized search finds the nested issue summary."""
        self.assertEqual(
            json_search(key1, data, role="viewer"),
            [{key1: "Network Device 10.10.20.82 Is Unreachable From Controller"}],
        )

    def test_search_not_found(self):
        """Searching for an absent key returns an empty list."""
        self.assertEqual(json_search(key2, data, role="admin"), [])

    def test_is_a_list(self):
        """Both successful and unsuccessful searches return lists."""
        for key in (key1, key2):
            with self.subTest(key=key):
                self.assertIsInstance(json_search(key, data, role="admin"), list)

    def test_all_nested_matches(self):
        """Collect matches across siblings, nested lists, and matched values."""
        nested = {
            "target": {"target": "inner"},
            "left": [{"target": 0}, [{"target": False}, {"target": None}]],
            "right": {"target": "last"},
        }
        self.assertEqual(
            json_search("target", nested),
            [
                {"target": {"target": "inner"}},
                {"target": "inner"},
                {"target": 0},
                {"target": False},
                {"target": None},
                {"target": "last"},
            ],
        )

    def test_list_root_and_repeated_calls(self):
        """Root lists retain duplicate matches without sharing call results."""
        nested = [{"target": "same"}, [{"target": "same"}]]
        expected = [{"target": "same"}, {"target": "same"}]
        self.assertEqual(json_search("target", nested), expected)
        self.assertEqual(json_search("missing", nested), [])
        self.assertEqual(json_search("target", nested), expected)

    def test_empty_and_scalar_inputs(self):
        """Empty containers and scalar inputs have no searchable keys."""
        for value in ({}, [], None, "target", 42, False):
            with self.subTest(value=value):
                self.assertEqual(json_search("target", value), [])

    def test_admin_permissions(self):
        """Admin can read every protected field defined in POLICY."""
        expected = {
            "apiKey": "SNMP-COMMUNITY-STRING-7f3a9c",
            "managementIpAddress": "10.10.20.21",
            "issueSummary": "Network Device 10.10.20.82 Is Unreachable From Controller",
        }
        for key, value in expected.items():
            with self.subTest(key=key):
                self.assertEqual(json_search(key, data, role="admin"), [{key: value}])

    def test_operator_permissions(self):
        """Operator can read management IP and summary but cannot read API keys."""
        self.assertEqual(json_search("apiKey", data, role="operator"), [])
        self.assertEqual(
            json_search("managementIpAddress", data, role="operator"),
            [{"managementIpAddress": "10.10.20.21"}],
        )
        self.assertEqual(
            json_search(key1, data, role="operator"),
            [{key1: "Network Device 10.10.20.82 Is Unreachable From Controller"}],
        )

    def test_viewer_permissions(self):
        """Viewer can read summaries but neither API keys nor management IPs."""
        for key in ("apiKey", "managementIpAddress"):
            with self.subTest(key=key):
                self.assertEqual(json_search(key, data, role="viewer"), [])
        self.assertEqual(
            json_search(key1, data, role="viewer"),
            [{key1: "Network Device 10.10.20.82 Is Unreachable From Controller"}],
        )

    def test_invalid_and_missing_roles(self):
        """Missing, unknown, and malformed roles cannot read protected fields."""
        for key in POLICY:
            self.assertEqual(json_search(key, data), [])
            for role in (None, "guest", "ADMIN", "", ["admin"], {"role": "admin"}):
                with self.subTest(key=key, role=role):
                    self.assertEqual(json_search(key, data, role=role), [])

    def test_nested_policy_permissions(self):
        """Each policy permission applies to every occurrence in nested data."""
        for key, allowed_roles in POLICY.items():
            nested = [{key: "first"}, [{"child": {key: "second"}}]]
            for role in ("admin", "operator", "viewer", "guest", None):
                expected = (
                    [{key: "first"}, {key: "second"}]
                    if role in allowed_roles else []
                )
                with self.subTest(key=key, role=role):
                    self.assertEqual(json_search(key, nested, role=role), expected)

    def test_parent_search_filters_protected_descendants(self):
        """Parent matches cannot expose restricted fields through nested lists."""
        nested = {
            "container": [
                {"apiKey": "secret", "label": "public"},
                {"nested": {"managementIpAddress": "private", "issueSummary": "ok"}},
            ]
        }
        original = deepcopy(nested)
        self.assertEqual(
            json_search("container", nested, role="viewer"),
            [{"container": [{"label": "public"}, {"nested": {"issueSummary": "ok"}}]}],
        )
        self.assertEqual(
            json_search("container", nested),
            [{"container": [{"label": "public"}, {"nested": {}}]}],
        )
        self.assertEqual(json_search("container", nested, role="admin"), [original])
        self.assertEqual(nested, original)

    def test_restricted_container_blocks_traversal(self):
        """Public child names cannot bypass a protected parent field."""
        nested = {"apiKey": {"value": "secret"}, "public": {"value": "visible"}}
        self.assertEqual(json_search("value", nested, role="viewer"), [{"value": "visible"}])
        self.assertEqual(
            json_search("value", nested, role="admin"),
            [{"value": "secret"}, {"value": "visible"}],
        )


if __name__ == "__main__":
    unittest.main()
