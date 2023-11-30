from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from socialnetwork.forms import LoginForm, RegisterForm, AddPostForm, ProfileForm, ProfileItemForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponse, Http404
from django.utils import timezone
from django.core.serializers import serialize
from django.utils.decorators import method_decorator
from django.utils import formats
from django.http import JsonResponse
from datetime import datetime
from socialnetwork.models import Post, Profile, Comment, RequestData, InventoryItem
from socialnetwork.MyMemoryList import MyMemoryList
import string
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from django.views.decorators.csrf import ensure_csrf_cookie
import json


#from celery import Celery

ENTRY_LIST = MyMemoryList()
# Create your views here.
def login_action(request):
    context = {}
    if(request.method == "GET"):
        form = LoginForm()    
        context["form"] = form
        context["id_page_name"] = "Login"
        return render(request, "socialnetwork/login.html", context)

    form = LoginForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        context["id_page_name"] = "Login"
        return render(request, 'socialnetwork/login.html', context)
    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

    login(request, new_user)
    return redirect(reverse('globalstream'))


def get_inventory_item_by_id(request, id):
    item = get_object_or_404(InventoryItem, id=id)
    serialized_data = serialize('json', [item])
    python_data = json.loads(serialized_data)
    return JsonResponse(python_data[0]['fields'])

def get_list_json_dumps_serializer(request):
    # To make quiz11 easier, we permit reading the list without logging in. :-)
    if not request.user.id:
        return _my_json_error_response("You must be logged in to do this operation", status=401)
    response_data = []
    for model_item in Post.objects.all():
        my_item = create_post_item(model_item)
        response_data.append(my_item)
    comments_data = []
    for model_item in Comment.objects.all():
        comment_item = create_comment_item(model_item)
        comments_data.append(comment_item)
    
    response_json = json.dumps({"posts":response_data, "comments":comments_data})
    return HttpResponse(response_json, content_type='application/json')

@csrf_exempt
def inventory_add(request, *args, **kwargs):
    print("entering function")
    try:
        data = json.loads(request.body.decode('utf-8'))
        product_name = data.get('product_name')
        farmer_name = data.get("farmer_name")
        quantity = data.get('quantity')
        expiry_date = data.get('expiry_date')

        # Use get_or_create directly to simplify the code
        inventory_item, created = InventoryItem.objects.get_or_create(
            product_name=product_name,
            farmer_name=farmer_name,
            defaults={'quantity': quantity, 'expiry_date': expiry_date}
        )

        # Update timestamp and expiry_date
        inventory_item.quantity += int(quantity)
        inventory_item.timestamp = datetime.now()
        inventory_item.expiry_date = datetime.now()
        inventory_item.save()

        return JsonResponse({'message': 'Inventory item added successfully'})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)



@csrf_exempt
def order_item(request, *args, **kwargs):
    try:
        data = json.loads(request.body.decode('utf-8'))
        product_name = data.get('product_name')
        farmer_name = data.get("farmer_name")
        quantity_ordered = data.get('quantity')

        # Retrieve the inventory item
        inventory_item = InventoryItem.objects.get(product_name=product_name, farmer_name=farmer_name)

        # Check if there is enough quantity to fulfill the order
        if inventory_item.quantity >= int(quantity_ordered):
            # Update quantity, timestamp, and expiry_date
            inventory_item.quantity -= int(quantity_ordered)
            inventory_item.timestamp = datetime.now()
            inventory_item.expiry_date = datetime.now()
            inventory_item.save()

            RequestData.objects.create(
                product_name=product_name,
                farmer_name=farmer_name,
                quantity=int(quantity_ordered)
            )

            return JsonResponse({'message': 'Order placed successfully'})

        else:
            return JsonResponse({'error': 'Not enough quantity in inventory'}, status=400)

    except InventoryItem.DoesNotExist:
        return JsonResponse({'error': 'Item not found in inventory'}, status=404)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
def get_follower_data(request):
    response_data = []
    post_ids = []
    for model_item in Post.objects.all():
        if(model_item.user in request.user.profile.following.all()):
            my_item = create_post_item(model_item)
            post_ids.append(model_item.id)
            response_data.append(my_item)
    comments_data = []
    for model_item in Comment.objects.all():
        if(model_item.post.id in post_ids):
            comment_item = create_comment_item(model_item)
            comments_data.append(comment_item)
    
    response_json = json.dumps({"posts":response_data, "comments":comments_data})
    return HttpResponse(response_json, content_type='application/json')
    

def create_comment_item(new_comment):
    comment_item = {
                'comment_id': new_comment.id,
                'post_id': new_comment.post.id,
                'comment_text': new_comment.text,
                'creator_first_name': new_comment.creator.first_name,
                'creator_last_name': new_comment.creator.last_name,
                'creator_id': new_comment.creator.id,
                'comment_time': timezone.localtime(new_comment.creation_time).isoformat()

    }
    return comment_item

def create_post_item(model_item):
    my_item = {
                'id': model_item.id,
                'text': model_item.text,
                'user_id' : model_item.user.id,
                'user': model_item.user.username,
                'first_name' : model_item.user.first_name,
                'last_name' : model_item.user.last_name,
                'date_time': timezone.localtime(model_item.date_time).isoformat()
    }
    return my_item

@csrf_exempt
def request_list(request):
    requests = RequestData.objects.all()
    return render(request, 'socialnetwork/request_list.html', {'requests': requests})

@csrf_exempt
def inventory_list(request):
    requests = InventoryItem.objects.all()
    return render(request, 'socialnetwork/inventory_list.html', {'requests': requests})


def get_inventory_list(request):
    inventory_items = InventoryItem.objects.all()
    serialized_data = serialize('json', inventory_items)
    python_data = json.loads(serialized_data)
    return JsonResponse({'inventory_items': python_data}, safe=False)


def _my_json_error_response(message, status=200):
    # You can create your JSON by constructing the string representation yourself (or just use json.dumps)
    response_json = '{ "error": "' + message + '" }'
    return HttpResponse(response_json, content_type='application/json', status=status)

def add_comment(request):
    if not request.user.id:
        return _my_json_error_response("You must be logged in to do this operation", status=401)

    if request.method != 'POST':
        return _my_json_error_response("You must use a POST request for this operation", status=405)

    try:
        post = Post.objects.get(id=request.POST['post_id'])
    except:
        return _my_json_error_response("Must have a valid post id.", status=400)
    if not 'comment_text' in request.POST or not request.POST['comment_text']:
        return _my_json_error_response("You must enter an item to add.", status=400)
    
    if not 'post_id' in request.POST or not request.POST['post_id'] or not request.POST["post_id"].isnumeric():
        return _my_json_error_response("Must have a valid post id.", status=400)

    associated_post = get_object_or_404(Post, id=request.POST["post_id"])
    new_comment = Comment(text= request.POST['comment_text'],creator= request.user, creation_time = timezone.now(),post = associated_post)
    new_comment.save()
    comments_response_data = []
    comment_item = create_comment_item(new_comment)
    comments_response_data.append(comment_item)
    json_dumped = json.dumps({"posts":[], "comments":comments_response_data})
    print(json_dumped)
    return HttpResponse(json_dumped, content_type='application/json')

def logout_action(request):
    logout(request)
    return redirect(reverse('login'))


@login_required
def get_photo(request, id):
    item = get_object_or_404(Profile, id=id)
    print('Picture #{} fetched from db: {} (type={})'.format(id, item.picture, type(item.picture)))

    # Maybe we don't need this check as form validation requires a picture be uploaded.
    # But someone could have delete the picture leaving the DB with a bad references.
    if not item.picture:
        raise Http404

    return HttpResponse(item.picture, content_type=item.content_type)

def register_action(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = RegisterForm()
        context["id_page_name"] = "Register"
        return render(request, 'socialnetwork/register.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    form = RegisterForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        context["id_page_name"] = "Register"
        return render(request, 'socialnetwork/register.html', context)

    # At this point, the form data is valid.  Register and login the user.
    new_user = User.objects.create_user(username=form.cleaned_data['username'], 
                                        password=form.cleaned_data['password'],
                                        email=form.cleaned_data['email'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'])
    new_user.save()
    new_profile = Profile.objects.create(user=new_user)
    new_profile.save()

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

    login(request, new_user)
    return redirect(reverse('globalstream'))

@login_required
def globalstream_action(request):
    context = {}
    context["id_page_name"] = "Global Stream"
    # Just display the registration form if this is a GET request.    
    if request.method == 'GET':
        context["posts"] = Post.objects.all().order_by('-date_time')
        return render(request, 'socialnetwork/globalstream.html', context)
    if 'id_post_input_text' not in request.POST or not request.POST['id_post_input_text']:
        return render(request, 'socialnetwork/globalstream.html', context)
    new_post = Post(text=request.POST["id_post_input_text"], user=request.user, date_time = timezone.now())
    new_post.save()
    context["posts"] = Post.objects.all().order_by('-date_time')
    return render(request, 'socialnetwork/globalstream.html', context)

''' @login_required
def profile_action(request):
    context = {}
    if request.method == 'GET':
        context['form'] = ProfileForm()
        context['id_page_name'] = "Profile Page for "
        return render(request, 'socialnetwork/profile.html', context)
    
    form = ProfileForm(request.POST)
    context['form'] = form
    if not form.is_valid():
        return render(request, 'socialnetwork/profile.html', context)
    context["id_page_name"] = "Profile Page for "
    return render(request, 'socialnetwork/profile.html', context) '''

@login_required
def other_profile_action(request, id):
    item = get_object_or_404(User, id=id)
    return render(request, "socialnetwork/otherprofile.html", {"profile":item.profile})


@login_required
def unfollow(request, id):
    user_to_unfollow = get_object_or_404(User, id=id)
    if(request.user != user_to_unfollow):
        request.user.profile.following.remove(user_to_unfollow)
        request.user.profile.save()
    return redirect(reverse('otherprofile', kwargs={'id': id}))
    #return render(request, "socialnetwork/otherprofile.html", {"profile": request.user.profile})

@login_required
def follow(request, id):
    user_to_follow = get_object_or_404(User, id=id)
    if(request.user != user_to_follow):
        request.user.profile.following.add(user_to_follow)
        request.user.profile.save()
    return redirect(reverse('otherprofile', kwargs={'id': id}))
    #return render(request, "socialnetwork/otherprofile.html", {"profile": request.user.profile})

@login_required
def profile_action(request):
    item = get_object_or_404(Profile, id=request.user.id)
    if request.method == 'GET':
        # context = { 'item': item, 'form': PicItemForm(instance=item) }
        context = { 'profile': request.user.profile, 'form': ProfileItemForm(initial={'bio': request.user.profile.bio}) }
        return render(request, 'socialnetwork/profile.html', context)

    form = ProfileItemForm(request.POST, request.FILES)
    if not form.is_valid():
        print("not valid")
        context = { 'profile': request.user.profile, 'form': form }
        return render(request, 'socialnetwork/profile.html', context)

    item.picture = form.cleaned_data['picture']
    item.content_type = form.cleaned_data['picture'].content_type
    item.bio = form.cleaned_data['bio']
    item.save()
    context = {
        'profile': item,
        'form': form,
        'message': 'Profile #{} updated.'.format(request.user.first_name),
    }
    print(context)
    return render(request, 'socialnetwork/profile.html', context)

@login_required
def followerstream_action(request):
    context = {}
    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['id_page_name'] = "Follower Stream" 
        context["posts"] = Post.objects.all().order_by('-date_time')
        return render(request, 'socialnetwork/followerstream.html', context)
    context["posts"] = Post.objects.all().order_by('-date_time')
    return render(request, 'socialnetwork/followerstream.html', context)


    
