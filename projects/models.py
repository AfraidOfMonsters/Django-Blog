from django.db import models
from django.utils.translation import ugettext as _
from django.contrib import admin
from datetime import datetime

from tagging.fields import TagField
from mediamanager.fields import MediaUploadField

class Project(models.Model):
	LIVE_STATUS = 1
	DRAFT_STATUS = 2
	HIDDEN_STATUS = 3
	STATUS_CHOICES = (
		(LIVE_STATUS, ('Live')),
		(DRAFT_STATUS, ('Draft')),
		(HIDDEN_STATUS, ('Hidden')),
	)

	id = models.AutoField(primary_key=True)
	title = models.CharField(max_length=250)
	slug = models.SlugField(unique=True)
	status = models.IntegerField(choices=STATUS_CHOICES, default=LIVE_STATUS)
	excerpt = models.TextField()
	content = models.TextField()
	image_preview = MediaUploadField(params={'size':500, 'compression':80}, blank=True, null=True)
	image_large = MediaUploadField(params={'size':500, 'compression':80}, blank=True, null=True)
	featured = models.BooleanField()
	date_created = models.DateTimeField(auto_now_add=True)
	date_published = models.DateTimeField(default=datetime.now)
	tags = TagField()

	def __unicode__(self):
		return self.title

	def get_tag_list(self):
		return parse_tag_input(self.tags)		
	
	class Meta(object):
		verbose_name_plural = "Projects"
		ordering = ['-date_published']
		
class ProjectAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('title',),
    }		
admin.site.register(Project, ProjectAdmin)