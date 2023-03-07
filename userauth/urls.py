# django
from rest_framework_simplejwt.views import TokenRefreshView

from django.urls import path

from . import views

urlpatterns = [
    path('registration/', views.UserRegisterationView.as_view(), name='user_register'),
    path('login/', views.UserLoginAPIView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('logout/', views.UserLogoutView.as_view(), name='reset_password')    
]
