from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework import generics, status
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from .renderer import UserRenderer
import requests
from .models import User


from django.contrib.auth import authenticate
# Create your views here.


class EmailAuth(generics.GenericAPIView):
    renderer_classes = (UserRenderer,)
    permision_classes = (AllowAny,)

    def get(self, request):
        return Response({"msg": "Welcome email"})

# Create your views here.


class LinkedInCodeAPIView(generics.GenericAPIView):
    permision_classes = (AllowAny,)

    def get(self, request):
        code = request.GET.get('code')
        # GET ACCESS TOKEN
        url = f"https://www.linkedin.com/oauth/v2/accessToken?grant_type=authorization_code&code={code}&client_id=8698c10i50m1o1&redirect_uri=http://127.0.0.1:8000/api/linkedin&client_secret=RO8ZGhoQLHce1X07"
        accesstoken = requests.get(url)
        response = accesstoken.json()
        access_token = response.get('access_token', None)

        if access_token is None:
            return Response({"message": 'Invalid token,please retry'}, status=status.HTTP_400_BAD_REQUEST)

        url2 = "https://api.linkedin.com/v2/me?projection=(id,firstName,lastName,emailAddress,profilePicture(displayImage~:playableStreams))"
        headers = {'Authorization': 'Bearer '+access_token}
        profile = requests.get(url2, headers=headers).json()

        url3 = "https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))"
        email_res = requests.get(url3, headers=headers).json()

        user_data = {
            'first_name': profile['firstName']['localized']['en_US'],
            'last_name': profile['lastName']['localized']['en_US'],
            'profilePic': profile['profilePicture']['displayImage~']['elements'][3]['identifiers'][0]['identifier'],
            "email": email_res['elements'][0]['handle~']['emailAddress'],
        }
        email = user_data['email']
        username = user_data['last_name']
        filtered_user_by_email = User.objects.filter(email=email).first()
        if filtered_user_by_email:
            user = authenticate(
                username=filtered_user_by_email.email, password='XXXXXXXX')
            if user is not None:
                return Response({
                    'username': user.username,
                    'email': user.email,
                    'token': user.token})
        else:
            user = {'username': username,
                    'email': email, 'password': 'XXXXXXXX'}

            User.objects.create_user(**user)
            user = User.objects.filter(email=email).first()
            user.is_verified = True
            user.save()
            new_user = authenticate(username=user.email, password="XXXXXXXX")
            return Response({
                'username': new_user.username,
                'email': new_user.email,
                'token': new_user.token})
