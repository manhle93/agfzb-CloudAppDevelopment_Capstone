from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf
# Get an instance of a logger
logger = logging.getLogger(__name__)




def about(request):
    if request.method == "GET":
        return render(request, 'djangoapp/about.html')


def contact(request):
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html')


def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['error_message'] = "Invalid login credentials"
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)



def logout_request(request):
    print("Log out the user `{}`".format(request.user.username))
    logout(request)
    return redirect('djangoapp:index')


def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        user_exist = False
        try:
            username = request.POST.get('username')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            psw = request.POST.get('psw')

            User.objects.get(username=username)
            user_exist = True
        except:
            logger.debug("{} is new user".format(username))
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=psw)

            return redirect("djangoapp:index")
        else:
          return render(request, 'djangoapp/registration.html', context)


def get_dealerships(request):
    if request.method == "GET":
        context = {}
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/fb925856-28f3-467e-95f7-39098f6cd9da/dealership-package/get-dealership"
        dealerships = get_dealers_from_cf(url)
        context['dealership_list'] = dealerships
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        return render(request, 'djangoapp/index.html', context)


def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/fb925856-28f3-467e-95f7-39098f6cd9da/dealership-package/get_reviews"
        context = {}
        reviews = get_dealer_reviews_from_cf(url, dealer_id=dealer_id)
        context['reviews'] = reviews
        return render(request, 'djangoapp/dealer_details.html', context)

def add_review(request, dealer_id):
   if request.method == "POST":
        review = {}
        review["time"] = datetime.utcnow().isoformat()
        review["dealership"] = dealer_id
        review["review"] = request.POST.get("review")

        url = "https://us-south.functions.appdomain.cloud/api/v1/web/fb925856-28f3-467e-95f7-39098f6cd9da/dealership-package/post-review" 
        json_payload["review"] = review
        post_request(url, json_payload, dealerId=dealer_id)

