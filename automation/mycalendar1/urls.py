"""
 * Version : 1.0
 * Project: Calendar Automation
 * Copyright : Indxx Capital Management
 * Author: Pavan Rajput
 * Created Date: 08-04-2019
 * Modified Date: dd-mm-yyyy
 * Licensed under : Self
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import (handler400, handler403, handler404, handler500)
from django.views.generic.base import TemplateView
from mycalendar import views

urlpatterns = [
	path('index/', views.index, name='index'),
    path('', views.index, name='home'),
    path('addindex/', views.addindex, name='addindex'),
	path('mycalendar/', views.mycalendar, name = 'mycalendar'),
	path('postindex/', views.post_index, name = 'postindex'),
	path('report/', views.report, name = 'report'),
    path('back/', views.back, name = 'back'),
    path('EditIndex/<int:id>', views.edit_index, name = 'EditIndex'),
    path('updateindex/<int:id>', views.update_index, name = 'updateindex'),
    path('DeleteIndex/<int:id>', views.delete_index, name = 'DeleteIndex'),
    path('reportgenerate/', views.report_generate, name = 'reportgenerate'),
	path('ViewIndex/<int:id>', views.view_index, name = 'ViewIndex'),
    path('SearchIndex/', views.search_index, name = 'SearchIndex'),
    path('emailsend/', views.mail_index, name = 'emailsend'),
	path('handler404/', views.error_404_view, name = 'handler404'),
	path('handler500/', views.error_500_view, name = 'handler500'),
	path('export_xlsx/', views.export_index_to_xlsx, name = 'export_xlsx'),

]
