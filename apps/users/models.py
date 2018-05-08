# _*_ encoding:utf-8 _*_
from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


class UserMessage(models.Model):
    user = models.IntegerField(default=0,verbose_name=u'接受用户')
    message = models.CharField(max_length=500,verbose_name=u'消息内容')
    has_read = models.BooleanField(default=False,verbose_name=u'是否已读')
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u'发送时间')

    class Meta:
        verbose_name = u'用户消息'
        verbose_name_plural = verbose_name


class UserProfile(AbstractUser):

    nick_name = models.CharField(max_length=50, verbose_name=u"昵称", default="")
    birday = models.DateField(verbose_name=u"生日", null=True, blank=True)
    gender = models.CharField(verbose_name=u"性别", max_length=6, choices=(("male", u"男"), ("female", "女")), default="female")
    id_card = models.CharField(verbose_name=u"身份证", max_length=18, default=u"")

    address = models.CharField(verbose_name=u"通讯地址", max_length=100, default=u"")
    mobile = models.CharField(verbose_name=u"手机号码", max_length=11, null=True, blank=True)
    image = models.ImageField(verbose_name=u"头像存储位置", upload_to="image/%Y/%m",default=u"image/default.png", max_length=100)

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.email

    def unread_nums(self):
        #获取用户未读消息的数量
        return UserMessage.objects.filter(user=self.id, has_read=False).count()


class Card(models.Model):

    card_id = models.AutoField(verbose_name=u"卡号", primary_key=True)
    user = models.OneToOneField(UserProfile, verbose_name=u"持卡人", related_name='card')
    balance = models.FloatField(verbose_name=u"余额", default=0)
    class Meta:
        verbose_name = "银行卡"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return u'卡号: {0}'.format(self.card_id)

    def get_balance(self):
        # 获取余额
        return self.balance


class TradeInfo(models.Model):

    """
    AutoField 为int 自增列，必须填入参数 primary_key=True
    BigAutoField(AutoField)
        bigint自增列，必须填入参数 primary_key=True
    """

    trade_id = models.AutoField(verbose_name=u"交易流水号", primary_key=True)
    trade_type = models.CharField(verbose_name=u"交易类型", max_length=8)
    trade_amount = models.FloatField(verbose_name=u"交易金额", default=0)

    # 下面外键中引用了card，所以要把card类的定义，放在前面。
    # 或者使用'card'的形式
    from_user = models.ForeignKey(UserProfile, related_name='from_user', verbose_name=u"转出用户", null=True, blank=True)
    to_user = models.ForeignKey(UserProfile, related_name='to_user', verbose_name=u"转入用户", null=True, blank=True)
    trade_time = models.DateTimeField(verbose_name=u"交易时间", default=datetime.now)

    class Meta:
        verbose_name = "交易记录"
        verbose_name_plural = verbose_name

    # def __unicode__(self):
    #     return self.trade_id


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


class Banner(models.Model):
    title = models.CharField(max_length=100, verbose_name=u"标题")
    image = models.ImageField(upload_to="banner/%Y/%m", verbose_name=u"轮播图", max_length=100)
    url = models.URLField(max_length=200, verbose_name=u"访问地址")
    index = models.IntegerField(default=100, verbose_name=u"顺序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"轮播图"
        verbose_name_plural = verbose_name

