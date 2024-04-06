from django.contrib import admin
from .models import Tag, Feature, Banner

admin.site.register(Tag)
admin.site.register(Feature)


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'is_active', 'created_at', 'updated_at')
    list_filter = ('tag_ids', 'feature_id',)
    fields = ['tag_ids', 'feature_id', 'content', 'is_active']
