from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'core'
urlpatterns = [
    path('',
         TemplateView.as_view(template_name='core/index.html'),
         name='index'),
    path('api/agreements',
         views.AgreementApi.as_view(),
         name='Agreements'),
    path('api/agreements/calendar',
         views.CalendarApi.as_view(),
         name='Calendar'),
]
