from django.urls import path
from .views import UsersAPIView, LoginAPIView, RandomizerListAPIView
# from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('get-users/', UsersAPIView.as_view(), name='get-users'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('random/', RandomizerListAPIView.as_view(), name='random'),
]