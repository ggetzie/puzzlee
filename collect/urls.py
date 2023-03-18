from django.urls import include, path
import collect.views as views

app_name = "collect"

listpage_urls = [
    path("", view=views.ListPageList.as_view(), name="listpage_list"),
    path("<int:pk>", view=views.ListPageDetail.as_view(), name="listpage_detail"),
]

detailpage_urls = [
    path("<int:pk>", view=views.DetailPageDetail.as_view(), name="detailpage_detail"),
    path(
        "filtered/<str:institution>",
        view=views.FilteredDetail.as_view(),
        name="detail_filtered",
    ),
    path("set_candidate/<int:dp_id>", view=views.set_candidate, name="set_candidate"),
    path("set_approved/<int:dp_id>", view=views.set_approved, name="set_approved"),
]


urlpatterns = [
    path("listpage/", include(listpage_urls)),
    path("detailpage/", include(detailpage_urls)),
]
