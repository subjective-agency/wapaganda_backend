from django.contrib import admin
from django.core.exceptions import PermissionDenied

from .models import People, Photos, PeopleOnPhotos


ENABLE_EDITING = True
ENABLE_ADDING = True
ENABLE_DELETING = True


class PeopleAdmin(admin.ModelAdmin):
    """
    Admin panel for PeopleExtended model
    Note PeopleExtended is a view, not table!
    """
    def save_model(self, request, obj, form, change):
        """
        Disable saving through API or serializer
        """
        if self.has_change_permission(request):
            super().save_model(request, obj, form, change)
        else:
            # Prevent saving through API or serializer
            raise PermissionDenied("Editing through API or Serializer is not allowed.")

    def has_change_permission(self, request, obj=None):
        """
        Enables editing records through the admin panel
        """
        return ENABLE_EDITING

    def has_add_permission(self, request):
        """
        Enables adding new records through the admin panel
        """
        return ENABLE_ADDING

    def has_delete_permission(self, request, obj=None):
        """
        Enables deleting records through the admin panel
        """
        return ENABLE_DELETING


class PhotosAdmin(admin.ModelAdmin):
    """
    Admin panel for Photos model
    """

    list_display = ('id', 'created_at', 'url', 'is_face', 'type')
    list_filter = ('is_face', 'type')

    def save_model(self, request, obj, form, change):
        """
        Disable saving through API or serializer
        """
        if self.has_change_permission(request):
            super().save_model(request, obj, form, change)
        else:
            # Prevent saving through API or serializer
            raise PermissionDenied("Editing through API or Serializer is not allowed.")

    def has_change_permission(self, request, obj=None):
        """
        Enables editing records through the admin panel
        """
        return ENABLE_EDITING

    def has_add_permission(self, request):
        """
        Enables adding new records through the admin panel
        """
        return ENABLE_ADDING

    def has_delete_permission(self, request, obj=None):
        """
        Enables deleting records through the admin panel
        """
        return ENABLE_DELETING


class PeopleOnPhotosAdmin(admin.ModelAdmin):
    """
    Admin panel for PeopleOnPhotos model
    """

    list_display = ('id', 'created_at', 'person', 'photo')
    list_filter = ('person', 'photo')

    def save_model(self, request, obj, form, change):
        """
        Disable saving through API or serializer
        """
        if self.has_change_permission(request):
            super().save_model(request, obj, form, change)
        else:
            # Prevent saving through API or serializer
            raise PermissionDenied("Editing through API or Serializer is not allowed.")

    def has_change_permission(self, request, obj=None):
        """
        Enables editing records through the admin panel
        """
        return ENABLE_EDITING

    def has_add_permission(self, request):
        """
        Enables adding new records through the admin panel
        """
        return ENABLE_ADDING

    def has_delete_permission(self, request, obj=None):
        """
        Enables deleting records through the admin panel
        """
        return ENABLE_DELETING


admin.site.register(People, PeopleAdmin)
admin.site.register(Photos, PhotosAdmin)
admin.site.register(PeopleOnPhotos, PeopleOnPhotosAdmin)
