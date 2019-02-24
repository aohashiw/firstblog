from django.shortcuts import render,redirect,reverse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from .forms import UserLoginForm,UserRegisterForm,ProfileForm
from .models import Profile
from django.contrib.auth.decorators import login_required
from captcha.models import CaptchaStore
import os,uuid,json
# Create your views here.

def user_login(request):
    if request.method == 'POST':
        uname =request.POST.get('username',None)
        upwd = request.POST.get('password',None)
        user=authenticate(username=uname,password=upwd)
        print('进入POST')
        if user:
            print('验证成功')
            if user.is_active:
                login(request, user)
                print('成功登录')
                return redirect('index')
        else:
            print('失败')
            return render(request, 'userprofile/login.html', {'mess': '用户名密码不正确'})
    elif request.method=='GET':
        login_form = UserLoginForm
        return render(request, 'userprofile/login.html', locals())
    else:
        return render(request, 'userprofile/login.html',locals())
def user_register(request):
    if request.method == "POST":
        print('进入post')
        register_form = UserRegisterForm(data=request.POST)
        print(register_form.is_valid())
        if register_form.is_valid():
            print('表单合法')
            password = register_form.cleaned_data['password2']
            user=register_form.save(commit=False)
            user.set_password(password)
            user.save()
            login(request,user)
            return redirect('index')
        else:
            mess="输入表单有误，请重新输入"
    register_form=UserRegisterForm()
    return render(request, 'userprofile/register.html', locals())

def user_logout(request):
    logout(request)
    return redirect('index')





@login_required(login_url='/userprofile/login/')
def profile_edit(request,id):
    user = User.objects.get(id = id)
    profile = Profile.objects.get(user_id=id)
    if request.method == 'POST':
        if request.user!= user:
            return HttpResponse("权限不足")
        profile_form = ProfileForm(request.POST,request.FILES)
        if profile_form.is_valid():
            profile_cd = profile_form.cleaned_data
            profile.phone = profile_cd['phone']
            profile.bio = profile_cd['bio']
            if 'icon' in request.FILES:

                '''
                img = request.FILES['icon']
                data = request.POST['icon_data']
                if img.size/1024>700:
                    return JsonResponse({"message":"图片尺寸应小于900 X 1200 像素, 请重新上传。",})
                current_icon = profile.icon
                cropped_icon = crop_image(current_icon,img,data,user.id)
                profile.icon = profile_cd['icon']
                profile.icon = cropped_icon
                data = {"result":profile.icon.url,}
                return JsonResponse(data)
                '''
                profile.icon = profile_cd['icon']
                profile.save()
        else:
            return HttpResponse("表单输入有误，请重新输入")

    profile_form = ProfileForm()
    return render(request, 'userprofile/edit.html', locals())





