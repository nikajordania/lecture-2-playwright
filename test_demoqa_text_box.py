# Three test cases from test-cases.xlsx, automated with Playwright.
# One test function = one test case (TC-01, TC-02, TC-03).
#
# Run all of them:        uv run pytest test_demoqa_text_box.py
# Watch the browser:      uv run pytest test_demoqa_text_box.py --headed --slowmo 500
from playwright.sync_api import Page, expect

URL = "https://demoqa.com/text-box"


def test_tc01_all_fields_are_shown_after_submit(page: Page):
    # Preconditions: the form is open and empty
    page.goto(URL)

    # Steps 1-5
    page.locator("#userName").fill("Anna Test")
    page.locator("#userEmail").fill("anna@test.ge")
    page.locator("#currentAddress").fill("Tbilisi")
    page.locator("#permanentAddress").fill("Batumi")
    page.locator("#submit").click()

    # Expected result: the output box shows all four values.
    # We search INSIDE #output, because the form fields
    # #currentAddress and #permanentAddress have the same ids.
    output = page.locator("#output")
    expect(output.locator("#name")).to_have_text("Name:Anna Test")
    expect(output.locator("#email")).to_have_text("Email:anna@test.ge")
    expect(output.locator("#currentAddress")).to_contain_text("Tbilisi")
    expect(output.locator("#permanentAddress")).to_contain_text("Batumi")


def test_tc02_invalid_email_is_highlighted(page: Page):
    page.goto(URL)

    # Email without "@" is invalid
    page.locator("#userName").fill("Anna Test")
    page.locator("#userEmail").fill("anna.test.ge")
    page.locator("#submit").click()

    # Expected result: the Email field gets the CSS class "field-error"
    # (red border), and nothing is shown in the output box.
    expect(page.locator("#userEmail")).to_contain_class("field-error")
    expect(page.locator("#output #name")).to_have_count(0)


def test_tc03_only_name_is_shown_when_other_fields_are_empty(page: Page):
    page.goto(URL)

    # Only one field is filled in
    page.locator("#userName").fill("Anna Test")
    page.locator("#submit").click()

    # Expected result: the name is shown, the email line is not
    output = page.locator("#output")
    expect(output.locator("#name")).to_have_text("Name:Anna Test")
    expect(output.locator("#email")).to_have_count(0)
