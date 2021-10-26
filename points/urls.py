from django.urls import path
from .views import PointView, PointDetailsView

urlpatterns = [
    path('get-points/', PointView.as_view(), name='get-points'),
    path('points-details/<int:id>', PointDetailsView.as_view(), name='points-details'),
]