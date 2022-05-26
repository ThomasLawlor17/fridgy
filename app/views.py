from distutils.log import error
import re
import django
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView

# import login
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from urllib3 import HTTPResponse

from .models import Food, Household, Profile
from .forms import GroupCreationForm, UpdateUserForm, UpdateProfileForm, FoodUpdateForm

# Create your views here.
def home(request):
    return render(request, 'home.html')

# Food functions
# @login_required
def foods_index(request):
    household = Household.objects.get(id=request.user.profile.household.id)
    in_household = Profile.objects.filter(household=household).values_list('user')
    users = User.objects.filter(id__in = in_household)
    foods = Food.objects.filter(user__in=users)
    for food in foods:
        profile = Profile.objects.get(user=food.user)
        food.user_image = profile.user_image
    return render(request, 'foods/index.html', {'foods': foods})
# @login_required
def foods_detail(request, food_id):
    food = Food.objects.get(id=food_id)
    return render(request, 'foods/detail.html', { 'food': food })
def foods_edit(request, food_id):
    error_message = ''
    if request.method == 'POST':
        food = Food.objects.get(id=food_id)
        food_image = request.POST['food_image']
        shareable = request.POST.get('shareable', False)
        count = request.POST['count']
        food.shareable = shareable
        food.food_image = food_image
        food.count = count
        food.save()
        return redirect('/foods/')
    form = FoodUpdateForm()
    food = Food.objects.get(id=food_id)
    context = { 'form': form, 'error_message': error_message, 'food':food }
    return render(request, 'foods/edit.html', context)
# Food Class-based views

class FoodCreate(CreateView): # Add login mixin
    def check(self):
        print(self.request)
    model = Food
    fields = ["food_name","shareable", "food_image"]
    def form_valid(self, form):
        food = form.save(commit=False)
        food.user = self.request.user
        food.save()
        return redirect('/foods/')
        
# class FoodUpdate(UpdateView): # Add login mixin
#     model = Food
#     fields = ['food_name', 'category', 'expiry', 'shareable', 'count', 'food_image']
#     def form_valid(self, form):
#         food = form.save()
#         return redirect('/foods/')
class FoodDelete(DeleteView): # Add login mixin
    model = Food
    success_url = '/foods/' # Go back to all

# Household functions

# Auth functions



# @login_required
def household_index(request):
    household = Household.objects.all()
    return render(request, 'households/index.html', {'household': household})
# @login_required
def household_detail(request, household_id):
    error_message = ''
    if request.user.profile.household == Household.objects.get(id=household_id):
        household = Household.objects.get(id=household_id)
        users_in_house = Profile.objects.filter(household=household_id)
        return render(request, 'households/detail.html', { 'household': household, 'users_in_house': users_in_house })
    else:
        error_message = 'You are not in this household'
        return redirect('home') # Change later?
def household_edit(request, household_id):
    error_message = ''
    if request.user.profile.household == Household.objects.get(id=household_id):
        household = Household.objects.get(id=household_id)
        users_in_house = Profile.objects.filter(household=household_id)
        users_not_in_house = Profile.objects.filter(household=None)
        return render(request, 'households/edit.html', {'household': household, 'users_in_house': users_in_house, 'users_not_in_house': users_not_in_house})
    else:
        error_message = 'You are not in this household'
        return redirect('home') # Change later?
def household_update(request, household_id):
    error_message = ''
    if request.method == 'POST':
        user = User.objects.get(username=request.POST['user'])
        household = Household.objects.get(id=household_id)
        user.profile.household = household
        user.save()
        user.profile.save()
    else:
        error_message = 'Something went wrong - please try again'
    return redirect('household_edit', household_id=household_id)
def household_remove_user(request, household_id):
    error_message = ''
    if request.user.profile.household == Household.objects.get(id=household_id):
        if request.user.profile.household_manager:
            if request.method == 'POST':
                user = User.objects.get(username=request.POST['user'])
                user.profile.household = None
                user.save()
                user.profile.save()
            else:
                error_message = 'Something went wrong - Please try again'
        else:
            error_message = 'You are not allowed to remove members of this household'
    else:
        error_message = 'You cannot remove people from this household'
    return redirect('household_edit', household_id=household_id)

# Household class-based views

class HouseholdCreate(CreateView): # Add login mixin
    model = Household
    fields = ['name']

    def form_valid(self, form):
        user = self.request.user
        user.profile.household_manager = True
        household = form.save(commit=False)
        user.profile.household = household
        user.save()
        household.save()
        user.profile.save()
        return redirect(f'/household/{household.pk}/')
class HouseholdDelete(DeleteView): # Add login mixin
    model = Household
    def remove_manager(self):
        profile = self.request.user
        profile.household_manager = False
        profile.save()
        return redirect('home')
    success_url = '/'
    


# Authorization functions
def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)
            return redirect(f'/profile/{user.pk}')
        else:
            error_message = 'Something went wrong - please try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

def login_success(request):
    if request.user.profile.household:
        return redirect('index')
    else:
        return redirect('household_create')
# @login_required
def profile_detail(request, user_id):
    profile = Profile.objects.get(user=user_id)
    user = User.objects.get(id=user_id)
    return render(request, 'profile/detail.html', {'profile': profile, 'user': user})
# @login_required
def profile_edit(request, user_id):
    profile = Profile.objects.get(user=user_id)
    user = User.objects.get(id=user_id)
    update_user_form = UpdateUserForm()
    update_profile_form = UpdateProfileForm
    return render(request, 'profile/edit.html', {'user': user, 'profile': profile, 'update_user_form': update_user_form, 'update_profile_form': update_profile_form})
# @login_required
def profile_update(request, user_id):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        user_image = request.POST['user_image']
        myuser = User.objects.get(pk=user_id)
        myuser.username = username
        myuser.email = email
        myuser.first_name = first_name
        myuser.last_name = last_name
        profile = Profile.objects.get(user=user_id)
        profile.user_image = user_image
        myuser.save()
        profile.save()
    return redirect('profile_detail', user_id=user_id)

def change_password(request):
    return render(request, 'registration/change_password.html')

def change_password_done(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('profile_detail', user_id=request.user.id)
        else:
            print(form.is_valid())
            print("ERROR: ", form.errors)
            return render(request, 'registration/change_password.html', {'form': form})

def group_create(request):
    error_message = ''
    if request.method == 'POST':
        form = GroupCreationForm(request.POST)
        if form.is_valid():
            household = form.save()
            household.user_set.add(request.user)
            return redirect(f'/household/{household.pk}')
        else:
            error_message = 'Something went wrong - Please try again'
    form = GroupCreationForm()
    context = {'form': form, 'error_messsage': error_message}
    return render(request, 'group/create.html', context)
def group_detail(request, group_id):
    group = Group.objects.get(id=group_id)
    users = list(group.user_set.values_list('username', flat=True))
    user = User.objects.get(id=request.user.id)
    return render(request, 'group/detail.html', {'user': user, 'group': group, 'users': users})
# Class Views
class ProfileDelete(DeleteView): # Add login mixin
    model = User
    success_url = '/'
    
    
    




