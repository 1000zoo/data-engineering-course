from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name="index"),
    path('<int:question_id>/', views.detail, name="detail"),
    path('some_url', views.some_url, name="some_url")
]
