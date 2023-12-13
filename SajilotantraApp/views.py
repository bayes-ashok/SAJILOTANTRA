from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from SajilotantraApp.models import Events

from Sajilotantra import settings

from .tokens import generate_token


def index(request):
    return render(request, 'index.html')

def signup(request):
    if request.method=="POST":
        username=request.POST.get("username")#username=email address
        pass1=request.POST.get("pass1")
        fname=request.POST.get("fname")
        lname=request.POST.get("lname")
        pass2=request.POST.get("pass2")
        print(username,pass1,pass2,fname,lname)

        #authentication(to check if the username(email) is already taken)

        if User.objects.filter(email=username):
            messages.error(request,"The username you entered is already taken, try another username")
            return redirect("signup")
        
        myuser=User.objects.create_user(fname,username,pass1)#create user in the database with the details entered
        myuser.first_name=fname
        myuser.last_name=lname
        myuser.is_active=False# before the user confirms their email address, the user's account(created) will not be active.

        myuser.save()

        messages.success(request,"Your account has been successfully Created. We have sent you a confirmation email, please click on the activation link to activate your account.")

        #Send Welcome Email
        subject="Welcome to Sajilotantra"
        message="Hello "+ str(myuser.first_name)+", \nWelcome to Sajilotantra. We have also sent you a confirmation email, please confirm your email address to activate your account.\n\n Thank You, \n Sajilotantra Team."
        from_email=settings.EMAIL_HOST_USER
        to_list=[myuser.email]
        send_mail(subject,message,from_email,to_list,fail_silently=True)#even if the email is not sent, it will not crash the website

        #Send Confirmation Email with Activation Token
        current_site=get_current_site(request)
        email_subject="Confirm your email @Sajilotantra"
        email_message=render_to_string("email_confirmation.html",{
            "name":myuser.first_name,
            "domain":current_site.domain,
            "uid": urlsafe_base64_encode(force_bytes(myuser.pk)),
            "token": generate_token.make_token(myuser)
        })
        email=EmailMessage(
            email_subject,
            email_message,
            settings.EMAIL_HOST_USER,
            [myuser.email],

        )
        email.fail_silently=True
        email.send()

        return redirect("signin")#after a successfull signup, redirect the user to sign in page

    return render(request,"signup.html")

def signin(request):
    return render(request,"signin.html")

# def playground(request):
#     return render(request,"playground.html")

def dashboard(request):
    return render(request,"dashboard.html")

def activate(request,uidb64,token):#activate user account if the confirmation link is clicked
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active = True
        # user.profile.signup_confirmation = True
        myuser.save()
        signin(request)
        messages.success(request, "Your Account has been activated!")
        return redirect('signin')
    else:
        return render(request,'activation_failed.html')
    

# events calendar
def events(request):
    return render(request,'events.html')