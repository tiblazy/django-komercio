from django.urls import path

from rest_framework.authtoken import views

from . import views


urlpatterns = [
    path('', views.AccountView.as_view(), name='accounts'),
    path('newest/<int:num>/', views.AccountListView.as_view()),
    path('<pk>/', views.AccountUpdateView.as_view()),
    path('<pk>/management/', views.ManagerView.as_view()),
]
