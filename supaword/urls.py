from django.urls import path, include
from django.contrib import admin
from core.views import TripleLangViewSet

from core import views as core_views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('triple_lang', TripleLangViewSet)

urlpatterns = [
    path('', core_views.bad_request),
    path('tl/', include(router.urls)),  # does it makes sense?
    path('admin/', admin.site.urls),
    path('people/', core_views.PeopleExtendedAPIView.as_view()),
    path('theory/', core_views.TheoryAPIView.as_view())
]
