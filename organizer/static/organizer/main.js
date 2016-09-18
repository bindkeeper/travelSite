
$(function() {
	$(".btn-share").click(function(){
		
		var url = $(this).attr('href');
		var self = $(this);
		
		$.getJSON(url, function(result){
			
				if (result.success) {
					//$(self).toggleClass('active');
					
					console.log(result.shared);
					$(".shared").html(result.shared);
					
				}
			
		});
		return false;
	});
	
	$(".item-form").on('submit', function(event){
		event.preventDefault();
		var url = $(this).attr("action");
		var self = $(this);
		
		var formData = $( this ).serialize();
		
		$.ajax({
            type        : 'POST', 
            url         : url, 
            data        : formData, 
            dataType    : 'json', 
			encode      : true
        })
		.done(function(data) {
			console.log(data); 
			if ( ! data.success) {
				alert('failed');
			} else {					
				alert('success');	
			}
			sumCalculate();
		});
	});
});