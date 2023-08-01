from django import forms
from django.contrib.auth.models import User
from django.db.models import Q

from booking.models import Booking, Table

class BookingForm(forms.ModelForm):
    email = forms.EmailField(required=True, label="Email")
    fullname = forms.CharField(required=True, label="Full Name (as it appears on ID) / Полное имя (Как в Вашем ID)")

    def __init__(self, *args, table_id=None, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)

        # Filter the queryset for the 'user' field based on the user_id
        if table_id:
            self.fields['tables'].queryset = Table.objects.filter(Q(booking=None) | Q(id=table_id))
            if tables := self.instance.tables.all():
                self.fields['tables'].initial = tables[0].pk

    CHOICES = (
        ('regular_pass', 'Regular pass / Стандартный вход'),
        ('table', 'Table / Бронь стола'),
    )

    selected_option = forms.ChoiceField(choices=CHOICES, label='Choose ticket type / Выберите тип билета')

    tables = forms.ModelChoiceField(
        queryset=Table.objects.filter(booking=None),
        required=False,
        empty_label='Table not selected ... / Стол не выбран ...',
        label='Table / Бронь стола',
        to_field_name='id',  # Change 'id' to the field you want to use as the value of the selected option
        widget=forms.Select(attrs={'class': 'tables-select'}),
    )
    bar_guests = forms.IntegerField(
        label="Regular pass / Стандартный вход",
        min_value=0,
        initial=0,
        widget=forms.NumberInput(attrs={'class': 'dark-input regular-select'}),
    )

    def clean(self):
        cleaned_data = super().clean()
        tables = cleaned_data.get('tables')
        bar_guests = cleaned_data.get('bar_guests')

        if not tables and not bar_guests:
            raise forms.ValidationError("At least one of table or bar guest booking is required.")

    class Meta:
        model = Booking
        fields = ('email', 'fullname', 'selected_option', 'bar_guests', 'tables')
