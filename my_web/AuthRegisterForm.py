from django.contrib.auth.models import User
from django import forms
class AuthRegisterForm(forms.Form):
    error_msg = {
        'username': {'required': '用户名不能为空', 'max_length': '最大20', },
        'password': {'required': '用户密码不能为空', 'max_length': '最大20',},
        'password2': {'required': '确认密码不能为空', 'max_length': '最大20', },
    }
    username = forms.CharField(label='用户名',max_length=20, required=True,
                               error_messages=error_msg['username'],widget=forms.TextInput(attrs={'class': 'form-control input-medium'}))
    password = forms.CharField(label='密码',max_length=20, required=True,
                               error_messages=error_msg['password'],widget=forms.PasswordInput(attrs={'class': 'form-control input-medium'}))
    password2 = forms.CharField(label='确认密码',max_length=20, required=True,
                               error_messages=error_msg['password2'],widget=forms.PasswordInput(attrs={'class': 'form-control input-medium'}))

    # def clean(self):
    #     username = self.cleaned_data.get('username')
    #     pwd = self.cleaned_data.get('password')
    #     pwd2 = self.cleaned_data.get('password2')
    #     self.cleaned_data=self.cleaned_data.pop('password2')
    #     if pwd == pwd2:
    #         return self.cleaned_data
    #     else:
    #         from django.core.exceptions import ValidationError  # 这里异常模块导入要放在函数里面，放到文件开头有时会报错，找不到
    #         raise ValidationError('密码输入不一致')