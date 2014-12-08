from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader

# Create your views here.
def oauth20(request):
	str = 'This is auth20 page for auth in LinkedIn';
	template = loader.get_template('oauth2_0/index.html');
	context = RequestContext(request, {
        	'info_str': str,
		'button_name': 'authorise'
    	})
	return HttpResponse(template.render(context));

def connections(request):
	Response = 'there will be a list of connections'
	return HttpResponse(Response);

def connect_info(request, conn_id):
	Page = "<title>Connect info</title>" + "connect_id = " + conn_id
	return HttpResponse(Page);
