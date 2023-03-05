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
    template = "collect/listpage_detail.html"


class DetailPageDetail(UserIsStaffMixin, DetailView):
    model = DetailPage
    template = "collect/detailpage_detail.html"
