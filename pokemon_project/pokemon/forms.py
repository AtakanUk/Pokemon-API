from django import forms

class PokemonForm(forms.Form):
    email = forms.CharField(
        label='Email (separate multiple addresses with spaces):',
        widget=forms.Textarea(attrs={'placeholder': 'Enter Email Addresses'}),
        required=True
    )
    pokemon_name = forms.CharField(
        label='Pokemon (separate multiple addresses with spaces):',
        widget=forms.Textarea(attrs={'placeholder': 'Enter Pokemon Name'}),
        required=True
    )
