
$(function() {
$(".btn-share").click(function(){
	
	
	
	var url = $(this).attr('href');
	var self = $(this);
	alert(url);
    $.getJSON(url, function(result){
        $.each(result, function(result) {
			if (result.success) {
				$(self).toggleClass('active');
			}
		});
    });
	return false;
	
});
});