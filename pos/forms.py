from django import forms
from .models import Group, Page

class GroupSelectionForm(forms.Form):
    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        empty_label="Select a group",
        to_field_name="name",
        label="Group"
    )

class PageSelectionForm(forms.Form):
    page = forms.ModelChoiceField(
        queryset=Page.objects.all(),
        empty_label="Select a page",
        to_field_name="name",
        label="Page"
    )