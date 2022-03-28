from django.urls import path

# from django.contrib.auth import views as auth_views

from . import views



urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),

    path('', views.home, name='home'),
    path('user/', views.userPage, name='user-page'), 

    path('account/', views.accountSettings, name='account'), 
    
    path('customer/<str:pk_key>/', views.customer, name='customer'),
    path('products/', views.products, name='product'),

    path('create_order/<str:pk_key>/',views.createOrder, name='create_order'),
    path('update_order/<str:pk_key>/',views.updateOrder, name='update_order'),
    path('delete_order/<str:pk_key>/',views.deleteOrder, name='delete_order'),

    # reset password 

    # path('reset_password/', auth_views.PasswordResetView.as_view(), name='password_reset' ),
    # path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
] 