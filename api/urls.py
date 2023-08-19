from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomUserDetailView, CustomUserListCreateView

app_name = 'api'

router = DefaultRouter()


urlpatterns = [
    path('users/', CustomUserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', CustomUserDetailView.as_view(), name='user-detail'),
]
