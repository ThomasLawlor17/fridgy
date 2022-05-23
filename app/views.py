from django.shortcuts import redirect, render


# import login
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import UpdateView, CreateView, DeleteView
from .models import Food

# Create your views here.
def home(request):
    return render(request, 'home.html')

class FoodCreate(LoginRequiredMixin, CreateView):


    model = Food
    fields = ["food_name", "category", "expiry", "shareable", "count"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


def foods_index(request):
    foods = Food.objects.all
    return render(request, 'foods/index.html', {"foods": foods})

# Authorization functions
def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Something went wrong - please try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)
