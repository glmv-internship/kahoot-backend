from django.urls import path
from core.views import UserCreate, UserDetail
urlpatterns = [
    path('users/', UserCreate.as_view(), name='user_create'),
    path('users/<int:uid>/', UserDetail.as_view(), name='user_detail'),
]
