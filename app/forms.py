from dataclasses import field
import email
from django import forms
from django.contrib.auth.models import User, Group, Permission
from .models import Food, Household, Profile
from django.contrib.admin.widgets import FilteredSelectMultiple

class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user_image']

class GroupCreationForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = '__all__'
        widgets = {
            'permissions': FilteredSelectMultiple("Permission", False, attrs={'rows': 2})
        }
class FoodUpdateForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ['food_name', 'category', 'expiry', 'shareable', 'count', 'food_image']
        
