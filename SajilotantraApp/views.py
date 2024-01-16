import heapq
import json
import os
from collections import defaultdict

from bitarray import bitarray
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User  # default user model
from django.contrib.auth.models import AnonymousUser
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from Sajilotantra import settings
from SajilotantraApp.models import Event, GovernmentProfile

from .models import (Feedback, GovernmentProfile, Guidance, Notification, Post,
                     PostComment, PostLike, UploadedFile, UserProfile)
from .tokens import generate_token
from .utils import *


def index(request):
    return render(request, 'index.html')

def signup(request):
    if request.method=="POST":
        username=request.POST.get("username")
        pass1=request.POST.get("pass1")
        fname=request.POST.get("fname")
        lname=request.POST.get("lname")
        pass2=request.POST.get("pass2")
        email=request.POST.get("email")
        print(username,pass1,pass2,fname,lname,email)

        #authentication(to check if the username and email are already taken)

        if User.objects.filter(username=username):
            messages.error(request,"The username you entered is already taken, try another username")
            return redirect("signup")
        
        if User.objects.filter(email=email):
            messages.error(request,"The email you entered is already taken, try another email")
            return redirect("signup")
        
        myuser=User.objects.create_user(username,email,pass1)#create user in the database with the details entered
        myuser.first_name=fname
        myuser.last_name=lname
        myuser.is_active=False# before the user confirms their email address, the user's account(created) will not be active.

        myuser.save()

        messages.success(request,"Your account has been successfully Created.  We have sent you a confirmation email, please click on the activation link to activate your account.")

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
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        remember_me = request.POST.get('remember')
        user = authenticate(request, username=username, password=pass1)
        print(username, pass1)

        # Check if user exists
        if user is None:
            messages.info(request, "Incorrect login credentials. Try again")
            return redirect('signin')

        # Login successful
        login(request, user)
        return redirect('dashboard')

    form = AuthenticationForm()
    return render(request, 'signin.html', {'form': form})


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
    



     
def events(request):
    all_events = Event.objects.all()
    context = {
        "events":all_events,
    }
    return render(request,'events.html',context)

def all_events(request):
    all_events = Event.objects.all()
    out = []
    for event in all_events:
        out.append({
            'title': event.name,
            'id': event.id,
            'description': event.description,
            'start': event.start.isoformat(),  # Use isoformat() here
            'end': event.end.isoformat(),      # Use isoformat() here
        })
    return JsonResponse(out, safe=False)

    all_events = Event.objects.all()
    out = []
    for event in all_events:
        out.append({
            'title': event.name,
            'id': event.id,
            'start': event.start.strftime("%m/%d/%Y, %H:%M:%S"),
            'end': event.end.strftime("%m/%d/%Y, %H:%M:%S"),
        })
    return JsonResponse(out, safe=False)
    return render(request,'events.html')

# def map(request):
#     return render(request, 'map.html')

def dashboard(request):
    notifications = Notification.objects.all()
    guidance = Guidance.objects.all().order_by('-pk')
    events = Event.objects.all().order_by('-pk')
    posts= Post.objects.all().order_by('-pk')
    
    for post in posts:
        if post.image:  # Check if the image field is not None
            # Get the file extension
            file_extension = os.path.splitext(post.image.url)[1][1:].lower()
            post.file_extension = file_extension
            
        post.decoded_caption = post.decode_caption()
        print(f"(dashboard) Decoded Caption: {post.decoded_caption}")
    context = {
        'notifications': notifications,
        'guidance_items': guidance[:6],  # Fetching the first 6 guidance items
        'events': events[:3],
        'posts':posts,
    }

    return render(request, 'dashboard.html', context)

def card(request):
    details=Guidance.objects.all().order_by('-pk')
    context={
        'details':details
    }
    return render(request, 'guidelines_details.html',context)

def guide_blog(request,pk):
    # print(f"Guide steps function called with pk={pk} and category={category}")
    # guidance = get_object_or_404(Guidance, id=pk, category=category)
    # print(f"Guidance object retrieved: {guidance}")
    # return render(request, 'guide_steps.html', {'guidance': guidance})
   guideBlog=Guidance.objects.get(id=pk)
   blog={
    'guideBlog':guideBlog
   }
   return render(request,'guide_steps.html',blog)

def government_profiles(request):
    profiles=GovernmentProfile.objects.all().order_by('-pk')
    data={
        'profiles':profiles
    }
    return render(request, 'government_profiles.html', data)

def map(request):
    profiles=GovernmentProfile.objects.all().order_by("-pk")
    data={
        'profiles':profiles
    }
    return render(request,'map.html',data)


def government_profiles_details(request,pk):
    profiles = get_object_or_404(GovernmentProfile, profile_id=pk)
    return render(request,'government_profiles_details.html',{'GovernmentProfile':profiles})

from django.http import Http404


# @login_required
def profile(request, username):
    auth_user = request.user
    print(auth_user)

    try:
        # Retrieve the user based on the provided username
        user = User.objects.get(username=username)

        if auth_user != user:
            # If they don't match, redirect to the login page
            return redirect('signin')

        if user is None:
            return render(request, "user_does_not_exist.html")

        # Retrieve or create UserProfile based on user_id
        profile, created = UserProfile.objects.get_or_create(user=user)

        # Handle profile update
        if request.method == 'POST':
            # Preserve the existing bio if the new bio is empty
            new_bio = request.POST.get('bio', '')
            if new_bio != '':
                profile.bio = new_bio

            # Update profile picture
            if 'picture' in request.FILES:
                profile.image = request.FILES['picture']

            # Update cover photo
            if 'cover' in request.FILES:
                profile.cover = request.FILES['cover']

            #drag and drop profile
            if 'drop-area-profile' in request.FILES:
                profile.image= request.FILES['drop-area-profile']

            #drag and drop cover
            if 'drop-area-cover' in request.FILES:
                profile.cover= request.FILES['drop-area-cover']

            profile.save()
            messages.success(request,"Your profile has been updated successfully")


        context = {
            'user': user,
            'auth_user': auth_user,
        }

    except User.DoesNotExist:
        raise Http404("User does not exist")

    return render(request, 'profileupdate.html', context)



def view_profile(request, username):
    user = get_object_or_404(User, username=username)
    
    try:
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        return render(request, 'user_does_not_exist.html')

    # if user is None:
    #     return render(request, 'user_does_not_exist.html')
    
    profile = UserProfile.objects.get(user=user)

    context = {
        'user': user,
        'profile': profile,
    }

    return render(request, 'frontprofile.html', context)


def government_profiles(request):
    profiles=GovernmentProfile.objects.all().order_by('-pk')
    data={
        'profiles':profiles
    }
    return render(request, 'government_profiles.html', data)

def map(request):
    profiles=GovernmentProfile.objects.all().order_by("-pk")
    data={
        'profiles':profiles
    }
    return render(request,'map.html',data)


def government_profiles_details(request,pk):
    profiles = get_object_or_404(GovernmentProfile, profile_id=pk)
    return render(request,'government_profiles_details.html',{'GovernmentProfile':profiles})

from django.http import Http404


# @login_required
def profile(request, username):
    auth_user = request.user
    print(auth_user)

    try:
        # Retrieve the user based on the provided username
        user = User.objects.get(username=username)

        if auth_user != user:
            # If they don't match, redirect to the login page
            return redirect('signin')

        if user is None:
            return render(request, "user_does_not_exist.html")

        # Retrieve or create UserProfile based on user_id
        profile, created = UserProfile.objects.get_or_create(user=user)

        # Handle profile update
        if request.method == 'POST':
            # Preserve the existing bio if the new bio is empty
            new_bio = request.POST.get('bio', '')
            if new_bio != '':
                profile.bio = new_bio

            # Update profile picture
            if 'picture' in request.FILES:
                profile.image = request.FILES['picture']

            # Update cover photo
            if 'cover' in request.FILES:
                profile.cover = request.FILES['cover']

            #drag and drop profile
            if 'drop-area-profile' in request.FILES:
                profile.image= request.FILES['drop-area-profile']

            #drag and drop cover
            if 'drop-area-cover' in request.FILES:
                profile.cover= request.FILES['drop-area-cover']

            profile.save()
            messages.success(request,"Your profile has been updated successfully")


        context = {
            'user': user,
            'auth_user': auth_user,
        }

    except User.DoesNotExist:
        raise Http404("User does not exist")

    return render(request, 'profileupdate.html', context)

def view_profile(request, username):
    user = get_object_or_404(User, username=username)
    
    try:
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        return render(request, 'user_does_not_exist.html')

    # if user is None:
    #     return render(request, 'user_does_not_exist.html')
    
    profile = UserProfile.objects.get(user=user)

    context = {
        'user': user,
        'profile': profile,
    }

    return render(request, 'frontprofile.html', context)

def feedback(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        suggestion = request.POST.get('Suggestion')

        feedback = Feedback(category=category, suggestion=suggestion)
        feedback.save()

        # Handle file uploads
        uploaded_files = request.FILES.getlist('user_avatar')
        for uploaded_file in uploaded_files:
            file_instance = UploadedFile(feedback=feedback, file=uploaded_file)
            file_instance.save()
        messages.success(request, "A new feedback is added go and check through!")
        # Redirect or render a thank you page
        return HttpResponseRedirect('feedback')  # Replace '/thank-you/' with your desired URL

    return render(request, 'feedback.html') 



@login_required(login_url='/signin')
def create_post(request):
    if request.method == 'POST':
        caption = request.POST.get('postCaption')
        category = request.POST.get('category')
        image = request.FILES.get('file_input')
        auth_user = request.user
        user_profile, created = UserProfile.objects.get_or_create(user=auth_user)
        try:
            # Calling the Huffman Coding:
            encoded_caption, encoding_dict = huffman_encode(caption)
            # encoded_caption, _ = huffman_encode(caption)
            post = Post.objects.create(
                user=user_profile,
                encoded_caption=encoded_caption,
                category=category,
                image=image,
                encoding_dict=json.dumps(encoding_dict)
            )
            return redirect('dashboard')
        except Exception as e:
            print(f"Error creating post: {e}")
    return redirect('dashboard.html')

def get_names(request):
    search = request.GET.get('search')
    payload = []

    if search:
        objs = UserProfile.objects.filter(user__username__startswith=search)

        for obj in objs:
            payload.append({
                'user': obj.user.username
            })

    return JsonResponse(
        {
            'status': True,
            'payload': payload,
        }
    )
  
@login_required(login_url='/signin')
def like_post(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_id)
        user_profile = request.user.userprofile

        # Check if the user has already liked the post
        if PostLike.objects.filter(post=post, user=user_profile).exists():
            # User has already liked the post, you might want to handle this case
            return JsonResponse({'message': 'You have already liked this post'})

        # Create a new PostLike instance
        like = PostLike.objects.create(post=post, user=user_profile)
        return JsonResponse({'message': 'Post liked successfully', 'like_id': like.pk})

    # Handle cases for GET requests or other HTTP methods
    return JsonResponse({'message': 'Method not allowed'}, status=405)

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import redirect, render


# @login_required
def change_password(request, username):
    auth_user = request.user
    print(auth_user)
    user = User.objects.get(username=username)


    error_message = None
    password_changed = False  # Assuming this variable is used to display a success message
    
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password1']
            
            # Change the user's password and update the session
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)
            
            messages.success(request, 'Password changed successfully.')
            password_changed = True
        else:
            error_message = 'Please correct the errors below.'
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")  # Add form errors to messages
    else:
        form = PasswordChangeForm(user=request.user)
    
    return render(request, 'change_password.html', {'form': form, 'error_message': error_message, 'password_changed': password_changed})
