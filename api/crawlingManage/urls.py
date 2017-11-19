__author__ = 'toantran'
from django.conf.urls import patterns, url, include
from rest_framework import routers, views, response
from .views import *
from webcrawl.routers import HybridRouter

# We use a single global DRF Router that routes views from all apps in project
router = routers.DefaultRouter()

# app views and viewsets
# router.register(r'testmodelviewset', TestModelViewSet, base_name='testmodelviewset')
# router.register(r'author', AuthorViewSet, r"author")
# router.register(r'book', BookViewSet, r"book")
# router.register(r'user', UserViewSet, r"user")
# router.add_api_view(r'auth', url(r'^auth/$', ObtainAuthToken.as_view(), name=r"auth"))


urlpatterns = patterns('',
                       url(r'^test_asynce/$', 'api.crawlingManage.views.test_asynce'),
                       # url(r'^testmodelviewset/$', TestModelViewSet),


                       )