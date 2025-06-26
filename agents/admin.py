from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'created_by', 'created_at', 'word_count']
    list_filter = ['status', 'created_at', 'created_by']
    search_fields = ['title', 'content', 'original_prompt']
    readonly_fields = ['created_at', 'updated_at', 'word_count']
    
    fieldsets = [
        ('Post Details', {
            'fields': ['title', 'content', 'status']
        }),
        ('Generation Info', {
            'fields': ['original_prompt'],
            'classes': ['collapse']
        }),
        ('Metadata', {
            'fields': ['created_by', 'created_at', 'updated_at'],
            'classes': ['collapse']
        }),
        ('Advanced', {
            'fields': ['conversation_history', 'generation_metadata'],
            'classes': ['collapse']
        })
    ]
    
    def word_count(self, obj):
        return obj.word_count
    word_count.short_description = 'Word Count'
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
