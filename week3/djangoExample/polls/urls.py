from . import views
from django.urls import path

app_name = "polls" # 실제 app 이름과 달라도 괜찮다.
urlpatterns = [
    path('', views.index, name="index"),
    path('<int:question_id>/', views.detail, name="detail"),
    path('some_url', views.some_url, name="some_url")
]
