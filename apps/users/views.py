# _*_ encoding:utf-8 _*_
import re
import json
import datetime

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


from .models import UserProfile, EmailVerifyRecord,UserMessage,Card,TradeInfo
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm, UploadImageForm
from .forms import UserInfoForm,TradeInfoForm
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin


class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class ActiveUserView(View):

    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, "register.html", {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email", "")
            if UserProfile.objects.filter(email=user_name):
                return render(request, "register.html", {"register_form":register_form, "msg": "用户已经存在"})
            pass_word = request.POST.get("password", "")
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            user_profile.password = make_password(pass_word)
            user_profile.save()

            #写入欢迎注册消息
            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = "欢迎注册慕学在线网"
            user_message.save()
            send_register_email(user_name, "register")
            return render(request, "login.html")
        else:
            return render(request, "register.html", {"register_form":register_form})


class LogoutView(View):
    """
    用户登出
    """
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("index"))


class LoginView(View):
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse("index"))
                else:
                    return render(request, "login.html", {"msg": "用户未激活！"})
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误！"})
        else:
            return render(request, "login.html", {"login_form": login_form})


class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, "forgetpwd.html", {"forget_form": forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email", "")
            send_register_email(email, "forget")
            return render(request, "send_success.html")
        else:
            return render(request, "forgetpwd.html", {"forget_form":forget_form})


class ResetView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, "password_reset.html", {"email":email})
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")


class ModifyPwdView(View):
    """
    修改用户密码
    """
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            email = request.POST.get("email", "")
            if pwd1 != pwd2:
                return render(request, "password_reset.html", {"email":email, "msg":"密码不一致"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()

            #写入修改密码的消息
            user_message = UserMessage()
            user_message.user = UserProfile.objects.get(email=email).id
            user_message.message = "修改了密码"
            user_message.save()
            return render(request, "login.html")
        else:
            email = request.POST.get("email", "")
            return render(request, "password_reset.html", {"email":email, "modify_form":modify_form})


class UserinfoView(LoginRequiredMixin, View):
    """
    用户个人信息
    """
    def get(self, request):
        return render(request, 'usercenter-info.html', {})

    def post(self, request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')


class UploadImageView(LoginRequiredMixin, View):
    """
    用户修改头像
    """
    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')


class UpdatePwdView(View):
    """
    个人中心修改用户密码
    """
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail","msg":"密码不一致"}', content_type='application/json')
            user = request.user
            user.password = make_password(pwd2)
            user.save()

            user_message = UserMessage()
            user_message.user = request.user.id
            user_message.message = "在个人中心修改了密码"
            user_message.save()

            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


class SendEmailCodeView(LoginRequiredMixin, View):
    """
    发送邮箱验证码
    """
    def get(self, request):
        email = request.GET.get('email', '')

        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已经存在"}', content_type='application/json')
        send_register_email(email, "update_email")

        return HttpResponse('{"status":"success"}', content_type='application/json')


class UpdateEmailView(LoginRequiredMixin, View):
    """
    修改个人邮箱
    """
    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')

        existed_records = EmailVerifyRecord.objects.filter(email=email, code=code, send_type='update_email')
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码出错"}', content_type='application/json')


class MyaccountView(LoginRequiredMixin, View):
    """
    我的账户余额
    """
    def get(self, request):
        user_temp = request.user
        if hasattr(user_temp,'user'):
            card = Card.objects.get(card_id=user_temp.user.card_id)
            has_card = True
            return render(request, 'usercenter-account.html', {'card':card, 'has_card': has_card})
        else:
            message = "哥，办个卡吧"
            has_card = False
            return render(request, 'usercenter-account.html', {'message' : message, 'has_card': has_card})


class MymessageView(LoginRequiredMixin, View):
    """
    我的消息
    """
    def get(self, request):
        all_messages = UserMessage.objects.filter(user=request.user.id).order_by('-add_time')

        #用户进入个人消息后清空未读消息的记录
        all_unread_messages = UserMessage.objects.filter(user=request.user.id, has_read=False)
        for unread_message in all_unread_messages:
            unread_message.has_read = True
            unread_message.save()

        #对个人消息进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_messages, 5, request=request)

        messages = p.page(page)
        return render(request, 'usercenter-message.html', {
            "messages":messages
        })


class TransFerView(LoginRequiredMixin, View):
    """
    用户转账
    """
    def get(self, request):
        user_temp = request.user
        if hasattr(user_temp, 'user'):  # 判断是否有卡，有的话，则UserProfile的对象就会有user这个属性
            card = Card.objects.get(card_id=user_temp.user.card_id)
            has_card = True
            return render(request, 'usercenter-transfer.html', {'card':card, 'has_card': has_card})
        else:
            message = "哥，办个卡吧"
            has_card = False
            return render(request, 'usercenter-transfer.html', {'message': message,
                                                                'has_card': has_card})

    def post(self, request):
        user_temp = request.user
        message = ""

        from_cardid = request.POST.get("from_cardid")  # 需要校验
        to_cardid = request.POST.get("to_cardid")       # 需要校验
        trade_amount = request.POST.get("trade_amount") # 需要校验
        balance = request.POST.get("balance")

        # 校验卡号
        card_out = Card.objects.get(card_id=from_cardid)
        cards_in = Card.objects.filter(card_id=to_cardid)
        if cards_in :
            exist_card = True
        else:
            exist_card = False

        pattern = re.compile(r'^([1-9]\d{0,9}|0)([.]?|(\.\d{1,2})?)$')
        match = pattern.match(trade_amount.encode("utf-8"))
        if match:
            if float(trade_amount.encode("utf-8")) < float(balance.encode("utf-8")):
                balance_error_info = ""
                amount_status = True
            else:
                balance_error_info = "余额不足"
                amount_status = False
        else:
            balance_error_info = "金额只能是数字，且不能小于零"
            amount_status = False

        if exist_card :
            if amount_status:
                user_tradeinfo = TradeInfo()
                user_tradeinfo.trade_type = "transfer"
                user_tradeinfo.from_card_id = user_temp.user.card_id
                user_tradeinfo.trade_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 现在
                user_tradeinfo.trade_amount = trade_amount
                user_tradeinfo.to_card_id = to_cardid
                user_tradeinfo.save()

                card_out.balance -= float(trade_amount.encode("utf-8"))
                card_out.save()
                cards_in[0].balance += float(trade_amount.encode("utf-8"))
                cards_in[0].save()

                user_message = UserMessage()
                user_message.user = request.user.id
                user_message.message = "向卡号 "+to_cardid+"转账 "+  trade_amount+"元"
                user_message.save()
                has_card = True
                return render(request, 'usercenter-account.html', {'card' : card_out, 'has_card': has_card})
            else:
                card = Card.objects.get(card_id=user_temp.user.card_id)
                return render(request, 'usercenter-transfer.html', {'message': message, 'card': card, 'has_card': True,
                                                                    'balance_error_info': balance_error_info})
        else:
            card = Card.objects.get(card_id=user_temp.user.card_id)
            message = "卡号"+to_cardid + "不存在"
            return render(request, 'usercenter-transfer.html', {'message':message,'card':card, 'has_card': True,
                                                                'balance_error_info':balance_error_info})


def page_not_found(request):

    # 全局404处理函数
    from django.shortcuts import render_to_response
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


def page_error(request):

    # 全局500处理函数
    from django.shortcuts import render_to_response
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response