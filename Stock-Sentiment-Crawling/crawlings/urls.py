from django.urls import path
from . import views

app_name = 'crawlings'

urlpatterns = [
    # 1. 검색을 처리하는 기본 URL
    path('', views.index, name='index'),
    # 2. 검색 결과를 보여주는 URL (redirect의 목적지)
    path('<str:company_name>/', views.index_result, name='index_result'),
    path('delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
]