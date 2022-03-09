from django import forms


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
