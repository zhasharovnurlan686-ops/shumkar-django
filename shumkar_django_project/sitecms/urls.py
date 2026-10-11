from django.urls import path
from .views import home, save_lead

urlpatterns = [
    path('', home, name='home'),
    path('request/', save_lead, name='save_lead'),
]