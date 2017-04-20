from django.db import models
import random
import string

class VoterAuth(models.Model):
    id = models.IntegerField(primary_key=True)
    password_hash = models.CharField(max_length=300)
    voter_id = models.CharField(max_length=20)
    election_id = models.CharField(max_length=20)
    
    class Meta:
        db_table = 'voter_auth'
        app_label = 'auth'

'''
    # Did not do encryption!!
    def generate_password():
        # Ref: http://davidsj.co.uk/blog/python-generate-random-password-strings/
        characters = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation
        generated_password = ''.join(random.choice(characters) for _ in range(20))
        # ==============================
        # Encryption should be done here
        # ==============================
        if not VoterAuth.objects.using('voterauth').filter(password_hash = generated_password).exists():
            return generated_password
        else:
            generate_password();


    def save_password(voter_code_id):
        password = VoterAuth.generate_password();
        entry = VoterAuth(id=voter_code_id, voter_code_number=voter_code_id, password_hash = password)
        entry.save(using='voterauth')
'''