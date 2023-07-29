from django import forms

from booking.models import Booking, Table


class BookingForm(forms.ModelForm):
    tables = forms.ModelMultipleChoiceField(
        queryset=Table.objects.all(),
        widget=forms.SelectMultiple(attrs={'style': 'height: 100px'}),
        required=False,
    )
    num_guests = forms.IntegerField(
        label="Guests at the bar",
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'dark-input'}),
        initial=0
    )

    class Meta:
        model = Booking
        fields = ('num_guests', 'tables')
