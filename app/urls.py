from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("foods/", views.foods_index, name="index"),
    path("foods/create/", views.FoodCreate.as_view(), name="foods_create"),
    # accounts url patterns
    path('accounts/signup/', views.signup, name='signup'),
]