# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

from django.db import models
from django.contrib.auth.models import User


class Team(models.Model):
    '''
    Class representing the team table in the database.
    
    Objects of this class will be used to interact with the
    team table in the database.
    '''
    name = models.TextField(max_length=200)
    # When user creates a team. The team will be assigned a
    # unique id. This unique id will be used to identify
    # the team of a newly signing up user who has been invited
    # by the other user.
    invitation_code = models.UUIDField(
        default=uuid.uuid4, editable=False,
        unique=True, null=True
    )


class I2XUser(models.Model):
    '''
    Class representing the I2XUser table in the database.
    
    This class uses django's `auth` model to store basic
    information like name, email, password etc. Custom field
    such as `verified` is stored in the object of this class.

    objects of this class will be used to interact with the
    I2XUsertable in the database.
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    verified = models.BooleanField(default=False)    
    team = models.ForeignKey(
        Team, on_delete=models.CASCADE, null=True,
        related_name='members'        
    )
