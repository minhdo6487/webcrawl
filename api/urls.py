from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       # url(r'', include('api.golfcourseeventMana.urls')),
                       # url(r'', include('api.teetimeMana.urls')),
                       # url(r'', include('api.bookingMana.urls')),
                       # url(r'', include('api.gameMana.urls')),
                       # url(r'', include('api.golfcourseMana.urls')),
                       # url(r'', include('api.postMana.urls')),
                       # url(r'', include('api.likeMana.urls')),
                        url(r'', include('api.crawlingManage.urls')),
                       )

