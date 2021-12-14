from django.db import models
from django.conf import settings
from django_extensions.db.fields import AutoSlugField
from ckeditor_uploader.fields import RichTextUploadingField
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField


class Content(models.Model):
    # This model is for user posts. User can upload a video or some text.
    title = models.CharField(max_length=255, unique=False)
    slug = AutoSlugField(populate_from=['title'])
    short_description = models.TextField(blank=True)
    text = RichTextUploadingField(blank=True)
    video = models.FileField(upload_to="videos/", blank=True)
    date_created = CreationDateTimeField()
    date_modified = ModificationDateTimeField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Contents"

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('content-detail', kwargs={'slug': self.slug})


class WatchListItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE, blank=True)
    date_created = CreationDateTimeField()

    def __str__(self):
        return str(self.user) + self.content.slug

    class Meta:
        verbose_name_plural = "Watch/read list items"
        constraints = [
            models.UniqueConstraint(fields=['user', 'content'], name='already_in_watchlater')
        ]


class Contact(models.Model):
    #An ordinary contact form
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, unique=False, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    message = models.TextField(blank=True)
    date_created = CreationDateTimeField()

    def __str__(self):
        return self.name + str(self.date_created)

    class Meta:
        verbose_name_plural = "Contact form records"
