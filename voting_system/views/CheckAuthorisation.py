from voting_system.models import *
#required_roles in the form of a list of tuples. 
#Each tuple has one or more roles.
#To return true, a user must be in at least one of the role in each tuple
#E.G:
#[(role_a,role_b),(role_c),(role_d,role_e)]
#a user with role_a, role_c and role_r would be accepted. 
def CheckAuthorisation(request, require_login=True, required_roles = []):

	if(not require_login):
		return True, None
	else:
		if request.session.has_key('username'):
			username = request.session['username']

			current_user_roles = GetUserRoles(username)
			for role_tuple in required_roles:
				role_match = False
				for role in role_tuple:
					if(role in current_user_roles):
						role_match = True
						break
				if(not role_match):
					return False, ""

			return True, username
		else:
			return False, None

			
def GetUserRoles(username):
	admin = Admin.objects.get(user_name = username)
	roles = [role.name for role in admin.roles.all()]
	
	return roles