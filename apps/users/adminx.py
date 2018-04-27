# -*- coding: utf-8 -*-
import xadmin
from xadmin import views

from .models import EmailVerifyRecord
from .models import UserMessage, Card, TradeInfo


class UserMessageAdmin(object):
    list_display = ['user', 'message', 'has_read', 'add_time']
    search_fields = ['user', 'message', 'has_read']
    list_filter = ['user', 'message', 'has_read']


class CardAdmin(object):
    list_display = ['card_id', 'user', 'balance']
    search_fields = ['card_id', 'user', 'balance']
    list_filter = ['card_id', 'user', 'balance']


class TradeInfoAdmin(object):
    list_display = ['trade_id', 'trade_type', 'trade_amount', 'from_user', 'to_user', 'trade_time']
    search_fields = ['trade_id', 'trade_type', 'trade_amount', 'from_user', 'to_user', 'trade_time']
    list_filter = ['trade_id', 'trade_type', 'trade_amount', 'from_user', 'to_user', 'trade_time']


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSetting(object):
    site_title = '个人网上银行管理系统'
    site_footer = '个人网上银行'
    menu_style = 'accordion'


class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type', 'send_time']
    list_filter = ['code', 'email', 'send_type', 'send_time']


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']


xadmin.site.register(TradeInfo, TradeInfoAdmin)
xadmin.site.register(Card, CardAdmin)
xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(views.CommAdminView, GlobalSetting)