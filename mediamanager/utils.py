def get_media_attachment(obj):
	"""
	Utility function for finding Media attachment of model object
	"""
	from django.contrib.contenttypes.models import ContentType
	from media.models import MediaAttachment
	try:
		ctype = ContentType.objects.get_for_model(obj)
	except ContentType.DoesNotExist:
		pass
		return None
	
	try:
		return MediaAttachment.objects.filter(content_type=ctype, object_id=obj.pk)
	except MediaAttachment.DoesNotExist:
		pass;
		
	return None