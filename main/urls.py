from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password-change/',
         auth_views.PasswordChangeView.as_view(),
         name='password_change'),
    path('password-change/done/',
         auth_views.PasswordChangeDoneView.as_view(),
         name='password_change_done'),
    path('remove/<int:uid>', views.remove, name='remove'),

    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('accounts/login/', views.LoginView.as_view(), name="login"),
    path('personal_area/', views.account, name='personal_area'),
    path('personal_area/update_preferences/', views.update_preferences, name='update_preferences'),
    path('booking/<int:uid>/', views.booking, name="booking"),
    path('stop_booking/<int:uid>/', views.stop_booking, name="stop"),
    path('question/', views.question, name="question"),
    path('question/response/<int:uid>/', views.question_response, name="question_response"),


    path('about', views.index, name='about'),

]
