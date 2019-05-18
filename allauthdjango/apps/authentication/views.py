from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.response import Response
from .renderer import UserRenderer
# Create your views here.


class EmailAuth(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserRenderer,)

    def get(self, request):
        return Response({"msg": "Welcome email"})
