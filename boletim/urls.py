from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.issue_upload, name='issue_upload'),
    path('jornal/<slug:slug>/', views.issue_detail, name='issue_detail'),
]