from . import views
from django.urls import path

urlpatterns = [
    path('home/', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.log_out, name='log_out'),
    path('read/', views.read, name='read'),
    path('create/', views.create, name='create'),
    path('update/<int:id>', views.update, name='update'),
    path('delete/<int:id>', views.delete, name='delete'),
    
]


