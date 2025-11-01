"""
Core abstract models that other apps will inherit from.
These provide common fields like created_at, updated_at, etc.
"""

from django.db import models
from django.utils.text import slugify
import uuid


class TimeStampedModel(models.Model):
    """
    Abstract base model that provides self-updating
    'created_at' and 'updated_at' fields.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # This won't create a database table
        ordering = ['-created_at']  # Newest first by default


class ContentBase(TimeStampedModel):
    """
    Abstract base for content types (prompts, news, blogs, tools).
    Provides common fields like title, slug, body, image, author.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    body = models.TextField()
    image = models.ImageField(
        upload_to='uploads/%Y/%m/',  # Organized by year/month
        null=True,
        blank=True
    )
    author = models.ForeignKey(
        'users.User',  # Reference User model from users app
        on_delete=models.CASCADE,
        related_name='%(class)s_posts'  # Dynamic related name
    )
    is_published = models.BooleanField(default=True)
    views = models.PositiveIntegerField(default=0)

    class Meta:
        abstract = True
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        Override save to auto-generate slug from title if not provided.
        """
        if not self.slug:
            self.slug = slugify(self.title)
            # Ensure uniqueness by appending UUID if slug exists
            original_slug = self.slug
            counter = 1
            while self.__class__.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def increment_views(self):
        """
        Increment view count.
        """
        self.views += 1
        self.save(update_fields=['views'])