from . import views
from django.urls import path
from .views import SingupView

app_name = "polls" # 실제 app 이름과 달라도 괜찮다.
urlpatterns = [
    path('', views.index, name="index"),
    path('<int:question_id>/', views.detail, name="detail"),
    path('<int:question_id>/result', views.result, name="result"),
    path('<int:question_id>/vote/', views.vote, name="vote"),
    path('signup/', SingupView.as_view(), name='signup')
]
