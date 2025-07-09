from django import forms


class SellBookForm(forms.Form):
    title = forms.CharField(max_length=200)
    author = forms.CharField(max_length=200)
    description = forms.CharField(widget=forms.Textarea)
    price = forms.DecimalField(max_digits=10, decimal_places=2)
    image = forms.ImageField(required=False)
    is_sold = forms.BooleanField(required=False)
