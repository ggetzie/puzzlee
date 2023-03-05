from django.urls import include, path
import collect.views as views

app_name = "collect"

listpage_urls = [
    path("", view=views.ListPageList.as_view(), name="listpage_list"),
    path("<int:pk>", view=views.ListPageDetail.as_view(), name="listpage_detail"),
]

detailpage_urls = [
    path("<int:pk>", view=views.DetailPageDetail.as_view(), name="detailpage_detail")
]


urlpatterns = [
    path("listpage/", include(listpage_urls)),
    path("detailpage/", include(detailpage_urls)),
]
