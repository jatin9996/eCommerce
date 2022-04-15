from django.shortcuts import render,redirect
from .models import *
import random
from django.core.mail import send_mail

def register(request):
    if request.method=='POST':
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']
        if pass1==pass2:
            Register(first_name=fname,last_name=lname,email=email,password=pass1).save()
            return redirect('login')
        else:
            return render(request,'register.html',{'error':"Password do not match"})
    return render(request,'register.html')

def login(request):
    if request.method=='POST':
        email=request.POST['email']
        pass1=request.POST['pass1']
        try:
            user_info=Register.objects.get(email=email)
            if pass1==user_info.password:
                request.session['user']=email
                return redirect('home')
            else:
                return render(request,'login.html',{'error':"Invalid Password"})
        except:
            return render(request,'login.html',{'error':"Invalid Email Id"})
    return render(request,'login.html')

def logout(request):
    if 'user' in request.session:
        del request.session['user']
        return redirect('login')

def home(request):
    return render(request,'index.html')

def forgetpassword(request):
    if request.method=='POST':
        email_id=request.POST['email']
        otp=random.randint(11111,99999)
        user=Register.objects.get(email=email_id)
        if user is not None:
            send_mail(
                'OTP Verifications',
                f'Your OTP is {otp}.Do not share your otp with anyone.',
                '____________@gmail.com',
                [email_id],
            )
            request.session['otp']=otp
            request.session['user']=user.email
            return redirect('eotp')
        else:
            return render(request,'forgetpassword.html',{'error':'Invalid Email ID,Please enter registered Email'})
    else:
        return render(request,'forgetpassword.html')

    

def eotp(request):
    otp=request.session['otp']
    if request.method=='POST':
        eotp=request.POST['eotp']
        if otp==int(eotp):
            return redirect('changepassword')
        else:
            return redirect('eotp')
    else:
        return render(request,'eotp.html')

def changepassword(request):
    if request.method=='POST':
        eemail=request.session['user']
        user=Register.objects.get(email=eemail)
        if request.method=='POST':
            pass1=request.POST['pass1']
            pass2=request.POST['pass2']
            if pass1==pass2:
                user.password=pass2
                user.save()
                return redirect('login')
            else:
                return redirect('changepassword')
        else:
            return redirect('eotp')
    else:
        return render(request,'changepassword.html')