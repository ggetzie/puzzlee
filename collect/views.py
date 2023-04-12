import json
from typing import Any, Dict

from django.db.models import QuerySet
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView

from collect.models import ListPage, DetailPage
from collect.forms import ApprovalForm
from core.views import UserIsStaffMixin
from core.decorators import user_is_staff_api


class ListPageList(UserIsStaffMixin, ListView):
    model = ListPage
    template = "collect/listpage_list.html"
    paginate_by = 100


class ListPageDetail(UserIsStaffMixin, DetailView):
    model = ListPage
    template_name = "collect/listpage_detail.html"


class DetailPageDetail(UserIsStaffMixin, DetailView):
    model = DetailPage
    template_name = "collect/detailpage_detail.html"


class FilteredDetail(UserIsStaffMixin, ListView):
    model = DetailPage
    template_name = "collect/filtered_detail.html"

    paginate_by = 100

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        institution = self.kwargs["institution"]
        approved = self.kwargs["approved"]
        qs = (
            qs.filter(parent__institution=institution, approved=approved)
            .exclude(artworkimage__image__exact="")
            .exclude(artist_name="")
            .exclude(title="")
            .exclude(year="")
            .order_by("artist_name", "title")
        )
        return qs

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["institution"] = self.kwargs["institution"]
        context["approved"] = self.kwargs["approved"]
        context[
            "approved_choices"
        ] = DetailPage.approved.field.choices  # pylint: disable=no-member
        return context


@require_POST
@user_is_staff_api
def set_approved(request):
    data = json.loads(request.body)
    print(data)
    form = ApprovalForm(data)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": "success"})
    else:
        return JsonResponse({"status": "error", "message": form.errors}, status=400)
