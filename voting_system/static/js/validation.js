$(document).ready(function() {
	$("#votecode").validate({
		rules: {	//rules specify which fields you want to validate
 			votecode: {
				required: true,
				maxlength: 8
			}
		},
		messages: {
      		votecode: {
        		required: "Please enter your vote code.",
        		maxlength: "Codes shouldn't be more than 8 characters!"
			}
		}
	})
});
