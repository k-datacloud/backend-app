from django.urls import path

from .views import *

urlpatterns = [
    path('user/', CreateUserView.as_view(), name='user'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='userdetail'),
    path('edituser/<int:pk>/', UserEditView.as_view(), name='edituser'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('post/', PostView.as_view(), name='post'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='postdetail'),
    path('postlikes/<int:pk>/', PostlikesView.as_view(), name='postlikes'),
    path('search/', SearchView.as_view(), name='search'),
]