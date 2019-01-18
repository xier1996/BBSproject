from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class BBS(models.Model):
    category = models.ForeignKey('Category')
    title = models.CharField('标题',max_length=64)
    summary = models.CharField('概要',max_length=256,blank=True) # 可以为空
    content = models.TextField()
    author = models.ForeignKey('BBS_user',verbose_name='作者')
    view_count = models.IntegerField('浏览数')
    ranking = models.IntegerField()
    create_at = models.DateTimeField('创建时间',auto_now_add=True)
    create_at.editable = True
    update_at = models.DateTimeField(auto_now_add=True)
    update_at.editable = True
    def __str__(self):
        return self.title
# class Comment(models.Model):
#     pass

class Category(models.Model):# 板块名称
    name = models.CharField(max_length=32,unique=True) # 唯一值
    administrator = models.ForeignKey('BBS_user')
    def __str__(self):
        return self.name
class BBS_user(models.Model):
    user = models.OneToOneField(User)
    signature = models.CharField(max_length=128,default="这个家伙很懒")
    photo = models.ImageField(upload_to='avator',default='default.jpg')
    def __str__(self):
        return self.user.username