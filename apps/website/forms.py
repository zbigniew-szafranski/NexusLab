from django import forms


class ContactForm(forms.Form):
    imie = forms.CharField(label='Imię i nazwisko', max_length=100)
    email = forms.EmailField(label='Email')
    telefon = forms.CharField(label='Telefon', max_length=30, required=False)
    wiadomosc = forms.CharField(label='Wiadomość', max_length=5000, widget=forms.Textarea(attrs={'rows': 5}))
    # Honeypot: hidden from humans, bots tend to fill every field
    website = forms.CharField(required=False)
