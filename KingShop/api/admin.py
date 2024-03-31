from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from main.models import ReturnProduct


class ReturnProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'price', 'confirmed', 'confirm_button']

    def confirm_button(self, obj):
        url = reverse('confirm')
        return format_html('<a class="button" href="{}">Confirm All Returns</a>', url)

    confirm_button.short_description = 'Confirm All Returns'


admin.site.register(ReturnProduct, ReturnProductAdmin)
