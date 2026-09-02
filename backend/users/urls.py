from django.urls import path
from .views import RegisterView, CompleteProfileView, GoogleAuthView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('complete-profile/', CompleteProfileView.as_view(), name='complete-profile'),
    path('google-auth/', GoogleAuthView.as_view(), name='google-auth'),
]