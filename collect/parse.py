from bs4 import BeautifulSoup

from collect.models import ListPage, DetailPage, AttributionToken
from game.models import ArtworkImage


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


def met_get_artist_name(soup):
    spans = soup.find_all("span", class_="artwork__artist__name")
    if spans:
        return spans[0].text.strip()
    else:
        return ""


def met_get_year(soup):
    spans = soup.find_all("span", class_="artwork__creation-date")
    if spans:
        return spans[0].text.strip()
    else:
        return ""


def met_get_image_url(soup):
    anchors = soup.find_all("a", class_="gtm__download__image")
    if anchors:
        return anchors[0]["href"]
    else:
        return ""


def met_parse_detailpages():
    # get detail pages from the Met that have html and have not yet been parsed
    queryset = (
        DetailPage.objects.filter(parent__institution="met")
        .exclude(html="")
        .filter(parsed=False)
    )
    for page in queryset:
        soup = BeautifulSoup(page.html, "lxml")
        page.artist_name = met_get_artist_name(soup)
        page.year = met_get_year(soup)
        image_url = met_get_image_url(soup)
        image = ArtworkImage(detailpage=page, source=image_url)
        page.parsed = True
        page.save()
        image.save()
