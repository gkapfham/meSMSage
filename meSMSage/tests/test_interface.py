"""Test the functions in the interface module."""

from mesmsage import constants
from mesmsage import interface


def test_select_all_individuals_only_choice():
    """Ensure that all of the individuals in the total list are selected when all is chosen."""
    chosen_list = [constants.markers.All_Individuals]
    total_list = [constants.markers.All_Individuals, "First Person", "Second Person"]
    final_list = interface.create_individuals_list(chosen_list, total_list)
    assert final_list is not None
    assert len(final_list) == 2
    assert "First Person" in final_list
    assert "Second Person" in final_list


def test_select_all_individuals_one_of_choice():
    """Ensure that all of the individuals in the total list are selected when all is chosen plus an extra."""
    chosen_list = [constants.markers.All_Individuals, "Second Person"]
    total_list = [constants.markers.All_Individuals, "First Person", "Second Person"]
    final_list = interface.create_individuals_list(chosen_list, total_list)
    assert final_list is not None
    assert len(final_list) == 2
    assert "First Person" in final_list
    assert "Second Person" in final_list


def test_not_select_all_individuals_one_of_choice():
    """Ensure that one of the individuals in the total list are selected when that one is chosen."""
    chosen_list = ["Second Person"]
    total_list = [constants.markers.All_Individuals, "First Person", "Second Person"]
    final_list = interface.create_individuals_list(chosen_list, total_list)
    assert final_list is not None
    assert len(final_list) == 1
    assert "Second Person" in final_list


def test_not_select_all_individuals_two_of_choice():
    """Ensure that both of the individuals in the total list are selected when both are chosen."""
    chosen_list = ["First Person", "Second Person"]
    total_list = [constants.markers.All_Individuals, "First Person", "Second Person"]
    final_list = interface.create_individuals_list(chosen_list, total_list)
    assert final_list is not None
    assert len(final_list) == 2
    assert "First Person" in final_list
    assert "Second Person" in final_list
