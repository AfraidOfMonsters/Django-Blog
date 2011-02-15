from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.db.models import get_model
from django.http import HttpResponseBadRequest
from django.utils.translation import ugettext as _
from django.shortcuts import get_object_or_404

from mediamanager.models import MediaForm, Media

@csrf_protect
@login_required
def upload_media(request):	
	if request.method == 'POST':
		form = MediaForm(request.POST, request.FILES)
		if form.is_valid():
			m = Media()
			m.upload_media(data=form.cleaned_data, params={'test':'testparam'})
			return redirect(reverse('mediamanager_view', kwargs={'id':m.pk}))
	else:
		form = MediaForm()
		
	data = {
		'form':form,
		'params':{
			'max_width' : request.GET.get('max_width', None),
			'max_height' : request.GET.get('max_height', None),
			'min_width' : request.GET.get('min_width', None),
			'min_height' : request.GET.get('min_height', None),
			'keep_ratio' : request.GET.get('keep_ration', True)
			},
	}
	
	return render_to_response(
		'upload_media.html',
		data,
		context_instance = RequestContext(request),
	)

@login_required
def view_media(request, id):
	
	media = get_object_or_404(Media, pk=id)
	
	return render_to_response(
		'view_media.html',
		{'media':media},
		context_instance = RequestContext(request),
	)