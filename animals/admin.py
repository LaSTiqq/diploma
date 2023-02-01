from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import *


class AnimalsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'animal_name',
        'family_name',
        'latin_name',
    )

    list_display_links = ('animal_name',)
    list_filter = ('family_name',)
    list_editable = ('family_name',)
    fields = (
        'animal_name',
        'family_name',
        'latin_name',
        'text',
        'image',
        'get_image',
        'qr_code',
        'prefix',
    )
    readonly_fields = (
        'get_image',
        'qr_code',
    )

    def get_image(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width="75">')
    get_image.short_description = 'Miniatūra'


class FamilyAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
    )
    list_display_links = ('name',)


admin.site.register(Animals, AnimalsAdmin)
admin.site.register(Family, FamilyAdmin)

admin.site.site_title = 'Dzīvnieku pārvaldīšana'
admin.site.site_header = 'Dzīvnieku pārvaldīšana'
