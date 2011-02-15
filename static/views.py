from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

def index(request):
	
	data = {}
	
	return render_to_response(
		'index.html',
		data,
		context_instance = RequestContext(request),
	)