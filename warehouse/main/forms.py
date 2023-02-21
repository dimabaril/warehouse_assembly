from django import forms
from django.forms.models import inlineformset_factory

from .models import Element, ElementInElement


class ElementInElementForm(forms.ModelForm):
    """ElementInElement form."""
    # to_elem = forms.ModelChoiceField(
    #     queryset=Element.objects.all(),
    #     label='Содержит',  # customize the label for this field
    # )

    class Meta:
        model = ElementInElement
        fields = ('to_elem', 'amount',)
        # labels = {"to_elem": "Содержит", }  # не работает в inlineformset_factory

    def clean(self):
        cleaned_data = super().clean()
        from_elem = cleaned_data.get('from_elem')
        to_elem = cleaned_data.get('to_elem')

        # Check if a record with the same from_elem and to_elem already exists
        if ElementInElement.objects.filter(from_elem=from_elem, to_elem=to_elem).exists():
            raise forms.ValidationError('An element connection with the same from_elem and to_elem already exists.')


class ElementForm(forms.ModelForm):
    """Element form."""
    class Meta:
        model = Element
        fields = ('name', 'measurement_value', 'description', )  # 'include')
        labels = {'measurement_value': 'Ед. изм.', }


ElementInElementFormSet = inlineformset_factory(
        Element, ElementInElement,
        # form=ElementForm,
        fields=('to_elem', 'amount'),
        extra=5, fk_name='from_elem', )  # can_delete=True,
