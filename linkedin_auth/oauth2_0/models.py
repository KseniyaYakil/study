from django.db import models

# Create your models here.
class User(models.Model):
	name = models.CharField(max_length = 30, default = 'undef')
	access_token = models.CharField(max_length = 1024)
	expires_in = models.IntegerField(default = 0)

class UserStory(models.Model):
	user_id = models.ForeignKey(User)
	last_seen = models.CharField(max_length = 20)
	log_file = models.CharField(max_length = 1024)
