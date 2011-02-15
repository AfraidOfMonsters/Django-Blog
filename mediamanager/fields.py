"""
Media Fields

Here is a list of accepted params:

size			- double	- resize dimensions
keep_aspect		- boolean	- resize image by maintaining aspect ratio
compression		- number	- compress the image? default 80
crop			- double	- crop coords of the fully uploaded image
"""
from django.utils.translation import ugettext as _
from django.db.models.fields import IntegerField
from django.db.models import SubfieldBase
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from django.core.validators import EMPTY_VALUES
from django.db.models.signals import post_save
			
from forms import MediaUploadFormField
from models import Media

class MediaUploadField(IntegerField):
	#__metaclass__ = SubfieldBase
	
	def __init__(self, params=None, *args, **kwargs):
		self.params = params
		super(MediaUploadField, self).__init__(*args, **kwargs)
	
	def contribute_to_class(self, cls, name):
		super(MediaUploadField, self).contribute_to_class(cls, name)
		setattr(cls, self.name, self)
		post_save.connect(self._save, cls, True)

	def _save(self, **kwargs): #signal, sender, instance):
		instance = kwargs['instance']
		val = getattr(instance, self.attname, None)	
		if val:
			Media.objects.update_attachments(instance, val)
				
	def to_python(self, value):
		if value in EMPTY_VALUES:
			return value
		if isinstance(value, Media):
			return value
		try:
			return Media.objects.get(pk=value)
		except (Media.DoesNotExist):
			return None
		try:
			return int(value)
		except ValueError:
			pass

	def get_prep_value(self, value):
		if isinstance(value, Media):
			value = value.pk
		return super(MediaUploadField, self).get_prep_value(value)
	
	def formfield(self, **kwargs):
		defaults = {'form_class':MediaUploadFormField,'params':self.params}
		defaults.update(kwargs)
		return super(MediaUploadField, self).formfield(**defaults)

"""
	def pre_save(self, model_instance, add):
		value = super(MediaUploadField, self).pre_save(model_instance, add)
		if value and add:
			post_save.connect(self.someCallback, sender=model_instance.__class__, dispatch_uid='media_attachment_signal')
		return value
	
	def someCallback(self, sender, **kwargs):
		# Get media object

		#m = Media.objects.get
		#MediaAttachment.objects.create_attachment(sender)
		post_save.disconnect(self.someCallback, sender=sender, dispatch_uid='media_attachment_signal')
		return
"""
