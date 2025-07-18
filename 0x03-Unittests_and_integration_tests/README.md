# 0x03. Unittests and Integration Tests

This project focuses on writing **unit tests** and **integration tests** in Python using the `unittest` framework, `mock` library, and related testing tools.

---

## 📚 Learning Objectives

By the end of this project, you should be able to explain:

- The difference between **unit tests** and **integration tests**
- How to write unit tests to test specific functions or classes
- How to write integration tests that simulate real application behavior
- The importance of mocking in testing external dependencies like APIs and databases
- How to use `unittest.mock`, `@patch`, and `@parameterized.expand`
- How and when to use fixtures and memoization
- How to run tests with `unittest`

---

## 🛠️ Project Requirements

- All files interpreted/compiled with **Python 3.7**
- Code is written for **Ubuntu 18.04 LTS**
- Code must follow **pycodestyle (PEP8)** version 2.5
- All files are executable (`chmod +x filename.py`)
- All modules, classes, and functions include **complete docstrings**
- All functions and methods are **type-annotated**
- `README.md` file is mandatory at the root of the project

---

## 📂 Project Structure

```bash
0x03-Unittests_and_integration_tests/
├── client.py          # GitHubOrgClient and related methods
├── fixtures.py        # Mocked GitHub API response data
├── test_client.py     # Unit and integration tests for GitHubOrgClient
├── test_utils.py      # Unit tests for access_nested_map, get_json, memoize
├── utils.py           # Utility functions used throughout the project
└── README.md          # Project documentation
