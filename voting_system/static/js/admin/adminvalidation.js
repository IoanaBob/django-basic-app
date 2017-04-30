$(document).ready(function() {
	console.log("doisdf");
	$("#adminLogin").validate({
		rules: {
			id_username: {
				required: true
			},
			id_password: {
				required: true
			}
		},
		messages: {
			id_username: {
				required: "Please fill in the username field"
			},
			id_password: {
				required: "Please fill in the password field" 
			}
		}
<<<<<<< HEAD
	})
});



=======
	});
});
>>>>>>> 56b688e0613cb5d188c3f2e7d7ae5142808e06d2
