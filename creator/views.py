from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User,auth
from . models import Contents
from django.http import JsonResponse
import base64
from django.core.files.base import ContentFile
from . models import *
# Create your views here.

def register_creator(request):
    if request.method == 'POST':
        first_name = request.POST['firstName']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        verifypassword = request.POST['verifypassword']
        if password==verifypassword:
            if User.objects.filter(email=email).exists():
                return JsonResponse('emailtaken', safe=False)
            elif User.objects.filter(username=username).exists():
                return JsonResponse('usernametaken',safe=False)
            else:
                user = User.objects.create_user(first_name=first_name,email=email,username=username,password=password,is_staff=True)
                user.save()
                return JsonResponse('success',safe=False)
        else:
            return JsonResponse('invalidpassword',safe=False)
    else:
        return render(request, './creator/register.html')

def login_creator(request):
    if request.user.is_authenticated:
        return redirect(creator_dashboard)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if not user.is_staff == False:
            if user:
                auth.login(request,user)
                return JsonResponse('loginsucess', safe=False)
            else:
                return JsonResponse('loginfail', safe=False)
        else:
            return JsonResponse('youarenotcreator', safe=False)
    else:
        return render(request, './creator/login.html')

def creator_logout(request):
    auth.logout(request)
    return redirect(login_creator)

def creator_profile(request):
    if CreatorDeatails.objects.filter(user=request.user).exists():
        extra_details = CreatorDeatails.objects.get(user=request.user)
        return render(request, './creator/creator_profile.html',{'extra_details':extra_details})
    else:
        return render(request, './creator/creator_profile.html')
        

def edit_creator_profile(request,id):
    creator_details = User.objects.get(id=id)
    if request.method == 'POST':
        creator_details.first_name = request.POST['fullname']
        creator_details.username = request.POST['username']
        creator_details.email = request.POST['email']
        creator_details.save()
        about_me = request.POST['aboutme']
        if CreatorDeatails.objects.filter(user=request.user).exists():
            extra_details = CreatorDeatails.objects.get(user=request.user)
            extra_details.about_me = about_me
            extra_details.save()
        else:
            CreatorDeatails.objects.create(user=request.user,about_me=about_me)
        return redirect(creator_profile)
    else:
        if CreatorDeatails.objects.filter(user=request.user).exists():
            extra_details = CreatorDeatails.objects.get(user=request.user)
            return render(request, './creator/edit_creator_profile.html',{'extra_details':extra_details})
        else:
            return render(request, './creator/edit_creator_profile.html')

def creator_dashboard(request):
    return render(request, './creator/creator_dashboard.html')

def display_contents(request):
    content = Contents.objects.filter(user=request.user)
    return render(request, './creator/display_contents.html', {'content':content})

def create_content(request):
    if request.method == 'POST':
        episode_name = request.POST['episode_name']
        description = request.POST['description']
        audio = request.FILES['audio']
        podcast_thumbnail = request.POST['pro_img']

        if podcast_thumbnail is not '':
            format, imgstr = podcast_thumbnail.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name=episode_name + '.' + ext)
            podcast_data = Contents.objects.create(user=request.user,episode_name=episode_name,description=description,podcast=audio,thumbnail=data)
        else:
            podcast_data = Contents.objects.create(user=request.user,episode_name=episode_name,description=description,podcast=audio)
        podcast_data.save()
        return render(request, './creator/create_content.html')
    else:
        return render(request, './creator/create_content.html')

def edit_content(request,id):
    content = Contents.objects.get(id=id)
    if request.method == 'POST':
        episode_name = request.POST['episode_name']
        description = request.POST['description']
        audio = request.FILES['audio']
        podcast_thumbnail = request.POST['pro_img']

        if podcast_thumbnail is not '':
            format, imgstr = podcast_thumbnail.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name=episode_name + '.' + ext)
            content.thumbnail = data

        content.episode_name = episode_name
        content.description = description
        content.podcast = audio
        content.save()
    return render(request, './creator/edit_content.html',{'content':content})

def delete_content(request,id):
    content = Contents.objects.get(id=id)
    content.delete()
    return redirect(display_contents)

