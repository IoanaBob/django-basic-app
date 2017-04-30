$(document).ready(function() {
	$("#candidateInfo").validate({
		rules: {	
 			cname: {
				required: true,
			},
			cparty: {
				required: true,
			},
			cmanifesto: {
				required: true,
			},
			caddress: {
				required: true,
			},
			cDOB: {
				required: true,
			},
			cemail: {
				required: true,
				email: true,
			},	
			cnumber: {
				required: true,
			}
		},
		messages: {
      		cname: {
				required: "Please enter the name of the candidate"
			},
			cparty: {
				required: "Please enter the name of the candidate"
			},
			cmanifesto: {
				required: "Please enter the name of the candidate"
			},
			caddress: {
				required: "Please enter the name of the candidate"
			},
			cDOB: {
				required: "Please enter the name of the candidate"
			},
			cemail: {
				required: "Please enter the name of the candidate",
				email: "Please enter a valid email address"
			},
			cnumber: {
				required: "Please enter the name of the candidate"
			}
		}
	}),
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
	})
});



