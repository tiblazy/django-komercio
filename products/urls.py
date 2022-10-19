from django.urls import path

from rest_framework.authtoken import views

from . import views


urlpatterns = [
    path('', views.ProductView.as_view()),
    path('<pk>/', views.ProductRetrieveView.as_view()),
]
