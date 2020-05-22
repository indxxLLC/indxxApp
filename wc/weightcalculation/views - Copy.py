from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import loader
from django.template.loader import render_to_string
# Create your views here.

def index(request):
	templates = loader.get_template("index.html")
	return HttpResponse(templates.render())
	
def weightcal(request):
	templateName = "index.html"
	context = {
		'indexlist': '',
	}

	return render(request, templateName, context)
