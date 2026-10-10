# Playwright + pytest with uv: setup from scratch

`uv` is a tool that installs Python, creates the project and installs packages for you.

## 1. Install uv (once per computer)

Windows (PowerShell):

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

macOS / Linux:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Close and reopen the terminal, then check that it works:

```bash
uv --version
```

## 2. Create a new project

```bash
uv init my-playwright-project
cd my-playwright-project
```

uv creates `pyproject.toml`, `.python-version`, `README.md` and `main.py`. You can delete `main.py`; you will not need it.

## 3. Add Playwright and pytest

```bash
uv add pytest-playwright
```

This one command installs `pytest-playwright` and `pytest`. It also writes both into `pyproject.toml` and `uv.lock`.

## 4. Download the browser (once)

```bash
uv run playwright install chromium
```

## 5. Write a test

Create a file whose name starts with `test_`, for example `test_example.py`:

```python
from playwright.sync_api import Page, expect


def test_name_field_is_visible(page: Page):
    page.goto("https://demoqa.com/text-box")
    expect(page.locator("#userName")).to_be_visible()
```

Each test function must also start with `test_`.

## 6. Run the tests

```bash
uv run pytest                          # all tests, browser hidden
uv run pytest --headed --slowmo 500    # watch the browser, 0.5 s per step
uv run pytest test_example.py -v       # one file, with test names
```

## 7. Turn off headless (see the browser)

By default the browser runs **headless**: it works, but you do not see a window.

### From the command line

```bash
uv run pytest --headed                     # show the browser window
uv run pytest --headed --slowmo 500        # show it and wait 0.5 s between actions
uv run pytest --headed --browser firefox   # another browser: chromium, firefox, webkit
```

These options work for every test that uses the `page` fixture.

### Always headed, without typing the option

Add this to `pyproject.toml`:

```toml
[tool.pytest.ini_options]
addopts = "--headed --slowmo 500"
```

Now `uv run pytest` always shows the browser. Remove these lines to go back to headless.

### In the code: the `playwright` object and `headless=False`

Instead of the ready `page` fixture, a test can take the `playwright` object and launch the browser itself:

```python
from playwright.sync_api import Playwright, expect


def test_name_with_visible_browser(playwright: Playwright):
    # Launch Chromium with a visible window, 0.5 s between actions
    browser = playwright.chromium.launch(headless=False, slow_mo=500)
    page = browser.new_page()

    page.goto("https://demoqa.com/text-box")
    page.locator("#userName").fill("Anna Test")
    page.locator("#submit").click()

    expect(page.locator("#output #name")).to_have_text("Name:Anna Test")

    # We opened the browser ourselves, so we close it ourselves
    browser.close()
```

The difference:

| `page: Page` | `playwright: Playwright` |
|---|---|
| pytest opens and closes the browser for you | you call `launch()` and `browser.close()` yourself |
| `--headed`, `--slowmo`, `--browser` work | the command-line options do **not** apply; `headless=False` is set in the code |
| use it for normal tests | use it when a test needs special browser settings |

## Already have a project (cloned or from a zip)?

Inside the project folder, run:

```bash
uv sync
uv run playwright install chromium
uv run pytest
```

`uv sync` creates `.venv` and installs everything listed in `uv.lock`.

## What to keep and what to skip

| Keep (share these) | Do not share |
|---|---|
| `pyproject.toml`, `uv.lock`, `.python-version`, `test_*.py`, `.xlsx` | `.venv`, `.pytest_cache`, `__pycache__`, `.idea` |
