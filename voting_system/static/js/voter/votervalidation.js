$(document).ready(function() {
	$("#voterLogin").validate({
		rules: {
			email: {
				required: true,
				email: true
			},
			password: {
				required: true
			}
		},
		messages: {
			email: {
				required: "Please fill in the email field",
				email: "Please enter a valid email address"
			},
			password: {
				required: "Please fill in the password field" 
			}
		}
	}),
	$("#enterVoterID").validate({
		rules: {
			voter_id: {
				required: true
			}
		},
		messages: {
			voter_id: {
				required: "Please fill in the voter ID field"
			}
		}
	}),
	$("#enterVoterCode").validate({
		rules: {
			code: {
				required: true
			}
		},
		messages: {
			code: {
				required: "Please enter your vote code"
			}
		}
	})
	$("#enterPassword").validate({
		rules: {
			password: {
				required: true
			}
		},
		messages: {
			password: {
				required: "Please fill in the password field"
			}
		}
	}),
	$("#create_confirm_password").validate({
		rules: {
			password: {
				required: true,
				minlength: 6
			},
			confirm_password: {
				required: true,
				equalTo: "#password"
			}
		},
		messages: {
			password: {
				required: "Please fill in the password field",
				minlength: "Your password must be at least 6 characters long"
			},
			confirm_password: {
				required: "Please confirm your password",
				equalTo: "Your passwords don't match!"
			}
		}
	})
});