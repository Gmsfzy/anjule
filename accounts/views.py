from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import User
from community.models import Community


# 登录视图
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f'登录成功！欢迎 {user.get_role_display()} {user.username}')
            return redirect('index')
        else:
            messages.error(request, '用户名或密码错误')
    return render(request, 'accounts/login.html')


# 注册视图
def user_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        phone = request.POST.get('phone')
        role = request.POST.get('role', 'resident')

        # 验证密码
        if password != password2:
            messages.error(request, '两次密码不一致')
            return render(request, 'accounts/register.html')

        # 检查用户名是否存在
        if User.objects.filter(username=username).exists():
            messages.error(request, '用户名已存在')
            return render(request, 'accounts/register.html')

        # 创建用户
        try:
            user = User.objects.create_user(
                username=username,
                password=password,
                role=role,
                phone=phone
            )
            messages.success(request, '注册成功！请登录')
            return redirect('user-login')
        except Exception as e:
            messages.error(request, f'注册失败：{str(e)}')

    # 获取所有小区（供物业/住户选择）
    communities = Community.objects.all()
    return render(request, 'accounts/register.html', {'communities': communities})


# 登出视图
def user_logout(request):
    logout(request)
    messages.success(request, '已成功退出登录')
    return redirect('index')


# 个人资料视图
@login_required
def user_profile(request):
    if request.method == 'POST':
        user = request.user
        user.phone = request.POST.get('phone', user.phone)
        user.email = request.POST.get('email', user.email)
        if request.user.role in ['resident', 'property_admin']:
            community_id = request.POST.get('community')
            user.community = Community.objects.get(id=community_id) if community_id else None
        user.save()
        messages.success(request, '个人资料更新成功')
        return redirect('user-profile')

    communities = Community.objects.all()
    return render(request, 'accounts/profile.html', {'communities': communities})


# 超级管理员用户管理
@login_required
def super_user_list(request):
    if request.user.role != 'super_admin':
        messages.error(request, '无权限访问')
        return redirect('index')
    users = User.objects.all()
    communities = Community.objects.all()
    return render(request, 'accounts/super_user_list.html', {'users': users, 'communities': communities})


# 物业管理员查看本小区用户
@login_required
def property_user_list(request):
    if request.user.role != 'property_admin':
        messages.error(request, '无权限访问')
        return redirect('index')
    users = User.objects.filter(community=request.user.community)
    return render(request, 'accounts/property_user_list.html', {'users': users})