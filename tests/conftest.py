"""Test configuration for PyTest.

Imports all fixtures that are used in the unittesting.
"""

# ruff: noqa
from fixtures_db_creation import my_data
from fixtures_model import (
    normal_user_1,
    normal_user_2,
    root_user,
    service_user,
    test_api_client_to_delete,
    test_api_clients,
    test_api_token_to_delete,
    test_api_tokens,
    test_normal_user,
    test_normal_user_to_delete,
    test_root_user,
    test_tag_to_delete,
    test_tags,
    test_user_setting_to_delete,
    test_user_settings,
)
