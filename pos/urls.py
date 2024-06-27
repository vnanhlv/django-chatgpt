from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.pos, name='pos'),
    path('engagements/', views.engagements, name='engagements'),
    path('load_result/', views.date_range_view, name='load_result'),
]