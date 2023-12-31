from django.contrib import admin

from booking.models import Booking, Payment, Table, Zone, CheckIn

admin.site.register(Payment)
admin.site.register(Zone)
admin.site.register(Table)

class TableInline(admin.TabularInline):
    model = Table
    extra = 0  # Number of empty forms to display for adding new related tables

class CheckinInline(admin.TabularInline):
    model = CheckIn
    extra = 0  # Number of empty forms to display for adding new related tables

class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'fullname',
        'email',
        'bar_guests',
        'checked_guests',
        'paid',
        'created_at',
        'selected_option',
        'display_related_tables'
    )

    def display_related_tables(self, obj):
        related_tables = obj.tables.all()  # Assuming you have a related_name='tables' in your Booking model ForeignKey
        return ', '.join([str(table) for table in related_tables])

    display_related_tables.short_description = 'Related Tables'
    inlines = [TableInline, CheckinInline]

admin.site.register(Booking, BookingAdmin)

class CheckInAdmin(admin.ModelAdmin):
    list_display = (
        'booking',
        'guests_checked_in',
        'checkin_time',
    )

admin.site.register(CheckIn, CheckInAdmin)
