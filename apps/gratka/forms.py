from django import forms
from django.core.exceptions import ValidationError

from .models import UserConfig

TAILWIND_INPUT = (
    'mt-1 block w-full rounded-md border-gray-300 shadow-sm '
    'focus:border-indigo-500 focus:ring-indigo-500 text-sm '
    'px-3 py-2 border'
)

TAILWIND_CHECKBOX = 'h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500'

TAILWIND_SELECT = (
    'mt-1 block w-full rounded-md border-gray-300 shadow-sm '
    'focus:border-indigo-500 focus:ring-indigo-500 text-sm '
    'px-3 py-2 border bg-white'
)

LOKALIZACJA_CHOICES = [
    ('bialystok', 'Białystok'),
    ('bielsko-biala', 'Bielsko-Biała'),
    ('bydgoszcz', 'Bydgoszcz'),
    ('bytom', 'Bytom'),
    ('czestochowa', 'Częstochowa'),
    ('gdansk', 'Gdańsk'),
    ('gdynia', 'Gdynia'),
    ('gliwice', 'Gliwice'),
    ('gorzow-wielkopolski', 'Gorzów Wielkopolski'),
    ('katowice', 'Katowice'),
    ('kielce', 'Kielce'),
    ('koszalin', 'Koszalin'),
    ('krakow', 'Kraków'),
    ('lublin', 'Lublin'),
    ('lodz', 'Łódź'),
    ('olsztyn', 'Olsztyn'),
    ('opole', 'Opole'),
    ('poznan', 'Poznań'),
    ('radom', 'Radom'),
    ('rzeszow', 'Rzeszów'),
    ('sosnowiec', 'Sosnowiec'),
    ('szczecin', 'Szczecin'),
    ('torun', 'Toruń'),
    ('warszawa', 'Warszawa'),
    ('wroclaw', 'Wrocław'),
    ('zabrze', 'Zabrze'),
    ('zielona-gora', 'Zielona Góra'),
]


class UserConfigForm(forms.ModelForm):
    class Meta:
        model = UserConfig
        fields = [
            'lokalizacja', 'cena_min', 'cena_max',
            'metraz_min', 'metraz_max',
            'balkon', 'garaz', 'piwnica',
        ]
        labels = {
            'lokalizacja': 'Lokalizacja',
            'cena_min': 'Cena minimalna (PLN)',
            'cena_max': 'Cena maksymalna (PLN)',
            'metraz_min': 'Metraż min (m²)',
            'metraz_max': 'Metraż max (m²)',
            'balkon': 'Balkon',
            'garaz': 'Garaż',
            'piwnica': 'Piwnica',
        }
        widgets = {
            'lokalizacja': forms.Select(
                choices=LOKALIZACJA_CHOICES,
                attrs={'class': TAILWIND_SELECT},
            ),
            'cena_min': forms.NumberInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': '100000',
            }),
            'cena_max': forms.NumberInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': '250000',
            }),
            'metraz_min': forms.NumberInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'np. 30',
            }),
            'metraz_max': forms.NumberInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'np. 80',
            }),
            'balkon': forms.CheckboxInput(attrs={'class': TAILWIND_CHECKBOX}),
            'garaz': forms.CheckboxInput(attrs={'class': TAILWIND_CHECKBOX}),
            'piwnica': forms.CheckboxInput(attrs={'class': TAILWIND_CHECKBOX}),
        }

    def clean(self):
        cleaned_data = super().clean()
        cena_min = cleaned_data.get('cena_min')
        cena_max = cleaned_data.get('cena_max')
        metraz_min = cleaned_data.get('metraz_min')
        metraz_max = cleaned_data.get('metraz_max')

        if cena_min is not None and cena_max is not None and cena_min >= cena_max:
            raise ValidationError('Cena minimalna musi być mniejsza od maksymalnej.')

        if metraz_min is not None and metraz_max is not None and metraz_min >= metraz_max:
            raise ValidationError('Metraż minimalny musi być mniejszy od maksymalnego.')

        return cleaned_data
