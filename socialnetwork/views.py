from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.http import HttpResponse, Http404
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.utils import timezone

from socialnetwork.forms import EntryForm, LoginForm, RegisterForm, CreatePost, CreateProfile
from socialnetwork.models import Post, Profile, Comment

from socialnetwork.MyMemoryList import MyMemoryList

import json, datetime

ENTRY_LIST = MyMemoryList()

# Create your views here.
def login_action(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = LoginForm()
        return render(request, 'socialnetwork/login.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    form = LoginForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'socialnetwork/login.html', context)

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

    login(request, new_user)
    return redirect(reverse('home'))

def register_action(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = RegisterForm()
        return render(request, 'socialnetwork/register.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    form = RegisterForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'socialnetwork/register.html', context)

    # At this point, the form data is valid.  Register and login the user.
    new_user = User.objects.create_user(username=form.cleaned_data['username'], 
                                        password=form.cleaned_data['password'],
                                        email=form.cleaned_data['email'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'])
    new_user.save()

    new_profile = Profile(user = new_user)
    create_profile = CreateProfile(request.POST,instance=new_profile)
    new_profile.save()

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

    login(request, new_user)
    return redirect(reverse('home'))

def logout_action(request):
    logout(request)
    return redirect(reverse('login'))


@login_required
def global_stream(request):
    
    context = {}
    # objects = Post.objects.all()
    # if objects.count() > 0:
    #     context = {'posts': objects.order_by('-post_time')}
    
    context['form'] = CreatePost()
    if request.method == 'GET':
        return render(request,'socialnetwork/global_stream.html', context)
    
    post = Post()
    post.post_author = request.user
    post.post_time = timezone.now()

    create_post = CreatePost(request.POST, instance=post)
    if not create_post.is_valid():
        context = {'form': create_post}
        return render(request, 'socialnetwork/global_stream.html', context)
    # post.post_time = post.post_time.strftime("%d/%m/%y %H:%M %p") 
    create_post.save()
    message = 'Post created'
    context['message'] =  message
    # objects = Post.objects.all()
    # context['posts'] = objects.order_by('-post_time')

    return render(request, 'socialnetwork/global_stream.html', context)

@login_required
def follower_stream(request):
    context = {}
    # this_profile = get_object_or_404(Profile, user = request.user)
    # users_iter = []
    # followings = this_profile.following.all().iterator()
    # for following in followings:
    #     users_iter.append(following.user)
    # objects = Post.objects.filter(post_author__in = users_iter)
    # if objects.count() > 0:
    #     context = {'posts': objects.order_by('-post_time')}

    return render(request,'socialnetwork/follower_stream.html', context)
    


@login_required
def get_photo(request, id):
    user = get_object_or_404(User, id=id)
    item = get_object_or_404(Profile, user = user.id)
    # print('id = ', id)
    # print('Picture #{} fetched from db: {} (type={})'.format(id, item.user_picture, type(item.user_picture)))

    # Maybe we don't need this check as form validation requires a picture be uploaded.
    # But someone could have delete the picture leaving the DB with a bad references.
    if not item.profile_picture:
        raise Http404

    return HttpResponse(item.profile_picture, content_type=item.content_type)

@login_required
def my_profile(request):
    this_profile = get_object_or_404(Profile, user = request.user)
    followings = this_profile.following.all()

    if request.method == 'GET':
        context = {'profile': this_profile, 
        'form': CreateProfile(initial={'bio_input_text': this_profile.bio_input_text}),
        'followings': followings.iterator()}
        return render(request,'socialnetwork/my_profile.html', context)

    create_profile = CreateProfile(request.POST, request.FILES)
    if not create_profile.is_valid():
        print('not valid')
        context = {'profile': this_profile, 'form': create_profile,'followings': followings.iterator()}
        return render(request,'socialnetwork/my_profile.html', context)
    this_profile.profile_picture = create_profile.cleaned_data['profile_picture']
    this_profile.content_type = create_profile.cleaned_data['profile_picture'].content_type
    this_profile.bio_input_text = create_profile.cleaned_data['bio_input_text']
    this_profile.user = request.user
    # for following in create_profile.cleaned_data['following']:
    #     this_profile.following.add(following)
    this_profile.save()
    context = {
        'followings': followings.iterator(),
        'message': "Profile updated",
        'profile': this_profile,
        'form': CreateProfile(initial={'bio_input_text': this_profile.bio_input_text}),
    }

    return render(request, 'socialnetwork/my_profile.html', context)

@login_required
def other_profile(request, id):
    this_profile = get_object_or_404(Profile, user = request.user)
    other_user = get_object_or_404(User, id = id)
    if other_user == request.user:
        return my_profile(request)

    user_profile = get_object_or_404(Profile, user = other_user)
    followed = False
    if this_profile.following.filter(id = id).exists():
        followed = True

    if request.method == 'GET':
        context = {'profile': user_profile, 'followed': followed}
        return render(request,'socialnetwork/other_profile.html', context)

    if followed:
        this_profile.following.remove(user_profile)
        print("follow action:", request.user.id, "has followed", id)
    else:
        this_profile.following.add(user_profile)
        print("follow action:", request.user.id, "has unfollowed", id)
    this_profile.save()
    
    for f in this_profile.following.all().iterator():
        print(f.user)

    context = {
        'message': 'updated',
        'profile': user_profile,
        'followed': not followed,
    }

    return render(request, 'socialnetwork/other_profile.html', context)


@login_required
def refresh_gloabl_json_dumps_serializer(request):
    response_data = {}
    comment_data = []
    post_data = []
    for comment in Comment.objects.all():
        this_profile = get_object_or_404(Profile, user = comment.comment_author)

        if not this_profile.profile_picture:
            profile_pic = 'false'
        else:
            profile_pic = 'true'
        comment_obj = {
            'id': comment.id,
            'post_id': comment.comment_post.id,
            'user_id': comment.comment_author.id,
            'first_name': comment.comment_author.first_name,
            'last_name': comment.comment_author.last_name,
            'comment_text': comment.comment_input_text,
            'comment_time': comment.comment_time.isoformat(),
            'profile_pic':profile_pic,
        }
        comment_data.append(comment_obj)
    for post in Post.objects.all().order_by('post_time'):
        this_profile = get_object_or_404(Profile, user = post.post_author)

        if not this_profile.profile_picture:
            profile_pic = 'false'
        else:
            profile_pic = 'true'
        post_obj = {
            'id': post.id,
            'user_id': post.post_author.id,
            'first_name': post.post_author.first_name,
            'last_name': post.post_author.last_name,
            'post_text': post.post_input_text,
            'post_time': post.post_time.isoformat(),
            'profile_pic':profile_pic,
        }
        post_data.append(post_obj)

    response_data["post"] = post_data
    response_data["comment"] = comment_data
    response_json = json.dumps(response_data)
    response = HttpResponse(response_json, content_type='application/json')
    #  response['Access-Control-Allow-Origin'] = '*'
    return response


@login_required
def refresh_follower_json_dumps_serializer(request):
    response_data = {}
    comment_data = []
    post_data = []
    users_iter = []
    try:
        its_profile = Profile.objects.get(user = request.user)
    except ObjectDoesNotExist:
        return _my_json_error_response("Profile with id={request.user.id} does not exist.", status=404)
    followings = its_profile.following.all().iterator()
    for following in followings:
        users_iter.append(following.user)
    post_objects = Post.objects.filter(post_author__in = users_iter)
    comment_objects = Comment.objects.filter(comment_post__in = post_objects)

    for comment in comment_objects:
        this_profile = get_object_or_404(Profile, user = comment.comment_author)

        if not this_profile.profile_picture:
            profile_pic = 'false'
        else:
            profile_pic = 'true'
        comment_obj = {
            'id': comment.id,
            'post_id': comment.comment_post.id,
            'user_id': comment.comment_author.id,
            'first_name': comment.comment_author.first_name,
            'last_name': comment.comment_author.last_name,
            'comment_text': comment.comment_input_text,
            'comment_time': comment.comment_time.isoformat(),
            'profile_pic':profile_pic,
        }
        comment_data.append(comment_obj)
    for post in post_objects.order_by('post_time'):
        this_profile = get_object_or_404(Profile, user = post.post_author)

        if not this_profile.profile_picture:
            profile_pic = 'false'
        else:
            profile_pic = 'true'
        post_obj = {
            'id': post.id,
            'user_id': post.post_author.id,
            'first_name': post.post_author.first_name,
            'last_name': post.post_author.last_name,
            'post_text': post.post_input_text,
            'post_time': post.post_time.isoformat(),
            'profile_pic':profile_pic,
        }
        post_data.append(post_obj)

    response_data["post"] = post_data
    response_data["comment"] = comment_data
    response_json = json.dumps(response_data)
    response = HttpResponse(response_json, content_type='application/json')
    #  response['Access-Control-Allow-Origin'] = '*'
    return response


def _my_json_error_response(message, status=200):
    # You can create your JSON by constructing the string representation yourself (or just use json.dumps)
    response_json = '{ "error": "' + message + '" }'
    return HttpResponse(response_json, content_type='application/json', status=status)

@login_required
def add_comment(request):
    if request.method != 'POST':
        return _my_json_error_response("You must use a POST request for this operation", status=404)

    if not 'comment_text' in request.POST or not request.POST['comment_text']:
        return _my_json_error_response("You must enter some text to comment.")
    if not 'post_id' in request.POST or not request.POST['post_id'] or not request.POST['post_id'].isnumeric():
        return _my_json_error_response("You must indicate which post to comment.")

    try:
        its_post = Post.objects.get(id=request.POST['post_id'])
    except ObjectDoesNotExist:
        return _my_json_error_response("Post with id={equest.POST['post_id']} does not exist.", status=404)

    new_comment = Comment(
        comment_post = its_post,
        comment_author = request.user,
        comment_input_text = request.POST['comment_text'],
        comment_time = timezone.now(),
    )
    try:
        new_comment.save()
    except:
        return _my_json_error_response("Failed to create new comment for post with id={its_post.id}", status=404)


    comment_data = []
    this_profile = get_object_or_404(Profile, user = new_comment.comment_author)

    if not this_profile.profile_picture:
        profile_pic = 'false'
    else:
        profile_pic = 'true'
    added_comment = {
        'id': new_comment.id,
        'post_id': new_comment.comment_post.id,
        'user_id': new_comment.comment_author.id,
        'first_name': new_comment.comment_author.first_name,
        'last_name': new_comment.comment_author.last_name,
        'comment_text': new_comment.comment_input_text,
        'comment_time': new_comment.comment_time.isoformat(),
        'profile_pic': profile_pic,
    }
    comment_data.append(added_comment)
    response_data = {'comment': comment_data}
    response_json = json.dumps(response_data)
    print("in views sent:", response_data)
    response = HttpResponse(response_json, content_type='application/json')

    return response




