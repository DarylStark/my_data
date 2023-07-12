"""TODO: documentation. """

from my_data.my_data import MyData


def test_check_configuration(my_data: MyData) -> None:
    with my_data.get_context(None) as c:
        assert True
