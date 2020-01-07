from django.urls import path

from . import views

urlpatterns = [
    path('', views.upcoming, name='index'),
    path('event/<uuid:event_id>', views.event, name='event'),
    path('date/<str:date>', views.date, name='date'),
    path('venue/<str:slug>', views.venue, name='venue')
]
