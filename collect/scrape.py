import time

import requests
from django.utils import timezone
from selenium.webdriver import Firefox

from collect.models import ListPage


def fetch_list_pages(institution):
    unvisited = ListPage.objects.filter(institution=institution)
    with Firefox() as driver:
        for list_page in unvisited:
            driver.get(list_page.url)
            time.sleep(3)
            list_page.html = driver.page_source
            list_page.last_visited = timezone.now()
            list_page.save()
