from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework import generics, status
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from allauthdjango.apps.authentication.renderer import UserRenderer
from rest_framework.views import APIView
import requests
from allauthdjango.apps.authentication.models import User
from allauthdjango.apps.authentication.utils import Utils
from django.contrib.auth import authenticate
# Create your views here.


class EmailAuth(generics.GenericAPIView):
    renderer_classes = (UserRenderer,)
    permision_classes = (AllowAny,)

    def get(self, request):
        return Response({"msg": "Welcome email"})


class LinkedInCodeAPIView(generics.GenericAPIView):
    permision_classes = (AllowAny,)

    def get(self, request):
        code = request.GET.get('code')
        # GET ACCESS TOKEN
        url = f"https://www.linkedin.com/oauth/v2/accessToken?grant_type=authorization_code&code={code}&client_id=8698c10i50m1o1&redirect_uri=https://all-auth.herokuapp.com/api/linkedin&client_secret=RO8ZGhoQLHce1X07"
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
        username = Utils.create_username(
            user_data['first_name'], user_data['last_name'])
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
            user.provider = "linkedin"
            user.save()
            new_user = authenticate(username=user.email, password="XXXXXXXX")
            return Response({
                'username': new_user.username,
                'email': new_user.email,
                'token': new_user.token})


class GoogleAuthAPIView(APIView):
    """
    Manage Google Login
    """
    renderer_classes = (UserRenderer,)

    def post(self, request):
        token = request.data.get('access_token', None)
        if token is None:
            return Response({
                "message": "Please provide a token"
            }, status.HTTP_401_UNAUTHORIZED)
        user_info = requests.get(
            "https://oauth2.googleapis.com/tokeninfo?id_token={}".format(token)).json()

        if "error" in str(user_info):
            return Response({"error": "Something went wrong,please try again"}, status.HTTP_401_UNAUTHORIZED)
        user_data = {
            'first_name': user_info['given_name'],
            'last_name': user_info['family_name'],
            'profilePic': user_info['picture'],
            "email": user_info['email'],
        }
        email = user_data['email']
        username = Utils.create_username(
            user_data['first_name'], user_data['last_name'])
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
            user.provider = "google"
            user.save()
            new_user = authenticate(username=user.email, password="XXXXXXXX")
            return Response({
                'username': new_user.username,
                'email': new_user.email,
                'token': new_user.token})


class GithubLoginAPIView(APIView):

    def get(self, request):
        code = request.query_params.get('code')
        access_token = requests.get(
            "https://github.com/login/oauth/access_token?client_id={}&client_secret={}&code={}".format(os.environ.get('GITHUB_CLIENT_ID'),os.environ.get('GITHUB_CLIENT_SECRET'),code)).text
        if not "access_token" in access_token:
            return Response({"github": "something went wrong"}, status.HTTP_400_BAD_REQUEST)

        token = access_token.split('access_token=')[
            1].replace("]", "").split("&scope")[0]
        headers = {
            'Authorization': 'token '+token
        }
        response = requests.get(
            'https://api.github.com/user', headers=headers).json()

        user_data = {
            'first_name': response['name'].split(" ")[0],
            'last_name': response['name'].split(" ")[1],
            'profilePic': response['avatar_url'],
            "email": response['email'],
        }
        email = user_data['email']
        username = Utils.create_username(
            user_data['first_name'], user_data['last_name'])
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
            user.provider = "github"
            user.save()
            new_user = authenticate(username=user.email, password="XXXXXXXX")
            return Response({
                'username': new_user.username,
                'email': new_user.email,
                'token': new_user.token})
