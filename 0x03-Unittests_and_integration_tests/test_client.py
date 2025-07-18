#!/usr/bin/env python3
"""Unit tests for GithubOrgClient"""
import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test suite for GithubOrgClient"""

    @parameterized.expand([
        ("google", {"login": "google", "repos_url": "https://api.github.com/orgs/google/repos"}),
        ("abc", {"login": "abc", "repos_url": "https://api.github.com/orgs/abc/repos"}),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, expected_payload, mock_get_json):
        """
        Test that GithubOrgClient.org returns correct value
        and that get_json is called once with correct URL
        """
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient(org_name)
        result = client.org

        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(result, expected_payload)

        def test_public_repos_url(self):
            """Test that _public_repos_url returns expected URL based on mocked org"""
            expected_url = "https://api.github.com/orgs/testorg/repos"
            payload = {"repos_url": expected_url}

            with patch.object(GithubOrgClient, 'org', new_callable=property) as mock_org:
                mock_org.return_value = payload
                client = GithubOrgClient("testorg")
                result = client._public_repos_url
                self.assertEqual(result, expected_url)
