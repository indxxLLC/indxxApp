#api/views.py
"""
 * Version : 1.0
 * Project: Calendar Automation
 * Copyright : Indxx Capital Management
 * Author: Pavan Rajput
 * Created Date: 08-04-2019
 * Modified Date: dd-mm-yyyy
 * Licensed under : Self
"""
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from rest_framework import status
from rest_framework import generics
from .serializers import CalendarlistSerializer
from .models import Calendarlist
from rest_framework import viewsets


class ApiViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
		
    queryset = Calendarlist.objects.all().order_by('id')
    serializer_class = CalendarlistSerializer
	
	
class CalViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
		
    queryset = Calendarlist.objects.filter(category="Cal").order_by('id')
    serializer_class = CalendarlistSerializer
	
class Cal_AgentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
		
    queryset = Calendarlist.objects.filter(category="Cal_Agent").order_by('id')
    serializer_class = CalendarlistSerializer
	
class Client_Comm_DateViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
		
    queryset = Calendarlist.objects.filter(category="Client_Comm_Date").order_by('id')
    serializer_class = CalendarlistSerializer

class Client_NameViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
		
    queryset = Calendarlist.objects.filter(category="Client_Name").order_by('id')
    serializer_class = CalendarlistSerializer

class Comm_to_Calc_AgentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
		
    queryset = Calendarlist.objects.filter(category="Comm_to_Calc_Agent").order_by('id')
    serializer_class = CalendarlistSerializer

class Comp_DateViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
		
    queryset = Calendarlist.objects.filter(category="Comp_Date").order_by('id')
    serializer_class = CalendarlistSerializer
	
class Contract_TypeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
		
    queryset = Calendarlist.objects.filter(category="Contract_Type").order_by('id')
    serializer_class = CalendarlistSerializer
	
class Effec_DateViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
		
    queryset = Calendarlist.objects.filter(category="Effec_Date").order_by('id')
    serializer_class = CalendarlistSerializer
	
class ETF_LaunchedViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
		
    queryset = Calendarlist.objects.filter(category="ETF_Launched").order_by('id')
    serializer_class = CalendarlistSerializer

class Ind_Cmte_Comm_DateViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
		
    queryset = Calendarlist.objects.filter(category="Ind_Cmte_Comm_Date").order_by('id')
    serializer_class = CalendarlistSerializer
	
class Ind_StyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
		
    queryset = Calendarlist.objects.filter(category="Ind_Sty").order_by('id')
    serializer_class = CalendarlistSerializer
	
class Ind_VerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
		
    queryset = Calendarlist.objects.filter(category="Ind_Ver").order_by('id')
    serializer_class = CalendarlistSerializer
	
class Prelim_Comm_DateViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
		
    queryset = Calendarlist.objects.filter(category="Prelim_Comm_Date").order_by('id')
    serializer_class = CalendarlistSerializer

	
class Prod_StatViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
		
    queryset = Calendarlist.objects.filter(category="Prod_Stat").order_by('id')
    serializer_class = CalendarlistSerializer
	
class Public_Announcement_DateViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
		
    queryset = Calendarlist.objects.filter(category="Public_Announcement_Date").order_by('id')
    serializer_class = CalendarlistSerializer
	
class RebalanceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
		
    queryset = Calendarlist.objects.filter(category="Rebalance").order_by('id')
    serializer_class = CalendarlistSerializer
	
class ReconstitutionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
		
    queryset = Calendarlist.objects.filter(category="Reconstitution").order_by('id')
    serializer_class = CalendarlistSerializer
	
class ReviewViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
		
    queryset = Calendarlist.objects.filter(category="Review").order_by('id')
    serializer_class = CalendarlistSerializer
	
class Selec_Date_Cyc_1ViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
		
    queryset = Calendarlist.objects.filter(category="Selec_Date_Cyc_1").order_by('id')
    serializer_class = CalendarlistSerializer
	
class Selec_Date_Cyc_2ViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
		
    queryset = Calendarlist.objects.filter(category="Selec_Date_Cyc_2").order_by('id')
    serializer_class = CalendarlistSerializer
	
class Theme_ReviewViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
		
    queryset = Calendarlist.objects.filter(category="Theme_Review").order_by('id')
    serializer_class = CalendarlistSerializer
	
class Type_of_IndViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
		
    queryset = Calendarlist.objects.filter(category="Type_of_Ind").order_by('id')
    serializer_class = CalendarlistSerializer
	
class Weights_Share_Freeze_DateViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
		
    queryset = Calendarlist.objects.filter(category="Weights_Share_Freeze_Date").order_by('id')
    serializer_class = CalendarlistSerializer

	
	
	
