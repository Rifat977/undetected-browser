from core import views
from django.urls import path

app_name = "core"

urlpatterns = [
    path('', views.index, name="index"),
    path('dashboard/', views.profiles, name="profiles"),
    path('stop_browser/<str:browser_name>/', views.stop_browser, name='stop_browser'),
]
