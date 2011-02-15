"""
Media form fields

The media upload field accepts kwargs which dicate how the
uploaded image will be processed. 

Here is a list of accepted arguments:

size			- double	- resize dimensions
keep_aspect		- boolean	- resize image by maintaining aspect ratio
compression		- number	- compress the image? default 80
crop			- double	- crop coords of the fully uploaded image

Field also takes a class name parameter, this will set the class name 
of the insert link. Useful if you want to change it from the default 
which is 'upload-image'.
"""
from django.utils.translation import ugettext as _
from django.forms.widgets import HiddenInput
from django.forms import IntegerField
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.core.validators import EMPTY_VALUES

from settings import MEDIA_URL
from models import Media

import urllib 

class MediaUploadWidget(HiddenInput):
	class Media:
		js = (
				MEDIA_URL + 'js/jquery.js', 
				MEDIA_URL + 'js/jquery.fancybox.js', 
				MEDIA_URL + 'js/media_manager.js'
			)
		css = {'all':(MEDIA_URL + 'css/fancybox.css',)}
			
	def __init__(self, attrs={}, params=None, **kwargs):
		self.class_name = kwargs.get('class_name', 'upload-image')
		self.text = kwargs.get('text', _('Upload Image'))
		if params:
			self.params = '?'+'&'.join([k+'='+urllib.quote(str(v)) for (k,v) in params.items()])
		else:
			self.params = u''	
		super(MediaUploadWidget, self).__init__(attrs)

	def render(self, name, value, attrs=None):
		id = (value.pk if isinstance(value, Media) else None)
		if not id and value not in EMPTY_VALUES:
			try:
				value = Media.objects.get(pk=value)
				id = value.pk
			except Media.DoesNotExist:
				pass
		output = []
		if id: # Show a thumbnail of our file icon
			output.append('<a href="%s"><img src="%s"/></a>' \
			% (reverse('mediamanager_upload')+self.params, value.thumbnail))
			output.append(super(MediaUploadWidget, self).render(name, id, attrs))
		else: 
			output.append('<a href="%s" class="%s">%s</a>' \
			% (reverse('mediamanager_upload')+self.params, self.class_name, self.text))
			output.append(super(MediaUploadWidget, self).render(name, value, attrs))
		return mark_safe(u''.join(output))

## TODO : OVERWRITE VALIDATION TO HAVE MORE IMAGE RELATED ERRORS ##

class MediaUploadFormField(IntegerField):
	def __init__(self, params=None, *args, **kwargs):
		super(MediaUploadFormField, self).__init__(*args, **kwargs)
		for k in kwargs.keys():
			if k not in('class_name', 'text'):
				del kwargs[k]
		self.widget = MediaUploadWidget(params=params, **kwargs)