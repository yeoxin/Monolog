from django.urls import path
from . import views

urlpatterns = [
    path('', views.entry_list, name='entry_list'),  
    path('entry/<int:pk>/', views.entry_detail, name='entry_detail'),
    path('entry/new/', views.entry_create, name='entry_create'),
    path('entry/<int:pk>/edit/', views.entry_update, name='entry_update'),
    path('entry/<int:pk>/delete/', views.entry_delete, name='entry_delete'),
]
