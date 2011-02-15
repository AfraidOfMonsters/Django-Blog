from livesettings.models import LiveSetting

l = LiveSetting()

def get_settings(*args):
	if len(args) > 1:
		result = l.get_settings(args)
	else:
		result = l.get_setting(args[0])
	return result