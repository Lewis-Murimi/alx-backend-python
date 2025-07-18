#!/usr/bin/env python3
"""Unit tests for GithubOrgClient"""
import unittest
from unittest.mock import patch, PropertyMock, MagicMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Test suite for GithubOrgClient"""

    @parameterized.expand([
        ("google", {"login": "google",
                    "repos_url": "https://api.github.com/orgs/google/repos"}),
        ("abc", {"login": "abc",
                 "repos_url": "https://api.github.com/orgs/abc/repos"}),
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

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(result, expected_payload)

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test GithubOrgClient.public_repos returns
        expected list of repo names"""
        test_repos_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
            {"name": "repo3"}
        ]
        mock_get_json.return_value = test_repos_payload
        test_url = "https://api.github.com/orgs/testorg/repos"

        with patch.object(
                GithubOrgClient,
                "_public_repos_url",
                new_callable=PropertyMock
        ) as mock_public_repos_url:
            mock_public_repos_url.return_value = test_url

            client = GithubOrgClient("testorg")
            repos = client.public_repos()

            self.assertEqual(repos, ["repo1", "repo2", "repo3"])
            mock_get_json.assert_called_once_with(test_url)
            mock_public_repos_url.assert_called_once()

    @patch.object(GithubOrgClient, 'org', new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """Test that _public_repos_url returns expected URL"""
        payload = {"repos_url": "https://api.github.com/orgs/testorg/repos"}
        mock_org.return_value = payload

        client = GithubOrgClient("testorg")
        self.assertEqual(
            client._public_repos_url,
            "https://api.github.com/orgs/testorg/repos"
        )

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test GithubOrgClient.has_license returns expected boolean"""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


org_payload = {
    "login": "testorg",
    "repos_url": "https://api.github.com/orgs/testorg/repos"
}


repos_payload = [
    {"name": "repo1", "license": {"key": "apache-2.0"}},
    {"name": "repo2", "license": {"key": "mit"}},
    {"name": "repo3", "license": {"key": "apache-2.0"}},
]

expected_repos = ["repo1", "repo2", "repo3"]
apache2_repos = ["repo1", "repo3"]


@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test class"""

    @classmethod
    def setUpClass(cls):
        """Set up mock requests.get"""
        cls.get_patcher = patch('requests.get')
        mock_get = cls.get_patcher.start()

        def side_effect(url):
            mock_resp = MagicMock()
            if url == "https://api.github.com/orgs/testorg":
                mock_resp.json.return_value = cls.org_payload
            elif url == cls.org_payload["repos_url"]:
                mock_resp.json.return_value = cls.repos_payload
            return mock_resp

        mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patching"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test fetching all repo names"""
        client = GithubOrgClient("testorg")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test fetching repos with apache-2.0 license"""
        client = GithubOrgClient("testorg")
        self.assertEqual(client.public_repos(license="apache-2.0"),
                         self.apache2_repos)
