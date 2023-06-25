import json
from typing import Any, Dict

from django.db.models import QuerySet
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404, render

from collect.models import ListPage, DetailPage
from collect.forms import SetStatusForm, ApproveForm
from core.views import UserIsStaffMixin
from core.decorators import user_is_staff_api

from game.models import Artist, Artwork, ArtworkImage


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
        approval_status = self.kwargs["approval_status"]
        qs = (
            qs.filter(parent__institution=institution, approved=approval_status)
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
        context["approval_status"] = self.kwargs["approval_status"]
        context["approved_choices"] = DetailPage.APPROVED_CHOICES
        return context


@require_POST
@user_is_staff_api
def set_status(request):
    data = json.loads(request.body)
    form = SetStatusForm(data)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": "success"})
    else:
        return JsonResponse({"status": "error", "message": form.errors}, status=400)


@user_is_staff_api
def approve_detailpage(request, pk):
    if request.method == "GET":
        dp = get_object_or_404(DetailPage, pk=pk)
        artists = Artist.objects.filter(fullname__iequals=dp.artist_name)
        initial = {"detailpage": dp.pk, "title": dp.title}
        if artists.count() > 0:
            initial["artist_answer"] = artists[0].answer
            initial["artist_fullname"] = artists[0].fullname
        form = ApproveForm(initial=initial)
        return render(
            request, "collect/add_artwork_modal.html", {"form": form, "detailpage": dp}
        )

    elif request.method == "POST":
        data = json.loads(request.body)
        form = ApproveForm(data)
        if form.is_valid():
            form.save(user=request.user)
            return JsonResponse({"status": "success"})
        else:
            return JsonResponse({"status": "error", "message": form.errors}, status=400)
    else:
        return JsonResponse(
            {"status": "error", "message": "Invalid method"}, status=400
        )


@require_POST
@user_is_staff_api
def reject_detailpage(request):
    data = json.loads(request.body)
    return JsonResponse({"status": "success"})
