from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Post(models.Model):
    """Model for storing generated social media post drafts"""
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    title = models.CharField(max_length=200, help_text="Brief title for this post")
    content = models.TextField(help_text="The generated social media content")
    original_prompt = models.TextField(help_text="The original user prompt that generated this content")
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Generation details
    conversation_history = models.JSONField(
        null=True, 
        blank=True, 
        help_text="Full conversation history from the generation process"
    )
    generation_metadata = models.JSONField(
        null=True, 
        blank=True, 
        help_text="Additional metadata about the generation process"
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Post Draft"
        verbose_name_plural = "Post Drafts"
    
    def __str__(self):
        return f"{self.title} ({self.status}) - {self.created_at.strftime('%Y-%m-%d')}"
    
    @property
    def content_preview(self):
        """Return a truncated version of the content for display"""
        if len(self.content) > 100:
            return self.content[:100] + "..."
        return self.content
    
    @property
    def word_count(self):
        """Return the word count of the content"""
        return len(self.content.split())
    
    def mark_as_published(self):
        """Mark the post as published"""
        self.status = 'published'
        self.save()
    
    def mark_as_archived(self):
        """Mark the post as archived"""
        self.status = 'archived'
        self.save()
    
    @property
    def status_css_class(self):
        """Return the CSS class for the post status badge"""
        status_classes = {
            'draft': 'bg-warning',
            'published': 'bg-success',
            'archived': 'bg-secondary',
        }
        return status_classes.get(self.status, 'bg-secondary')
