from .views import EmailAuth
from django.urls import path
urlpatterns = [
    path("", EmailAuth.as_view())
]
