# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.models import User

from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework import status

from accounts.models import I2XUser
from accounts.models import Team
from accounts.serializers import I2XUserSerializer
from accounts.serializers import TeamSerializer


class UserViewSet(viewsets.ModelViewSet):
    '''Views to handle REST API calls on resource `User`.'''
    
    queryset = I2XUser.objects.all()    
    serializer_class = I2XUserSerializer

    def create(self, request):
        '''
        This methods overides the `rest_framework`'s create method
        to create an object of our custom user model I2XUser.
        
        If the data contains an invitation code the new user will be 
        added to the team corresponding to the invitation code.
        Every team has a unique invitation code. Exisiting members of 
        the team can send an invitation link to a potential new user.
        If the user register's using this link the POST body must contain
        the `invitation_code`.
        '''
        serializer = I2XUserSerializer(data=request.data)
        invitation_code = request.data.get('invitation_code')
        
        if not serializer.is_valid():
            return JsonResponse({}, status=status.HTTP_400_BAD_REQUEST)
        
        if invitation_code:
            team = Team.objects.filter(invitation_code=invitation_code).first()
        else:
            team = None
        
        data = serializer.data
        user = User.objects.create_user(
            username=data.get('user').get('username'),
            password=data.get('user').get('password'),
            email=data.get('user').get('email'),
            first_name=data.get('user').get('first_name'),
            last_name=data.get('user').get('last_name')
        )
        I2XUser.objects.create(user=user, team=team, verified=False)
        login(request, user)
        
        return JsonResponse({}, status=status.HTTP_201_CREATED)
        

class TeamViewSet(viewsets.ModelViewSet):
    '''Views to handle REST API calls on resource `Team`.'''
    
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    def create(self, request):
        '''
        This method overrides the `rest_framework`'s create method.
        
        User who is registered and signed in is allowed to create 
        a team only if he not already part of an existing team.
        `user.team` should be `None` for the user.
        '''
        i2x_user = I2XUser.objects.get(user=request.user)

        if i2x_user.team:
            return JsonResponse({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        serializer = TeamSerializer(data=request.data)

        if not serializer.is_valid():
            return JsonResponse({}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        
        return JsonResponse({}, status=status.HTTP_201_CREATED)
    
    
def verify_email(request):
    '''
    This endpoint is used to verify the email.
    
    The verification link can be sent to the user in
    an email. This link must contain `user_id` of the user 
    who is to be verified, in the query params. For example:
    
    https://i2x.ai/api/v1/verify/?user_id=121
    
    This user id will be used to query the correct user and
    verify them.
    '''
    try:
        user_id = int(request.GET['user_id'])
        
    except (ValueError, KeyError):
        return JsonResponse({}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = I2XUser.objects.get(id=user_id)
        user.verified  = True
        user.save()
        
        return JsonResponse({}, status=status.HTTP_200_OK)
    
    except I2XUser.DoesNotExist:
        return JsonResponse({}, status=status.HTTP_404_NOT_FOUND)


def user_login(request):
    '''
    This function logs in user based on the
    username and password provided as patameter 
    in the post request.
    '''
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)

        return JsonResponse({}, status=status.HTTP_200_OK)
        
    else:
        return JsonResponse({}, status=status.HTTP_401_UNAUTHORIZED)

    
def reset_password(request):
    '''
    This view send's an email with the link which includes
    user's id in the query params. For example link must look
    something like:
    
    https://i2x.ai/?user=121213.

    Onlicking on the link in email, user will be directed to the
    i2x.ai website. Javascript on the i2x website must extract the
    user_id and send the POST request to the server at:
    
    api/v1/password/ with json body that contains new password.
    {    
      "new_password": "adf`21fax!",
      "user_id": 13221
    }
    '''
    data = json.loads(request.body)
    email = data.get('email')

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return JsonResponse({}, status=status.HTTP_404_NOT_FOUND)
    
    # Send email using SMTP backend.
    # This needs configuration and needs to setup an SMTP server
    # or using a 3rd party server like Gmail.    
    return JsonResponse({}, status=status.HTTP_200_OK)    
    
    
def password(request):
    '''
    This view handles the request for password reset.

    Given new password and user_id (which was embeded in the link in email)
    this function will update the user's password with the given id.
    
    POST Body Example: {
      'user_id': 1212,
      'new_password': #$@!@!
    }
    '''
    data = json.loads(request.body)
    new_password = data.get('new_password')
    user_id = data.get('user_id')
    
    if not (new_password or user_id):
        return JsonResponse({}, status=status.HTTP_400_BAD_REQUEST)
    try:
        i2x_user = I2XUser.objects.get(id=user_id)
    except I2XUser.DoesNotExist:
        return JsonResponse({}, status=status.HTTP_404_NOT_FOUND)
    
    i2x_user.user.set_password(new_password)
    i2x_user.user.save()
    
    return JsonResponse({}, status=status.HTTP_200_OK)    
