from collect.models import ListPage


def met_list_url(offset):
    return f"https://www.metmuseum.org/art/collection/search?offset={offset}&showOnly=withImage%7CopenAccess&material=Paintings"


def met_generate_list_urls():
    # total items 8413
    # paginates by 40
    pages = [
        ListPage(url=met_list_url(offset), institution="met")
        for offset in range(0, 8413, 40)
    ]
    ListPage.objects.bulk_create(pages)
