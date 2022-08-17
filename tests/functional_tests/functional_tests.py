"""
The tests are implemented with dependencies overridden in `test/conftest.py`,
please keep that in mind when asserting numbers of elements and their values.

In a production environment functional tests shouldn't have overridden dependencies!

UI tests implemented in this manner (with overridden dependencies) can serve as 
tests for our frontend/DOM manipulation logic though, because we don't have any 
unit/integration tests for our htmx and _hyperscript code.
"""
from pylenium.driver import Pylenium


TEST_APP_URL = "http://localhost:5000/"


def test_textarea_input_triggers_overall_and_individual_sentiments(
    run_server,
    py: Pylenium,
):
    py.visit(TEST_APP_URL)
    textarea = py.get("textarea#text_for_analysis")

    textarea.type("test")

    assert all(
        [
            child_element.should().be_visible
            for child_element in py.get("#overall-sentiment-container").children()
        ]
    )
    assert all(
        [
            child_element.should().be_visible
            for child_element in py.get("#sentiments").children()
        ]
    )


def test_clicking_get_wordcloud_button_renders_wordcloud(
    run_server,
    py: Pylenium,
):
    py.visit(TEST_APP_URL)

    py.get("button#get-wordcloud").click()

    assert py.get("#wordcloud").get("svg").should().be_visible()


def test_textarea_content_persists_in_between_reloads_and_reopens(
    run_server, py: Pylenium
):
    py.visit(TEST_APP_URL)
    text_to_type = "test if persists after refresh"

    py.get("textarea#text_for_analysis").type(text_to_type)

    assert (
        py.reload()
        .get("textarea#text_for_analysis")
        .should(timeout=10)
        .have_attr("value", value=text_to_type)
    )
    assert (
        py.switch_to.new_tab()
        .visit(TEST_APP_URL)
        .get("textarea#text_for_analysis")
        .should(timeout=10)
        .have_attr("value", value=text_to_type)
    )
    assert (
        py.switch_to.new_window()
        .visit(TEST_APP_URL)
        .get("textarea#text_for_analysis")
        .should(timeout=10)
        .have_attr("value", value=text_to_type)
    )
