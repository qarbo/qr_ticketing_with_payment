from django import forms

from booking.models import Booking, Table


class BookingForm(forms.ModelForm):
    tables = forms.ModelMultipleChoiceField(
        queryset=Table.objects.all(),
        widget=forms.SelectMultiple(attrs={'style': 'height: 200px'}),
        required=False,
    )

    class Meta:
        model = Booking
        fields = ('num_guests', 'tables')
