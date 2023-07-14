"""Test configuration for PyTest.

Imports all fixtures that are used in the unittesting.
"""

from fixtures_db_creation import my_data
from fixtures_model import (normal_user_1, normal_user_2, root_user,
                            test_normal_user, test_normal_user_to_delete,
                            test_root_user, test_tag_to_delete, test_tags)
