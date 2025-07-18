from django.urls import path
from . import views
from diary import views as diary_views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('chart/', diary_views.emotion_chart, name='emotion_chart'),
]
