from django.urls import include, path, register_converter
import collect.views as views

app_name = "collect"


class ApprovedStateConverter:
    regex = "[0-2]"

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return f"{value}"


register_converter(ApprovedStateConverter, "apr")


listpage_urls = [
    path("", view=views.ListPageList.as_view(), name="listpage_list"),
    path("<int:pk>", view=views.ListPageDetail.as_view(), name="listpage_detail"),
]

detailpage_urls = [
    path("<int:pk>", view=views.DetailPageDetail.as_view(), name="detailpage_detail"),
    path(
        "review/<str:institution>/<apr:approved>",
        view=views.FilteredDetail.as_view(),
        name="detail_filtered",
    ),
    path("set_approved/<int:dp_id>", view=views.set_approved, name="set_approved"),
]


urlpatterns = [
    path("listpage/", include(listpage_urls)),
    path("detailpage/", include(detailpage_urls)),
]
