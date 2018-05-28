# -*- coding: utf-8 -*-
from django import forms
from captcha.fields import CaptchaField

from .models import UserProfile, TradeInfo


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True,min_length=6)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=6)
    captcha = CaptchaField(error_messages={"invalid": u'验证码错误'})


class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={"invalid":u"验证码错误"})


class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)


# class UserInfoForm(forms.Form):
#     nick_name = forms.CharField(min_length=5, max_length=50)
#     gender = forms.CharField()
#     birday = forms.DateField()
#     address = forms.CharField()
#     mobile = forms.CharField(min_length=11,max_length=11)
#     id_card = forms.CharField(min_length=18,max_length=18)


class TradeInfoForm(forms.ModelForm):
    class Meta:
        model = TradeInfo
        fields = ['trade_time','trade_type', 'from_user', 'to_user', 'trade_amount']


class UploadImageForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['image']


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nick_name', 'gender', 'birday', 'address', 'mobile','id_card']