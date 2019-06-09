from allauthdjango.apps.authentication.views import EmailAuth, LinkedInCodeAPIView, GoogleAuthAPIView
from django.urls import path

urlpatterns = [
    path("", EmailAuth.as_view(), name="emailauth"),
    path('linkedin/', LinkedInCodeAPIView.as_view(), name='linkedin'),
    path('google/', GoogleAuthAPIView.as_view(), name='google'),
]
