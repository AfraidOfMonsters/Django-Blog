from django.db import models
from django.core.cache import cache
from django.db.models import Manager
from django.contrib import admin

from livesettings.settings import CACHE_TIMEOUT

class SettingDoesNotExist(Exception):	   
	def __init__(self, k):
		self.key = k
		self.args = [self.key]
		
	def __unicode__(self):
		return "Unset setting key, '%s' does not exist" % self.key

class LiveSettingManager(models.Manager):
	def get_value(self, key):
		k = "%s_%s" % (LiveSetting.__name__, key)
		val = cache.get(k)
		if val is None:
			try:
				val = self.get(key__exact=key).value
			except LiveSetting.DoesNotExist:
				raise SettingDoesNotExist(key)
			cache.set(k, val, CACHE_TIMEOUT)
		return val
	
class LiveSetting(models.Model):
	id = models.AutoField(primary_key=True)
	title = models.CharField(max_length=255, blank=False, null=False)
	description = models.TextField(blank=True, null=True)
	key = models.CharField(max_length=100, blank=False, null=False)
	value = models.CharField(max_length=255, blank=True)
 
	objects = LiveSettingManager()
	
	def __unicode__(self):
		return self.key
	
	class Meta(object):
		verbose_name = "Setting"
		verbose_name_plural = "Settings"
"""
	def get_setting(self, k):
		if cache.get(k):
			return cache.get(k)
		else:
			try:
				r = self._default_manager.get(key__exact=k)
			except LiveSetting.DoesNotExist:
				raise SettingDoesNotExist(k)		 
			cache.set(k, r.value, CACHE_TIMEOUT)
			return r.value

	def get_settings(self, keys):
		cache_results = cache.get_many(keys)

		if(len(cache_results) == len(keys)):
			return cache_results
		
		results = self._default_manager.filter(key__in=keys).values('key','value')
		for r in results:
			cache.set(r['key'], r['value'], CACHE_TIMEOUT)
			
		if(len(results) != len(keys)):
			raise SettingDoesNotExist(list(keys))

		return results
		
	def save(self, force_insert=False, force_update=False):
		super(LiveSetting, self).save(force_insert=force_insert, force_update=force_update)
		cache.set(self.key, self.value)
"""
admin.site.register(LiveSetting)