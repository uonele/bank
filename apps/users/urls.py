# -*- coding: utf-8 -*-
__author__ = 'bobby'

from django.conf.urls import url, include

from .views import UserinfoView, UploadImageView, UpdatePwdView, SendEmailCodeView, DepositeView
from .views import UpdateEmailView, MymessageView, MyaccountView,TransFerView, WithdrowView

urlpatterns = [
    # 用户信息
    url(r'^info/$', UserinfoView.as_view(), name="user_info"),

    # 用户头像上传
    url(r'^image/upload/$', UploadImageView.as_view(), name="image_upload"),

    # 用户个人中心修改密码
    url(r'^update/pwd/$', UpdatePwdView.as_view(), name="update_pwd"),

    #发送邮箱验证码
    url(r'^sendemail_code/$', SendEmailCodeView.as_view(), name="sendemail_code"),

    #修改邮箱
    url(r'^update_email/$', UpdateEmailView.as_view(), name="update_email"),

    # 我的消息
    url(r'^mymessage/$', MymessageView.as_view(), name="mymessage"),

    # 取款
    url(r'^withdraw/$', WithdrowView.as_view(), name="withdraw"),

    # 存款
    url(r'^deposit/$', DepositeView.as_view(), name="deposit"),

    # 办卡
    url(r'^add_card/$', MymessageView.as_view(), name="add_card"),

    # 交易记录
    url(r'^translation_record/$', MymessageView.as_view(), name="translation_record"),
    # 账户余额
    url(r'^myaccount/$', MyaccountView.as_view(), name="myaccount"),

    # 转账
    url(r'^transfer/$', TransFerView.as_view(), name="transfer"),
]