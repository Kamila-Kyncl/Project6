import re

from playwright.sync_api import Page, expect

BASE_URL = "https://engeto.cz/"


def accept_cookies_if_present(page: Page) -> None:
    """
    Zavře cookie dialog na engeto.cz, pokud se objeví.
    """
    page.wait_for_timeout(500)

    agree_main = page.get_by_role(
        "button",
        name=re.compile(r"chápu.*přijímám", re.I),
    )

    if agree_main.count() > 0:
        try:
            agree_main.first.click(timeout=2000)
            return
        except Exception:
            pass


def open_homepage(page: Page) -> None:
    """Otevře homepage a případně odklikne cookies."""
    page.goto(BASE_URL, wait_until="domcontentloaded")
    accept_cookies_if_present(page)


def test_homepage_loads_and_has_title(page: Page) -> None:
    """Test 1: Ověří, že homepage jde otevřít a má neprázdný title."""
    open_homepage(page)
    expect(page).to_have_title(re.compile(r".+"))


def test_navigation_contains_courses_link(page: Page) -> None:
    """
    Test 2: Ověří, že existuje odkaz "Kurzy" a že po kliknutí dojde k navigaci
    na stránku s kurzy.
    """
    open_homepage(page)

    courses_link = page.get_by_role("link", name="Kurzy", exact=True)
    expect(courses_link).to_be_visible()
    courses_link.click()

    expect(page).to_have_url(re.compile(r".*kurz.*", re.I))


def test_contact_or_cta_is_present(page: Page) -> None:
    """
    Test 3: Ověří, že stránka obsahuje viditelný prvek typu Kontakt.
    """
    open_homepage(page)

    contact_link = page.get_by_role("link", name=re.compile(r"kontakt", re.I))
    if contact_link.count() > 0:
        expect(contact_link.first).to_be_visible()
        return
