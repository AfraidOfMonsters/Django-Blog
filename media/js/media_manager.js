var uploaded_media_id = false;
var uploaded_media_url = false;

$(document).ready(function() {
	
	var current_window;

	$('.upload-image').click(function(){
		$.fancybox.showActivity();
		current_window = $(this);
		$.fancybox({
			'type':'iframe',
			'href':this.href,
			'onClosed':testFunction
		})
		
		return false;
	});
	
	function testFunction() {
		if(!uploaded_media_id)
			return;
			
		$(current_window).parent().find('input').val(uploaded_media_id);
		$(current_window).parent().find('a').html("<img src=\""+uploaded_media_url+"\" />").fadeIn();
		uploaded_media_id = false;
	}
})