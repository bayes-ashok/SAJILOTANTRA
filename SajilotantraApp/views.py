import heapq
import json
import os
from collections import defaultdict

from bitarray import bitarray
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User  
from django.contrib.auth.models import AnonymousUser
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import redirect, render
from django.utils.encoding import force_bytes, force_str
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.http import require_POST

from .models import Post, PostLike

from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from Sajilotantra import settings
from SajilotantraApp.models import Event, GovernmentProfile

from .models import (Feedback, GovernmentProfile, Guidance, Notification, Post,
                     PostComment, PostLike, ReportedPost, UploadedFile,
                     UserProfile)
from .tokens import generate_token
from .utils import *



def index(request):
    auth_user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=auth_user)
    

    
    context = {
        'user_profile':user_profile
    }

    return render(request, 'index.html', context)




def e(request):
    return render(request,'event.html')
def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        pass1 = request.POST.get("pass1")
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        pass2 = request.POST.get("pass2")
        email = request.POST.get("email")

        if User.objects.filter(username=username).exists():
            messages.error(request, "The username you entered is already taken, try another username")
            return redirect("signup")

        if User.objects.filter(email=email).exists():
            messages.error(request, "The email you entered is already taken, try another email")
            return redirect("signup")

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = False  
        myuser.save()

        new_user_profile = UserProfile.objects.create(user=myuser)
        new_user_profile.save()

        messages.success(request,"Your account has been successfully Created.  We have sent you a confirmation email, please click on the activation link to activate your account.")

        subject="Welcome to Sajilotantra"
        message="Hello "+ str(myuser.first_name)+", \nWelcome to Sajilotantra. We have also sent you a confirmation email, please confirm your email address to activate your account.\n\n Thank You, \n Sajilotantra Team."
        from_email=settings.EMAIL_HOST_USER
        to_list=[myuser.email]
        send_mail(subject,message,from_email,to_list,fail_silently=True)

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

        return redirect("signin")

    return render(request,"signup.html")

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        remember_me = request.POST.get('remember')
        user = authenticate(request, username=username, password=pass1)
        print(username, pass1)

        if user is None:
            messages.info(request, "Incorrect login credentials. Try again")
            return redirect('signin')

        login(request, user)
        return redirect('dashboard')

    form = AuthenticationForm()
    return render(request, 'signin.html', {'form': form})


def activate(request,uidb64,token):
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
    auth_user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=auth_user)
    context = {
        "events":all_events,
        'user_profile':user_profile
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
            'start': event.start.isoformat(),  
            'end': event.end.isoformat(),      
            'Location':event.Location,
        })
    return JsonResponse(out, safe=False)


@login_required(login_url='signin')
def dashboard(request):
    notifications = Notification.objects.all()
    guidance = Guidance.objects.all().order_by('-pk')
    events = Event.objects.all().order_by('-pk')
    posts= Post.objects.all().order_by('-pk')
    auth_user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=auth_user)
    

    post_comments={}
    for post in posts:
        comments=PostComment.objects.filter(post=post)
        post_comments[post.id]=comments
        if post.image:  
            file_extension = os.path.splitext(post.image.url)[1][1:].lower()
            post.file_extension = file_extension
            
        post.decoded_caption = post.decode_caption()
        print(f"(dashboard) Decoded Caption: {post.decoded_caption}")
    context = {
        'notifications': notifications,
        'guidance_items': guidance[:6], 
        'events': events[:3],
        'post_comments':post_comments,
        'posts':posts,
        'post_comments':post_comments,
        'user_profile':user_profile
    }

    return render(request, 'dashboard.html', context)

def card(request):
    details=Guidance.objects.all().order_by('-pk')
    auth_user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=auth_user)
    context={
        'user_profile':user_profile,
        'details':details
    }
    return render(request, 'guidelines_details.html',context)

def guide_blog(request,pk):

    guideBlog=Guidance.objects.get(id=pk)
    auth_user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=auth_user)
    blog={
        'guideBlog':guideBlog,
        'user_profile':user_profile
    }
    return render(request,'guide_steps.html',blog)

def government_profiles(request):
    profiles=GovernmentProfile.objects.all().order_by('-pk')
    auth_user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=auth_user)

    data={
        'user_profile':user_profile,
        'profiles':profiles
    }
    return render(request, 'government_profiles.html', data)


def landing(request):
    return render(request,'landing.html')

def map(request):
    profiles=GovernmentProfile.objects.all().order_by("-pk")
    auth_user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=auth_user)
    data={
        'user_profile':user_profile,
        'profiles':profiles
    }
    return render(request,'map.html',data)


def government_profiles_details(request,pk):
    profiles = get_object_or_404(GovernmentProfile, profile_id=pk)
    auth_user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=auth_user)
    return render(request,'government.html',{'GovernmentProfile':profiles, 'user_profile':user_profile})



def government_profiles(request):
    profiles=GovernmentProfile.objects.all().order_by('-pk')
    auth_user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=auth_user)    
    data={
        'user_profile':user_profile,
        'profiles':profiles
    }
    return render(request, 'government_profiles.html', data)

def map(request):
    profiles=GovernmentProfile.objects.all().order_by("-pk")
    auth_user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=auth_user)    
    data={
        'user_profile':user_profile,
        'profiles':profiles
    }
    return render(request,'map.html',data)



from django.http import Http404


# @login_required
def profile(request, username):
    auth_user = request.user
    print(auth_user)

    try:
        auth_user = request.user
        user = User.objects.get(username=username)
        profile = UserProfile.objects.get(user=user)
        posts= Post.objects.filter(user=profile).order_by("-pk")
        profile = UserProfile.objects.get(user=user)
        posts= Post.objects.filter(user=profile).order_by("-pk")
        auth_user = request.user
        user_profile, created = UserProfile.objects.get_or_create(user=auth_user)    
        posts_comments={}
        for post in posts:
            comments=PostComment.objects.filter(post=post)
            posts_comments[post.id]=comments
            posts.decoded_caption = post.decode_caption()
            post_category=post.category
            print(f"(dashboard) Decoded Caption: {posts.decoded_caption}")

        if auth_user != user:
            return redirect('signin')

        if user is None:
            return render(request, "user_does_not_exist.html")

        profile, created = UserProfile.objects.get_or_create(user=user)

        if request.method == 'POST':
            new_bio = request.POST.get('bio', '')
            if new_bio != '':
                profile.bio = new_bio

            new_f_name=request.POST.get('fname','')
            if new_f_name != '':
                user.last_name = new_f_name

            new_l_name=request.POST.get('lname','')
            if new_l_name != '':
                user.first_name = new_l_name

            if 'picture' in request.FILES:
                profile.image = request.FILES['picture']

            if 'cover' in request.FILES:
                profile.cover = request.FILES['cover']

            if 'drop-area-profile' in request.FILES:
                profile.image= request.FILES['drop-area-profile']

            if 'drop-area-cover' in request.FILES:
                profile.cover= request.FILES['drop-area-cover']
            user.save()
            profile.save()
            messages.success(request,"Your profile has been updated successfully")
            

        context = {
            'user': user,
            'auth_user': auth_user,
            'profile': profile,
            'posts':posts,
            'posts.decoded_caption':posts.decoded_caption,
            'posts_comments':posts_comments,
            'post_category':post_category,
            'user_profile':user_profile
        }

    except:
        return render(request,"user_does_not_exist.html")

    return render(request, 'profileupdate.html', context)


@login_required(login_url='signin')
def view_profile(request, username):
    auth_user=request.user
    user_profile, created = UserProfile.objects.get_or_create(user=auth_user)   
    try:
        auth_user=request.user
        auth_profile = get_object_or_404(UserProfile, user=auth_user)
        user = get_object_or_404(User, username=username)
        profile = get_object_or_404(UserProfile, user=user)
        posts = Post.objects.filter(user=profile).order_by("-pk")
        posts_comments={}
        for post in posts:
            comments=PostComment.objects.filter(post=post)
            posts_comments[post.id]=comments
            post_category=post.category
            posts.decoded_caption = post.decode_caption()
            print(f"(dashboard) Decoded Caption: {posts.decoded_caption}")
    except Http404:
        return render(request, 'user_does_not_exist.html')
    context = {
        'user': user,
        'profile': profile,
        'posts': posts,
        'auth_profile': auth_profile,
        'posts.decoded_caption':posts.decoded_caption,
        'posts_comments':posts_comments,
        'posts':posts,
        'post_category':post_category,
        'posts_comments':posts_comments,
        'user_profile':user_profile
    }
    return render(request, 'frontprofile.html', context)


def feedback(request):
    auth_user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=auth_user)    
    data={
        'user_profile':user_profile,
    }
    if request.method == 'POST':
        category = request.POST.get('category')
        suggestion = request.POST.get('Suggestion')

        feedback = Feedback(category=category, suggestion=suggestion)
        feedback.save()

        uploaded_files = request.FILES.getlist('user_avatar')
        for uploaded_file in uploaded_files:
            file_instance = UploadedFile(feedback=feedback, file=uploaded_file)
            file_instance.save()
        messages.success(request, "A new feedback is added go and check through!")
        return HttpResponseRedirect('feedback')  

    return render(request, 'feedback.html',data) 



@login_required(login_url='/signin')
def create_post(request):
    if request.method == 'POST':
        caption = request.POST.get('postCaption')
        category = request.POST.get('category')
        image = request.FILES.get('file_input')
        auth_user = request.user
        user_profile, created = UserProfile.objects.get_or_create(user=auth_user)
        try:
            encoded_caption, encoding_dict = huffman_encode(caption)
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

@login_required(login_url="/signin")
def add_comment(request, post_id):
    if request.method =='POST':
        post=get_object_or_404(Post, pk=post_id)
        comment_user=request.user.userprofile
        text = request.POST.get('commentInput')

        if text:
            comment = PostComment.objects.create(post=post, user=comment_user, text=text)
            messages.success(request, 'Comment added successfully!')
            return redirect("dashboard")
        else:
            messages.error(request, 'Invalid comment input.')
            return redirect("map")

    return redirect("dashboard")
    

@login_required(login_url="/signin")
def add_comment(request, post_id):
    if request.method =='POST':
        post=get_object_or_404(Post, pk=post_id)
        comment_user=request.user.userprofile
        text = request.POST.get('commentInput')

        if text:
            comment = PostComment.objects.create(post=post, user=comment_user, text=text)
            messages.success(request, 'Comment added successfully!')
            return redirect("dashboard")
        else:
            messages.error(request, 'Invalid comment input.')
            return redirect("map")

    return redirect("dashboard")

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


def change_password(request, username):
    auth_user = request.user
    print(auth_user)
    user = User.objects.get(username=username)


    error_message = None
    password_changed = False  
    
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password1']
            
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)
            
            messages.success(request, 'Password changed successfully.')
            password_changed = True
        else:
            error_message = 'Please correct the errors below.'
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")  
    else:
        form = PasswordChangeForm(user=request.user)
    
    return render(request, 'change_password.html', {'form': form, 'error_message': error_message, 'password_changed': password_changed})

def report_post(request, post_id):
    if request.method == 'POST':
        reason = request.POST.get('reason', '')
        report = ReportedPost.objects.create(post_id=post_id, reason=reason)
        print(f"Reported post saved: {report}")

        return redirect('dashboard')
    return render(request, 'dashboard.html')



@login_required(login_url="/signin")
def add_comment(request, post_id):
    if request.method =='POST':
        post=get_object_or_404(Post, pk=post_id)
        comment_user=request.user.userprofile
        text = request.POST.get('commentInput')

        if text:
            comment = PostComment.objects.create(post=post, user=comment_user, text=text)
            messages.success(request, 'Comment added successfully!')
            return redirect("dashboard")
        else:
            messages.error(request, 'Invalid comment input.')
            return redirect("map")

    return redirect("dashboard")
    

@login_required(login_url="/signin")
def add_comment(request, post_id):
    if request.method =='POST':
        post=get_object_or_404(Post, pk=post_id)
        comment_user=request.user.userprofile
        text = request.POST.get('commentInput')

        if text:
            comment = PostComment.objects.create(post=post, user=comment_user, text=text)
            messages.success(request, 'Comment added successfully!')
            return redirect("dashboard")
        else:
            messages.error(request, 'Invalid comment input.')
            return redirect("map")

    return redirect("dashboard")


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

        like, created = PostLike.objects.get_or_create(post=post, user=user_profile)

        if not created:
            like.delete()
        else:
            pass  

        post.like_count = PostLike.objects.filter(post=post).count()
        post.save()

        response_data = {
            'message': 'Post liked successfully' if created else 'Post unliked successfully',
            'is_liked': not created,
            'like_count': post.like_count
        }

        return HttpResponse(json.dumps(response_data), content_type='application/json')

    return HttpResponse(json.dumps({'message': 'Invalid request method'}), content_type='application/json')




def change_password(request, username):
    auth_user = request.user
    print(auth_user)
    user = User.objects.get(username=username)

    error_message = None
    password_changed = False
    
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password1']
            
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)
            
            password_changed = True
        else:
            error_message = 'Please correct the errors below.'
            first_error = list(form.errors.values())[0][0]
    else:
        form = PasswordChangeForm(user=request.user)
    
    return render(request, 'change_password.html', {'form': form, 'password_changed': password_changed})

def report_post(request, post_id):
    if request.method == 'POST':
        reason = request.POST.get('reason', '')
        report = ReportedPost.objects.create(post_id=post_id, reason=reason)
        print(f"Reported post saved: {report}")

        return redirect('dashboard')
    return render(request, 'dashboard.html')



@require_POST
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.user.user != request.user:
        return HttpResponse(status=403)

    post.delete_post()

    return HttpResponse(status=200)

from django.shortcuts import redirect


def logout_view(request):
    logout(request)
    return redirect('index')  