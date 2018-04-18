# _*_ encoding:utf-8 _*_
from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):

    nick_name = models.CharField(max_length=50, verbose_name=u"昵称", default="")
    birday = models.DateField(verbose_name=u"生日", null=True, blank=True)
    gender = models.CharField(max_length=6, choices=(("male", u"男"), ("female", "女")), default="female")
    id_card = models.CharField(verbose_name=u"身份证", max_length=18, default=u"")

    address = models.CharField(max_length=100, default=u"")
    mobile = models.CharField(max_length=11, null=True, blank=True)
    image = models.ImageField(upload_to="image/%Y/%m",default=u"image/default.png", max_length=100)

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.username


class Card(models.Model):

    card_id = models.CharField(verbose_name=u"卡号", max_length=11, primary_key=True)
    user = models.OneToOneField(UserProfile, verbose_name=u"持卡人", related_name='user')
    balance = models.FloatField(verbose_name=u"余额", default=0)

    class Meta:
        verbose_name = "银行卡"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return u'卡号: {0}'.format(self.card_id)

    def get_balance(self):
        # 获取余额
        return self.balance

# 转账信息表
class TradeInfo(models.Model):
    trade_id = models.CharField(verbose_name=u"交易流水号", max_length=9, default=u"", primary_key=True)
    trade_type = models.CharField(verbose_name=u"交易类型", choices=(("transfer", u"转账"), ("draw", u"取款"), ("deposit", u"存款")), max_length=8)
    trade_amount = models.FloatField(verbose_name=u"交易金额", default=0)

    # 下面外键中引用了card，所以要把card类的定义，放在前面。
    # 或者使用'card'的形式
    from_card = models.ForeignKey(Card, related_name='from_card', verbose_name=u"转出账户")
    to_card = models.ForeignKey(Card, related_name='to_card', verbose_name=u"转入账户")
    trade_time = models.DateTimeField(verbose_name=u"交易时间", default=datetime.now)
    trade_status = models.CharField(verbose_name=u"交易状态", choices=(("success", u"成功"), ("fail", u"失败")), max_length=7)

    class Meta:
        verbose_name = "交易记录"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.trade_id


# 异常交易

class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name=u"验证码")
    email = models.EmailField(max_length=50, verbose_name=u"邮箱")
    send_type = models.CharField(verbose_name=u"验证码类型", choices=(("register",u"注册"),("forget",u"找回密码"), ("update_email",u"修改邮箱")), max_length=30)
    send_time = models.DateTimeField(verbose_name=u"发送时间", default=datetime.now)

    class Meta:
        verbose_name = u"邮箱验证码"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '{0}({1})'.format(self.code, self.email)


class UserMessage(models.Model):
    user = models.IntegerField(default=0,verbose_name=u'接受用户')
    message = models.CharField(max_length=500,verbose_name=u'消息内容')
    has_read = models.BooleanField(default=False,verbose_name=u'是否已读')
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u'发送时间')

    class Meta:
        verbose_name = u'用户消息'
        verbose_name_plural = verbose_name

