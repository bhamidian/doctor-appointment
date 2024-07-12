from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'score', 'title', 'reservation')
    search_fields = ('title', 'text', 'reservation__id')
    list_filter = ('score',)
    ordering = ('-score',)

    fieldsets = (
        (None, {
            'fields': ('score', 'title', 'text', 'reservation')
        }),
    )


