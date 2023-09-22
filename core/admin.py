from django.contrib import admin
from django.core.exceptions import PermissionDenied

from .models import People, Photos, PeopleOnPhotos


@admin.register(People)
class PeopleAdmin(admin.ModelAdmin):
    """
    Admin panel for PeopleExtended model
    Note PeopleExtended is a view, not table!
    """
    pass


@admin.register(Photos)
class PhotosAdmin(admin.ModelAdmin):
    """
    Admin panel for Photos model
    """
    list_display = ('id', 'created_at', 'url', 'is_face', 'type')
    list_filter = ('is_face', 'type')


@admin.register(PeopleOnPhotos)
class PeopleOnPhotosAdmin(admin.ModelAdmin):
    """
    Admin panel for PeopleOnPhotos model
    """
    list_display = ('id', 'created_at', 'person', 'photo')
    list_filter = ('person', 'photo')
