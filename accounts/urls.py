from django.urls import path

from accounts.views import (
    RegisterView, LoginView, ForgotPasswordView,
    ChangePasswordView, RestorePasswordView, VerifyEmailView,
    ResendVerifyEmailView, RetrieveUpdateProfileView,
    RetrieveUpdateDestroyProfilePicView, LogoutView, RefreshTokenView
)

urlpatterns = [
    # endpoints which doesn't require authentication
    path('register/', RegisterView.as_view(), name='register_user'),
    path('verify-email/<str:token>/', VerifyEmailView.as_view(), name='verify_user_email'),
    path('resend-verify-email/', ResendVerifyEmailView.as_view(), name='resend_verify_user_email'),
    path('login/', LoginView.as_view(), name='token_obtain_pair'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('restore-password/<int:uid>/<str:token>/', RestorePasswordView.as_view(), name='restore_password'),

    # endpoints which requires authentication
    path('token/', RefreshTokenView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout_user'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('profile/', RetrieveUpdateProfileView.as_view(), name='retrieve_update_profile'),
    path('profile-pic/', RetrieveUpdateDestroyProfilePicView.as_view(), name='retrieve_update_remove_profile_pic'),
]
