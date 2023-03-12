from typing import Any, Dict

from django.db.models import QuerySet
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView

from collect.models import ListPage, DetailPage
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
        qs = qs.filter(parent__institution=institution)
        if institution == "met":
            qs = qs.filter(attribution__regex=r",\D*\d{4}")
        return qs

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["institution"] = self.kwargs["institution"]
        return context


@require_POST
@user_is_staff_api
def set_candidate(request):
    dp_id = request.POST["detailpage_id"]
    try:
        dp = DetailPage.objects.get(id=dp_id)
        dp.is_candidate = request.POST["is_candidate"]
        dp.save()
    except DetailPage.DoesNotExist:
        return JsonResponse(
            {"status": "error", "message": f"DetailPage with id {dp_id} not found"},
            status=404,
        )


@require_POST
@user_is_staff_api
def set_approved(request):
    dp_id = request.POST["detailpage_id"]
    try:
        dp = DetailPage.objects.get(id=dp_id)
        dp.approved = request.POST["approved"]
        dp.save()
    except DetailPage.DoesNotExist:
        return JsonResponse(
            {"status": "error", "message": f"DetailPage with id {dp_id} not found"},
            status=404,
        )
