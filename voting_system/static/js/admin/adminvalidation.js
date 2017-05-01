$(document).ready(function() {
	$("#adminLogin").validate({
		rules: {
			username: {
				required: true
			},
			password: {
				required: true
			}
		},
		messages: {
			username: {
				required: "Please fill in the username field"
			},
			password: {
				required: "Please fill in the password field" 
			}
		}
	}),
	$("#adminNewRole").validate({
		rules: {
			name: {
				required: true
			}
		},
		messages: {
			name: {
				required: "Please fill in the name field"
			}
		}
	}),
	$("#adminNewParty").validate({
		rules: {
			name: {
				required: true
			}
		},
		messages: {
			name: {
				required: "Please enter a new party"
			}
		}
	})
	$("#adminNewRegion").validate({
		rules: {
			name: {
				required: true
			}
		},
		messages: {
			name: {
				required: "Please fill in the name field"
			}
		}
	}),
	$("#adminCreate").validate({
		rules: {
			first_name: {
				required: true
			},
			last_name: {
				required: true
			},
			user_name: {
				required: true
			},
			email: {
				email: true,
				required: true
			},
			password: {
				required: true
			},
			repeatPassword: {
				required: true,
				equalTo: "#id_password"
			}, 
			'roles[]': {
				required: true
			}
		},
		messages: {
			first_name: {
				required: "Please enter the first name"
			},
			last_name: {
				required: "Please enter the last name"
			},
			user_name: {
				required: "Please enter the username"
			},
			email: {
				email: "Please enter a valid email",
				required: "Please enter an email address"
			},
			password: {
				required: "Please enter a password"
			},
			repeatPassword: {
				required: "Please confirm the password",
				equalTo: "Your passwords aren't equal!"
			},
			'roles[]': {
				required: "Please select a role"
			}
		}
	}),
	$("#adminNewElection").validate({
		rules: {
			name: {
				required: true
			},
			start_date: {
				required: true
			},
			end_date: {
				required: true
			},
			'regions[]': {
				required: true
			}
		},
		messages: {
			name: {
				required: "Please enter an election title"
			},
			start_date: {
				required: "Please enter a start date"
			},
			end_date: {
				required: "Please enter an end date"
			},
			'regions[]': {
				required: "Please select a region"
			}
		}
	}),
	$("#adminNewCandidate").validate({
		rules: {
			first_name: {
				required: true
			},
			last_name: {
				required: true
			},
			email: {
				required: true,
				email: true
			},
			party_id: {
				required: true
			},
			region_id: {
				required: true
			}
		},
		messages: {
			first_name: {
				required: "Please enter a first name"
			},
			last_name: {
				required: "Please enter a last name"
			},
			email: {
				required: "Please enter an email address",
				email: "Please enter a valid email address"
			},
			party_id: {
				required: "Please select a party"
			},
			region_id: {
				required: "Please select a region"
			}
		}
	})
});

