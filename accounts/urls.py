from django.contrib import admin
from django.urls import path
from accounts import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home,name='home'),
    # path('', views.dashboard,name='dashboard'),
    path('orders/', views.orders,name='orders'),
    path('products/', views.products,name='products'),
    path('customer/<pk>',views.customer,name='customer'),
    path('register/',views.register_page,name='register'),
    path('login/',views.login_page, name='login'),
    path('logout/',views.logoutUser, name='logout'),
    path('user/',views.user_page,name='user_page'),
    path('profile/',views.profile,name='profile'),
    path('password_reset',
         auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'),
         name='password_reset'),

    path('password_reset_sent',
         auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_sent.html'),
         name='password_reset_done'),

    path('password/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_form.html'),
         name='password_reset_confirm'),

    path('password_reset_complete',
         auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
         name='password_reset_complete')


]