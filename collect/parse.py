from bs4 import BeautifulSoup

from collect.models import ListPage, DetailPage, AttributionToken


def met_parse_list():
    lps = ListPage.objects.filter(institution="met")
    details = []
    for lp in lps:
        soup = BeautifulSoup(lp.html)
        links = soup.find_all("a", class_="result-object")
        for link in links:
            details.append(
                DetailPage(
                    url=link["href"],
                    title=link["title"],
                    attribution=link.find(
                        "div", class_="result-object__attribution"
                    ).text,
                    parent=lp,
                )
            )
    DetailPage.objects.bulk_create(details)


def met_tokenize_attributes():
    for page in DetailPage.objects.filter(parent__institution="met"):
        tokens = [t.strip() for t in page.attribution.split(",")]
        for token_str in tokens:
            token, _ = AttributionToken.objects.get_or_create(value=token_str)
            page.tokens.add(token)
