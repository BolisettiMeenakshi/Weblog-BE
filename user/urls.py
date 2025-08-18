from django.urls import path
from . import views
from.views import UserListCreate, UserDetail
#from rest_framework_simplejwt.views import (
    #TokenObtainPairView,
    #TokenRefreshView,
#)

#urlpatterns = [
   #path('login/', views.login, name='login'),
    #path('register/', views.register, name='register'),
    #path('verify/', views.verify, name='verify'),
    #path('logout/', views.logout, name='logout'),
#]


urlpatterns = [
    path('', UserListCreate.as_view(), name = 'user-list'),
    path('<int:pk>/', UserDetail.as_view(), name = 'user-detail'),
]

