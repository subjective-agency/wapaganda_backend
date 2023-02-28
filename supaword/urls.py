from django.urls import path
from django.contrib import admin
from django.views.generic import TemplateView

from core import views as core_views
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html')),
    path('admin/', admin.site.urls),
    path('people/', core_views.PeopleExtendedAPIView.as_view()),
]
urlpatterns += router.urls
