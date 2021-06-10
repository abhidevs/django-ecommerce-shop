from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name='BlogHome'),
    path('p/<str:slug>', views.detailedPost, name='detailedPost'),
    path('search/', views.search, name='search'),
    path('login/', views.loginUser, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logoutUser, name='logoutUser'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('addPost/', views.addPost, name='addPost'),
    path('editPost/<str:action>/<str:post_id>', csrf_exempt(views.editPost), name='editPost'),
    path('deletePost/<str:post_id>', views.deletePost, name='deletePost')
]
