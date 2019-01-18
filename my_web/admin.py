from django.contrib import admin
from my_web import models
# Register your models here.
# 展示
class BBS_admin(admin.ModelAdmin):
    # 添加一个个性签名的字段
    list_display = ('title','summary','author','signature','view_count','create_at') #显示列表
    list_filter = ('create_at',)# 过滤器
    search_fields = ('title','author__user__username')#查找
    def signature(self,obj):
        return obj.author.signature
    signature.short_description = '签名'
# 注册表
admin.site.register(models.BBS,BBS_admin)
admin.site.register(models.Category)
admin.site.register(models.BBS_user)
