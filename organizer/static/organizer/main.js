
$(function() {
	$("#compare").click(function(e) {
		e.preventDefault(); 
		alert("compare clicked");
	});
	
	
	$(".btn-share").click(function(){
		
		var url = $(this).attr('href');
		var self = $(this);
		
		$.getJSON(url, function(result){
			
				if (result.success) {
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

function addTripsToURL(element)
{
    $(element).attr('href', function() {
		var checked_trips = [];
		$(".trip").each(function (index) {
			var checkbox = $( this ).find('.check_for_compare');
			if(checkbox[0].checked) {
				var id = $( this ).children('.trip_id').val();
				checked_trips.push(id);
			}
		});
        return this.href+"?trips="+checked_trips;
    });
}