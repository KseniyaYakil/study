from django.shortcuts import render
from django.http import HttpResponse
import config
import httplib2
import json
from urllib import urlencode

uniq_state = 'ASPKT564VG912S0H5V12M4Z09dwaqsgtfcoi';

def show_user_info(request):
	if 'access_token' not in request.session:
		return HttpResponse("Error: no access_token for this session")

	http_manager = httplib2.Http()
	req = '{0}{1}?oauth2_access_token={2}'.format(config.Conf.api_addr,
												  config.Conf.api_people,
												  request.session['access_token'])
	headers, body = http_manager.request(req, 'GET')

	return HttpResponse(body)

def get_auth_code(uniq_state):
		format_str = '''{0}authorization?
						response_type=code
						&client_id={1}
						&scope={2}
						&state={3}
						&redirect_uri={4}'''.format(
						config.Conf.auth_addr,
						config.AppConf.api_key,
						config.Conf.scope,
						uniq_state,
						config.AppConf.redirect_uri)
		return format_str

def get_access_token(request):
	if 'code' not in request.GET:
		raise Http404

	if 'state' in request.GET and uniq_state == request.GET['state']:
		req_params = dict()
		req_params['grant_type'] = 'authorization_code'
		req_params['client_id'] = config.AppConf.api_key
		req_params['code'] = request.GET['code']
		req_params['redirect_uri'] = config.AppConf.redirect_uri
		req_params['client_secret'] = config.AppConf.api_secret

		req_access_token = '{0}accessToken?'.format(config.Conf.auth_addr)
		req_headers = {'Content-type': 'application/x-www-form-urlencoded'}

		http_manager = httplib2.Http()
		headers, body = http_manager.request(req_access_token, 'POST', urlencode(req_params), headers=req_headers)

		recv_answer = json.loads(body)
		if 'access_token' in recv_answer:
			request.session['access_token'] = recv_answer['access_token']
			request.session['access_token_exp_in'] = recv_answer['expires_in']
			return show_user_info(request)
		elif 'error' in recv_answer:
			return HttpResponse('Error: {0}'.format(recv_answer['error_description']))
		else:
			raise Http404
	else:
		return HttpResponse('Error: resieved state differs from app uniq state')

def redirected(request):
	if 'code' in request.GET and 'state' in request.GET:
		return get_access_token(request)
	elif 'error' in request.GET:
		return HttpResponse('Auth in LinkedIn failed: {0}'.format(request.GET['error_descriprion']))
	else:
		raise Http404

def home(request):
	if 'acces_token' in request.session:
		return show_user_info(request)
	else:
		auth_addr = get_auth_code(uniq_state);
		response = '''<p>You are not authorized in LinkedIn.</p>
				      <p>Please, visit
				      <a href="{0}">LinkedIn authorization page</a></p>'''.format(auth_addr);
		return HttpResponse(response);

