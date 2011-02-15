from django.template import Library, Node, TemplateSyntaxError
from django.utils.translation import ugettext as _

from livesettings.models import LiveSetting

register = Library()

class GetSettingNode(Node):
	def __init__(self, key):
		self.key = key

	def render(self, context):
		return LiveSetting._default_manager.get_value(self.key)

def do_get_setting(parser, token):
	bits = token.contents.split()
	if len(bits) > 2:
		raise TemplateSyntaxError(_('%s tag requires exactly 1 argument') % bits[0])
	return GetSettingNode(bits[1])

register.tag('setting', do_get_setting)