from typing import Any, Dict

from django.db.models import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from collect.models import ListPage, DetailPage
from core.views import UserIsStaffMixin


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
