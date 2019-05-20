from .views import EmailAuth, LinkedInCodeAPIView
from django.urls import path

urlpatterns = [
    path("", EmailAuth.as_view(),name="emailauth"),
    path('linkedin/', LinkedInCodeAPIView.as_view(), name='linkedin'),
]
