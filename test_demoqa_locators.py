# Import Page and Playwright classes from Playwright.
#
# Page:
#   Represents one browser tab/page.
#
# Playwright:
#   The main Playwright object that gives us access
#   to Chromium, Firefox, and WebKit.
from playwright.sync_api import Page, expect, Playwright


# "page: Page" means:
#
# page      -> the name of the parameter/fixture
# : Page    -> a type hint saying that "page" is a Page object
#
# Playwright's pytest plugin automatically provides the "page"
# fixture to this test.
#
# So we DON'T need to create the browser or page ourselves.
def test_submit_form(page: Page):

    # Open the website in the browser tab.
    page.goto("https://demoqa.com/text-box")

    # Locate the element by its HTML id.
    #
    # "#" is CSS syntax for an id.
    #
    # HTML:
    # <input id="userName">
    #
    # Playwright:
    # #userName
    page.locator("#userName").fill("Anna Test")

    # Locate the element using Playwright's "id=" selector.
    #
    # This:
    #     id=userEmail
    #
    # is another way to locate:
    #     <input id="userEmail">
    page.locator("id=userEmail").fill("anna@test.ge")

    # Locate the element by id and fill it.
    page.locator("#currentAddress").fill("Tbilisi")

    # Locate the element by id and fill it.
    page.locator("#permanentAddress").fill("Batumi")

    # Locate the Submit button by id and click it.
    page.locator("#submit").click()

    # Store the #output element in a variable.
    #
    # This is useful because we want to work with
    # several elements inside #output.
    output = page.locator("#output")

    # Find #name INSIDE the #output element.
    #
    # This is called locator chaining.
    #
    # output
    #   └── #name
    #
    # Then check that the text is exactly:
    # "Name:Anna Test"
    expect(output.locator("#name")).to_have_text("Name:Anna Test")

    # Find #email inside #output
    # and check its text.
    expect(output.locator("#email")).to_have_text(
        "Email:anna@test.ge"
    )

    # Check that #output contains "Tbilisi".
    #
    # to_contain_text() means the element's text
    # only needs to contain the specified text.
    expect(output).to_contain_text("Tbilisi")

    # Check that #output contains "Batumi".
    expect(output).to_contain_text("Batumi")

    # Find text on the page.
    #
    # The website has a real typo:
    # "Permananet Address"
    #
    # This assertion checks that the typo is visible.
    expect(page.get_by_text("Permananet Address")).to_be_visible()


# Here we use:
#
# "playwright: Playwright"
#
# playwright  -> parameter/fixture name
# : Playwright -> type hint
#
# Unlike the previous test, we are NOT given a Page directly.
# We are given the main Playwright object.
#
# We can use it to create our own browser.
def test_submit_form_headless_off(playwright: Playwright):

    # Use the Playwright object to launch Chromium.
    #
    # playwright
    #     ↓
    # chromium
    #     ↓
    # launch()
    #
    # headless=False:
    #     Show the browser window.
    #
    # slow_mo=500:
    #     Wait 500 milliseconds between actions.
    #     This makes the test easier to watch.
    browser = playwright.chromium.launch(
        headless=False,
        slow_mo=500
    )

    # Create a new browser tab/page.
    #
    # browser
    #    ↓
    # new_page()
    #    ↓
    # page
    page = browser.new_page()

    # Open the website.
    page.goto("https://demoqa.com/text-box")

    # Find the element by id and fill it.
    page.locator("#userName").fill("Anna Test")

    # Find the element by id and fill it.
    page.locator("#userEmail").fill("anna@test.ge")

    # Fill Current Address.
    page.locator("#currentAddress").fill("Tbilisi")

    # Fill Permanent Address.
    page.locator("#permanentAddress").fill("Batumi")

    # Click Submit.
    page.locator("#submit").click()

    # Store the output element.
    output = page.locator("#output")

    # Verify the Name.
    expect(output.locator("#name")).to_have_text("Name:Anna Test")

    # Verify the Email.
    expect(output.locator("#email")).to_have_text(
        "Email:anna@test.ge"
    )

    # Verify Current Address.
    expect(output).to_contain_text("Tbilisi")

    # Verify Permanent Address.
    expect(output).to_contain_text("Batumi")

    # Verify the typo on the page.
    expect(page.get_by_text("Permananet Address")).to_be_visible()
