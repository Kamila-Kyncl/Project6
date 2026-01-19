import re

from playwright.sync_api import Page, expect

BASE_URL = "https://engeto.cz/"


def accept_cookies_if_present(page: Page) -> None:
    """
    Zavře cookie dialog (CookieScript) pokud se objeví.
    Zamezí tomu, aby overlay blokoval klikání na UI.
    """
    wrapper = page.locator("#cookiescript_injected_wrapper")

    try:
        # Počkej krátce, jestli se dialog vůbec objeví
        wrapper.wait_for(state="visible", timeout=3000)

        # Zkus najít a kliknout na hlavní tlačítko souhlasu
        accept_btn = wrapper.get_by_role(
            "button",
            name=re.compile(r"(chápu|přijímám|souhlasím)", re.I),
        )

        # V CookieScriptu může být víc buttonů – vezmeme první viditelný
        accept_btn.first.click(timeout=3000)
        return

    except TimeoutError:
        # banner se neukázal
        return

    except Exception:
        # fallback: ESC někdy zavře modal
        page.keyboard.press("Escape")

        # pokud overlay pořád existuje, poslední záchrana = odstranit z DOM
        try:
            if wrapper.is_visible():
                wrapper.evaluate("el => el.remove()")
        except Exception:
            pass


def open_homepage(page: Page) -> None:
    """Otevře homepage a případně odklikne cookies."""
    page.goto(BASE_URL, wait_until="domcontentloaded")
    accept_cookies_if_present(page)


def test_homepage_loads_and_has_engeto_title(page: Page) -> None:
    """
    Test 1:
    Ověří, že homepage ENGETO:
    - se načte
    - má v title značku ENGETO
    - zůstane na homepage URL
    """
    open_homepage(page)

    expect(page).to_have_url(re.compile(r"engeto\.cz/?$"))
    expect(page).to_have_title(re.compile(r"ENGETO", re.I))


def test_navigation_to_courses_page(page: Page) -> None:
    """
    Test 2:
    Ověří, že klik na 'Kurzy' vede na stránku Přehled kurzů.
    """
    open_homepage(page)

    courses_link = page.get_by_role("link", name="Kurzy", exact=True)
    expect(courses_link).to_be_visible()

    courses_link.click()

    expect(page).to_have_url(re.compile(r"/prehled-kurzu/?$"))


def test_contact_or_primary_cta_is_present(page: Page) -> None:
    """
    Test 3:
    Ověří, že stránka obsahuje alespoň jeden důležitý CTA prvek:
    - Kontakt
    - nebo Výukový portál / Akademie apod.

    Test vždy obsahuje aserci - pokud nic nenajde, selže.
    """
    open_homepage(page)

    possible_cta = page.get_by_role(
        "link",
        name=re.compile(
            r"(kontakt|výukový portál|akademie)",
            re.I,
        ),
    )

    expect(
        possible_cta.first,
        "Na stránce nebyl nalezen žádný očekávaný kontakt/CTA prvek",
    ).to_be_visible()
