from django.conf.urls import include
from django.conf.urls import url
from rest_framework import routers

from accounts import views


router = routers.DefaultRouter()
router.register(r'team', views.TeamViewSet)
router.register(r'user', views.UserViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^verify/$', views.verify_email, name='verify'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^password/$', views.password, name='password'),
    url(r'^reset/$', views.reset_password, name='password_reset'),    
]
