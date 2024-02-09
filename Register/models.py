from django.db import models
from django.contrib.auth.models import User



class Relation(models.Model):
    from_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='follow')
    to_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='following')
    created = models.TimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.from_user} is following {self.to_user} '



