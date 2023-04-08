from django import forms
from collect.models import DetailPage


class ApprovalForm(forms.Form):
    detailpage = forms.ModelChoiceField(queryset=DetailPage.objects.all())
    approved = forms.ChoiceField(choices=DetailPage.APPROVED_CHOICES)

    def save(self):
        dp = self.cleaned_data["detailpage"]
        dp.approved = self.cleaned_data["approved"]
        dp.save()
