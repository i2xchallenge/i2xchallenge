# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.test import Client
from django.urls import reverse

from accounts.models import Team
from accounts.models import I2XUser


class TestTeamApi(TestCase):

    def setUp(self):
        self.client = Client()
        user = User.objects.create(
            username='darthvader',
            email='darth@deathstar.com',
            password="12343",
            first_name='Darth',
            last_name='Vader'
        )
        i2x_user = I2XUser.objects.create(user=user, verified=False)
        self.client.force_login(i2x_user.user)

    def test_create_team(self):
        team_name = 'Darkside'
        response = self.client.post(
            reverse('team-list'),
            json.dumps({'name': team_name}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Team.objects.all().first().name, team_name)


class TestRegisterApi(TestCase):

    def setUp(self):
        self.client = Client()

    def test_register_without_invite(self):
        post_data = json.dumps({
            'user': {
                'username': 'avichal',
                'password': '12345',
                'email': 'a@b.com',
                'first_name': 'a',
                'last_name': 'b'
            },
            'verified': False
        })

        response = self.client.post(
            reverse('i2xuser-list'),
            post_data,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 201)

    def test_register_with_invite(self):
        team = Team.objects.create(name='Darkside')
        post_data = json.dumps({
            'user': {
                'username': 'darthvader',
                'password': '12345',
                'email': 'darth@deathstar.com',
                'first_name': 'Darth',
                'last_name': 'Vader'
            },
            'verified': False,
            'invitation_code': str(team.invitation_code)
        })

        response = self.client.post(
            reverse('i2xuser-list'),
            post_data,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 201)
        # test if user is associated with the correct team
        self.assertEqual(I2XUser.objects.all().first().team, team)


class TestVerifyEmail(TestCase):

    def setUp(self):
        self.client = Client()

    def test_verify_email(self):
        user = User.objects.create(
            username='darthvader',
            email='darth@deathstar.com',
            password="12343",
            first_name='Darth',
            last_name='Vader'
        )
        i2x_user = I2XUser.objects.create(user=user, verified=False)
        response = self.client.get(reverse('verify'), {'user_id': i2x_user.id})

        self.assertEqual(response.status_code, 200)
        self.assertTrue(I2XUser.objects.all().first().verified)


    def test_verify_email_incorrect_id(self):
        # response should be 404 for incorrect user_id
        response = self.client.get(reverse('verify'), {'user_id': 1212312})
        self.assertEqual(response.status_code, 404)


class TestResetPasswordApi(TestCase):

    def setUp(self):
        self.client = Client()

    def test_reset_password(self):
        user = User.objects.create(
            username='darthvader',
            email='darth@deathstar.com',
            password="12343",
            first_name='Darth',
            last_name='Vader'
        )
        i2x_user = I2XUser.objects.create(user=user, verified=False)
        response = self.client.post(
            reverse('password'),
            json.dumps({'user_id': i2x_user.id, 'new_password': 'abcd'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            I2XUser.objects.all().first().user.check_password('abcd')
        )

    def test_reset_password_wrong_id(self):
        # with wrong user id, we should get 404
        response = self.client.post(
            reverse('password'),
            json.dumps({'user_id': 1212, 'new_password': 'abcd'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 404)
