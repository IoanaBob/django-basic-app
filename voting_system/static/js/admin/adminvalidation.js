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
			voting_start_date: {
				required: true
			},
			voting_end_date: {
				required: true
			},
			registration_start_date: {
				required: true 
			},
			registration_end_date: {
				required: true
			},
			region_id: {
				required: true
			}
		},
		messages: {
			name: {
				required: "Please enter an election title"
			},
			voting_start_date: {
				required: "Please select an election start date"
			},
			voting_end_date: {
				required: "Please enter the election's end date"
			},
			registration_start_date: {
				required: "Please select the registration start date"
			},
			registration_end_date: {
				required: "Please enter the registration's end date"
			},
			region_id: {
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

