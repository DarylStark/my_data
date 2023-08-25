import toml
import re
import sys

invalid_versions = [
    r'-?dev[0-9]*$',
]


def is_valid_version(version: str) -> bool:
    """Check if the version is valid.

    Checks if a version is valid.

    Args:
        version: the version string from pyproject.toml.

    Returns:
        True if the version is correct, otherwise False.
    """
    for invalid in invalid_versions:
        if re.search(invalid, version):
            return False
    return True


if __name__ == '__main__':
    # Get the data from `pyproject.toml`
    data = toml.load('./pyproject.toml')
    poetry = data['tool']['poetry']

    # Get the main dependencies
    dependencies = {'main': poetry['dependencies']}

    # Get the group dependencies
    for group_name, group_config in poetry['group'].items():
        dependencies[group_name] = group_config['dependencies']

    # Loop through them
    error = False
    for group_name, group_dependencies in dependencies.items():
        for dependency, version in group_dependencies.items():
            if not is_valid_version(version):
                error = True
                print(
                    f'Dependency "{dependency} {version}" in group ' +
                    f'"{group_name}" has a invalid version!')

    # Exit with a error code if there were errors
    sys.exit(0 if not error else 1)
