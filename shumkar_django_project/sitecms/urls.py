from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import home, save_lead

urlpatterns = [
    path('', home, name='home'),
    path('request/', save_lead, name='save_lead'),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
