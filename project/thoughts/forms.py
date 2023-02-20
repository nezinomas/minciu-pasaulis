from crispy_forms.helper import FormHelper
from django import forms

from ..core.lib.form_helper import set_field_properties
from . import models


class ThoughtForm(forms.ModelForm):
    class Meta:
        model = models.Thought
        fields = ['category', 'author', 'thought']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        set_field_properties(self, self.helper)
