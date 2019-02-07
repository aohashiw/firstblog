from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Profile(models.Model):
    # 与User模型一对一
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    # 电话
    phone = models.CharField(max_length=20,blank=True)
    # 头像
    icon = models.ImageField(upload_to='icon/%Y%m%d/',blank=True)
    # 个人简介
    bio = models.TextField(max_length=500,blank=True)

    def __str__(self):
        return 'user{}'.format(self.user.username)

@receiver(post_save,sender=User)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save,sender=User)
def save_user_profile(sender,instance,**kwargs):
    instance.profile.save()
