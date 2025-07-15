from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin
from modeltranslation.admin import TranslationAdmin

class PropertyImageInline(admin.TabularInline):
    model = ImageProperty
    extra = 1


admin.site.register(UserProfile)
admin.site.register(Review)
admin.site.register(Booking)


@admin.register(Property)
class PropertyAdmin(TranslationAdmin):
    inlines = [PropertyImageInline]

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

# Register your models here.
