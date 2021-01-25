from django.shortcuts import render,redirect,HttpResponse
from django.http import JsonResponse
from django.contrib.auth.models import User,auth
from . models import UserDetails
from creator.models import Contents,CreatorDeatails
import requests
import json
from django.core import serializers
from django.contrib.auth.decorators import login_required

# Create your views here.

def consumer_registration(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        mobile_number = request.POST['mobilenumber']
        password = request.POST['password']
        verifypassword = request.POST['verifyPassword']

        if password==verifypassword:
            if User.objects.filter(email=email).exists():
                return JsonResponse('emailtaken', safe=False)
            elif User.objects.filter(username=username).exists():
                return JsonResponse('usernametaken',safe=False)
            elif UserDetails.objects.filter(mobile_number=mobile_number).exists():
                return JsonResponse('mobilenumberexists',safe=False)
            else:
                user = User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
                UserDetails.objects.create(user=user,mobile_number=mobile_number)
                return JsonResponse('success', safe=False)
        else:
            return JsonResponse('invalidpassword', safe=False)
    else:
        return render(request, './consumer/consumer_registration.html')

def popup_login(request):
    return render(request, './consumer/Pop_Login.html')

def consumer_login(request):
    if request.user.is_authenticated:
        return redirect(consumer_homepage)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if not user.is_staff == True:
            if user:
                auth.login(request,user)
                return JsonResponse('success', safe=False)
            else:
                return JsonResponse('loginfailed', safe=False)
        else:
            return JsonResponse('youarenotconsumer', safe=False)
    else:
        return render(request, './consumer/consumer_login.html')

def mobile_login(request):
    if request.method == 'POST':
        user_mobile_number = request.POST['mobile_number']
        print(user_mobile_number)
        if UserDetails.objects.filter(mobile_number=user_mobile_number).exists():
            url = "https://d7networks.com/api/verifier/send"

            payload = {'mobile': str(+91)+user_mobile_number,
            'sender_id': 'SMSINFO',
            'message': 'Your otp code is {code}',
            'expiry': '900000'}
            files = [

            ]
            headers = {
            'Authorization': 'Token b76a52adeb253e2dbb98dd2378d542f8d53fbe6b'
            }

            response = requests.request("POST", url, headers=headers, data = payload, files = files)
            data = response.text.encode('utf8')
            dict = json.loads(data.decode('utf8'))
            otp_id = dict['otp_id']
            request.session['otp_id'] = otp_id
            request.session['phone'] = user_mobile_number
            return JsonResponse('success', safe=False)
        else:
            return JsonResponse('notregistered', safe=False)
    else:
        return render(request, './consumer/Mobile_login.html')

def verify_otp(request):
    if request.method == 'POST':
        otp = request.POST['otp']
        otp_id = request.session['otp_id']
        user_mobile_number = request.session['phone']

        url = "https://d7networks.com/api/verifier/verify"

        payload = {'otp_id': otp_id,
        'otp_code': otp}
        files = [

        ]
        headers = {
        'Authorization': 'Token b76a52adeb253e2dbb98dd2378d542f8d53fbe6b'
        }

        response = requests.request("POST", url, headers=headers, data = payload, files = files)

        data = response.text.encode('utf8')
        dict = json.loads(data.decode('utf8'))
        status = dict['status']

        if status == 'success':
            user_detail = UserDetails.objects.filter(mobile_number=user_mobile_number).first()
            user = user_detail.user
            if user:
                auth.login(request,user,backend='django.contrib.auth.backends.ModelBackend')
                return JsonResponse('success', safe=False)
            else:
                return JsonResponse('otpfail', safe=False)
        else:
            return JsonResponse('otpfail', safe=False)
    else:
        return render(request, './consumer/Verify_otp.html')

def consumer_forgot_password(request):
    return render(request, './consumer/consumer_forgot_password.html')

def consumer_logout(request):
    auth.logout(request)
    return redirect(consumer_homepage)

def consumer_homepage(request):
    consumer_data = Contents.objects.all()
    return render(request, './consumer/homepage.html',{'consumer_data':consumer_data})


def consumer_profile(request):
    if request.user.is_authenticated:
        user_details = UserDetails.objects.get_or_create(user=request.user)
        user_secondary_data = UserDetails.objects.get(user=request.user)
        return render(request, './consumer/consumer_profile.html',{'user_details':user_details,'user_secondary_data':user_secondary_data})
    else:
        return redirect(consumer_login)

def consumer_profile_edit(request,id):
    if request.user.is_authenticated:
        user_primary_data = User.objects.get_or_create(id=id)
        user_secondary_data = UserDetails.objects.get(user=request.user)
        if request.method == 'POST':
            user_primary_data.first_name = request.POST['firstname']
            user_primary_data.last_name = request.POST['lastname']
            user_details.mobile_number = request.POST['mobilenumber']
            user_details.save()
            user_primary_data.save()
            return redirect(consumer_profile)
        else:
            return render(request, './consumer/consumer_profile_edit.html',{'user_secondary_data':user_secondary_data})
    else:
        return redirect(consumer_login)

def consumer_password_change(request,id):
    if request.method == 'POST':
        new_password = request.POST['new_password']
        verify_password = request.POST['verify_password']
    else:
        return render(request, './consumer/Consumer_change_password.html')

@login_required()
def music_player(request,id):
    consumer_data = Contents.objects.get(id=id)
    return render(request, './consumer/music_player.html',{'consumer_data':consumer_data})

def next_music_data(request,id):
    consumer_data = Contents.objects.get(id=id)
    data = {'next_songs':serializers.serialize('json',[consumer_data])}
    return JsonResponse(data)

def previous_music_data(request,id):
    consumer_data = Contents.objects.get(id__exact=id)
    data = {'previous_songs':serializers.serialize('json',[consumer_data])}
    return JsonResponse(data)


@login_required(login_url='/login/')
def consumer_playlist(request):
    return render(request, './consumer/playlist.html')

def consumer_latest_feed(request):
    return render(request, './consumer/latest.html')