from django.urls import path
from . import views

urlpatterns = [
    path('login', views.loginPage, name="login"),
    path('register', views.registerPage, name="register"),
    path('logout', views.logoutUser, name="logout"),
    path('', views.home, name="home"),
    path('room/<int:slug>', views.room, name="room"),
    path('profile/<int:slug>', views.userProfile, name="user-profile"),
    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<int:slug>', views.updateRoom, name="update-room"),
    path('delete-room/<int:slug>', views.deleteRoom, name="delete-room"),
    path('delete-comment/<int:slug>', views.deleteComment, name="delete-comment"),
    path('update-user', views.updateUser, name="update-user"),
    path('topics', views.topicsPage, name="topics"),
    path('activities', views.activitiesPage, name="activities"),
    # path('token/', views.CustomTokenObtainPairView.as_view(),
    #      name='token-obtain-pair'),
    # path('token/refresh/', views.TokenRefreshView.as_view(), name='token-refresh'),
]
