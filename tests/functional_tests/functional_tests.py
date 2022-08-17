import pytest
from pylenium.driver import Pylenium


TEST_APP_URL = "http://localhost:5000/"


def test_textarea_input_triggers_overall_and_individual_sentiments(
    run_server,
    py: Pylenium,
):
    py.visit(TEST_APP_URL)
    textarea = py.get("#text_for_analysis")

    textarea.type("test")

    #  ("css_selector > *")  -> is CSS for any direct children of element with selector "css_selector"
    assert py.get("#overall-sentiment-container > *").should().be_visible()
    assert py.get("#sentiments").should().be_visible()
