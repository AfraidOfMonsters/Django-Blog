def default_processors(request):
	return {
				'root_url':request.path, 
				'absolute_url':request.build_absolute_uri(),
			}