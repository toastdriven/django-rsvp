from django.contrib import admin
from rsvp.models import Event, Guest


# TODO: Fix the inline form to remove metadata fields.
# class GuestInline(admin.TabularInline):
#     model = Guest
#     extra = 3


class EventAdmin(admin.ModelAdmin):
    date_hiearchy = 'date_of_event'
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'description', 'date_of_event'),
        }),
        ('Email', {
            'fields': ('email_subject', 'email_message'),
        }),
        ('Event Details', {
            'fields': ('hosted_by', 'street_address', 'city', 'state', 'zip_code', 'telephone'),
            'classes': ('collapse',)
        })
    )
    # inlines = [GuestInline]
    list_display = ('title', 'date_of_event')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'description', 'hosted_by')


class GuestAdmin(admin.ModelAdmin):
    fields = ('event', 'email', 'name', 'attending_status', 'number_of_guests', 'comment')
    list_display = ('email', 'name', 'attending_status', 'number_of_guests')
    list_filter = ('attending_status',)
    search_fields = ('email', 'name')


admin.site.register(Event, EventAdmin)
admin.site.register(Guest, GuestAdmin)
