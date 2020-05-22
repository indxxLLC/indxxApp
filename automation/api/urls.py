# api/urls.py
"""
 * Version : 1.0
 * Project: Calendar Automation
 * Copyright : Indxx Capital Management
 * Author: Pavan Rajput
 * Created Date: 08-04-2019
 * Modified Date: dd-mm-yyyy
 * Licensed under : Self
"""
from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns
#from .views import CreateView
#from django.conf import settings

from api.views import ApiViewSet, api_root
from rest_framework import renderers
'''
urlpatterns = {
    url(r'^calendarlists/$', CreateView.as_view(), name="create"),
}
'''

from . import views

urlpatterns = format_suffix_patterns([
    path('', api_root),
    path('snippets/', snippet_list, name='snippet-list'),
])

#urlpatterns = format_suffix_patterns(urlpatterns)