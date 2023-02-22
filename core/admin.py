from django.contrib import admin
from django.core.exceptions import PermissionDenied

from .models import PeopleExtended


class PeopleExtendedAdmin(admin.ModelAdmin):
    """
    Admin panel for PeopleExtended model
    """
    def save_model(self, request, obj, form, change):
        """
        Disable saving through API or serializer
        """
        if request.resolver_match.url_name != 'admin:myapp_peopleextended_changelist':
            # Prevent saving through API or serializer
            raise PermissionDenied("Editing through API or Serializer is not allowed.")
        else:
            # Allow saving through the admin panel
            super().save_model(request, obj, form, change)

    def has_add_permission(self, request):
        """
        Disable adding new records through the admin panel
        """
        return False

    def has_delete_permission(self, request, obj=None):
        """
        Disable deleting records through the admin panel
        """
        return False


admin.site.register(PeopleExtended, PeopleExtendedAdmin)
