from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('hello-viewset', views.HelloViewSet, basename='viewset')

urlpatterns = [
    path('hello-view/', views.HelloAPIView.as_view()),
    path('', include(router.urls)),
]