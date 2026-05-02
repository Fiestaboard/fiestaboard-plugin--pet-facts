"""Tests for the pet_facts plugin."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch, Mock

import pytest

from plugins.pet_facts import PetFactsPlugin
from src.plugins.base import PluginResult

MANIFEST = json.loads("""
{
    "id": "pet_facts",
    "name": "Pet Facts",
    "version": "0.1.0",
    "settings_schema": {
        "type": "object",
        "properties": {
            "enabled": {
                "type": "boolean",
                "title": "Enabled",
                "default": false
            },
            "animal": {
                "type": "string",
                "title": "Animal",
                "description": "Which animal facts to show.",
                "enum": [
                    "cat",
                    "dog",
                    "random"
                ],
                "default": "random"
            },
            "refresh_seconds": {
                "type": "integer",
                "title": "Refresh Interval (seconds)",
                "description": "How often to fetch a new fact.",
                "default": 300,
                "minimum": 60
            }
        },
        "required": []
    }
}
""")

SAMPLE_RESPONSE = json.loads("""
{
    "fact": "Cats sleep between 12 and 16 hours a day.",
    "length": 41
}
""")


@pytest.fixture
def plugin():
    return PetFactsPlugin(MANIFEST)


@pytest.fixture
def configured_plugin():
    p = PetFactsPlugin(MANIFEST)
    p.config = json.loads("""
{
    "animal": "cat"
}
""")
    return p


class TestPetFactsPlugin:

    def test_plugin_id(self, plugin):
        assert plugin.plugin_id == "pet_facts"

    def test_manifest_valid(self):
        manifest_path = Path(__file__).parent.parent / "manifest.json"
        with open(manifest_path) as f:
            m = json.load(f)
        for field in ("id", "name", "version"):
            assert field in m

    @patch("plugins.pet_facts.requests.get")
    def test_fetch_data_success(self, mock_get, configured_plugin):
        mock_response = Mock()
        mock_response.json.return_value = SAMPLE_RESPONSE
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = configured_plugin.fetch_data()

        assert result.available is True
        assert result.error is None
        assert result.data is not None
        assert "fact" in result.data, "missing variable: fact"
        assert "animal" in result.data, "missing variable: animal"

    @patch("plugins.pet_facts.requests.get")
    def test_fetch_data_network_error(self, mock_get, configured_plugin):
        import requests as req_mod
        mock_get.side_effect = req_mod.exceptions.ConnectionError("network down")

        result = configured_plugin.fetch_data()

        assert result.available is False
        assert result.error is not None

    @patch("plugins.pet_facts.requests.get")
    def test_fetch_data_bad_json(self, mock_get, configured_plugin):
        mock_response = Mock()
        mock_response.json.side_effect = ValueError("bad json")
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = configured_plugin.fetch_data()

        assert result.available is False

