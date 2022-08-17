import pytest
from pylenium.driver import Pylenium


test_app_url = "http://localhost:5000/"


def test_textarea_input_triggers_overall_and_individual_sentiments(
    run_server,
    py: Pylenium,
):
    py.visit(test_app_url)
    py.screenshot("fail.png")
    assert False
