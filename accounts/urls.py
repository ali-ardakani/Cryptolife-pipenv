from django.urls import path
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from .views import (
    SignUpView, 
    UserView, 
    UserUpdate,
    )

app_name = "accounts"

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html',
    email_template_name='registration/password_reset_email.html',
    success_url=reverse_lazy('accounts:password_reset_done'),
    ), name='password_reset'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html',
    success_url=reverse_lazy('accounts:password_reset_complete')), name='password_reset_confirm'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('<user_id>/', UserView.as_view(), name="user_view"),
    path('<user_id>/edit/', UserUpdate.as_view(), name='user_update'),
    path('<user_id>/delete_profile_image/', UserUpdate.delete_profile_image, name='delete_profile_image'),
]
