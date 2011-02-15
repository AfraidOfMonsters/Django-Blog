from django.db import models
from django.contrib import admin
from django.forms import ModelForm
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_delete, post_save
from django.utils.translation import ugettext as _

from settings import MEDIA_THUMBNAIL_SIZES

class MediaManager(models.Manager):
	def get_for_object(self, obj):
		ctype = ContentType.objects.get_for_model(obj)
		return self.filter(items__content_type__pk=ctype.pk,
						   items__object_id=obj.pk)
		
	def update_attachments(self, obj, media):
		ctype = ContentType.objects.get_for_model(obj)
		MediaAttachment._default_manager.get_or_create(media=media, content_type=ctype, object_id=obj.pk)
		
class Media(models.Model):
	"""
	Media model - Represents images, music, video etc
	"""
	id = models.AutoField(primary_key=True)
	file = models.FileField(upload_to='uploads/%m-%Y/')
	title = models.CharField(max_length=100, blank=True, null=True)
	alt = models.CharField(max_length=100, blank=True, null=True)
	caption = models.CharField(max_length=100, blank=True, null=True)
	desciption = models.TextField(blank=True)
	content_type = models.CharField(max_length=100, blank=False, null=False)
	created = models.DateTimeField(auto_now_add=True, editable=False)
	
	objects = MediaManager()

	def __unicode__(self):
		return u'%s' % self.id
		
	class Meta(object):
		verbose_name_plural = "Media"
		ordering = ['-created']
		
	def upload_media(self, data, params=None):
		self.file = data['file']
		self.content_type = data['file'].content_type
		return self.save()
		
	@property
	def thumbnail(self):
		#print u'%s_%sx%s.%s' % (self.file.path, '100', '100', 'jpg')
		return self.file.url

## MEDIA ATTACHMENTS ##
class MediaAttachmentManager(models.Manager):	
	def create_attachment(self, instance, obj):
		ctype = ContentType.objects.get_for_model(instance)
		self.create(media=instance, object=obj) 
	def delete_attachment(self, instance, *args, **kwargs):
		ctype = ContentType.objects.get_for_model(instance)
		return self.filter(content_type=ctype, object_id=instance.pk).delete()
			
class MediaAttachment(models.Model):
	"""
	Media Attachment - Attaches media to a specific piece of content
	
	Taxonomy can be used to very losely categorise attachments.
	"""
	media = models.ForeignKey(Media, verbose_name=_('attachments'), related_name='items')
	content_type = models.ForeignKey(ContentType)
	object_id = models.PositiveIntegerField(_('object id'), db_index=True)
	object = generic.GenericForeignKey('content_type', 'object_id')
	
	objects = MediaAttachmentManager()
	
	def __unicode__(self):
		return u'%s [%s]' % (self.object, self.media)

	class Meta:
		unique_together = (('media', 'content_type', 'object_id'),)

## SIGNALS AND METHODS ##
post_delete.connect(MediaAttachment.objects.delete_attachment)

## FORMS ##		
class MediaForm(ModelForm):
	class Meta:
		model = Media
		exclude = ('content_type')
		## Do so file type validation here, specify valid extensions in settings etc
		
admin.site.register(Media)