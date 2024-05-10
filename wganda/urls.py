from django.urls import path
from django.contrib import admin

from core import views as core_views
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    path('', core_views.bad_request),
    path('admin/', admin.site.urls),
    path('people/', core_views.PeopleExtendedAPIView.as_view()),
    path('theory/', core_views.TheoryAPIView.as_view()),
    path('orgs/', core_views.OrgsAPIView.as_view()),
]
