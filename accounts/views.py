from django.contrib.auth.models import User, Group
from django.views.generic.edit import CreateView
from allauth.account.forms import SignupForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from News.models import Author

@login_required()
def upgrade_user(request):
    user = request.user
    group = Group.objects.get(name='authors')
    group.user_set.add(user)
    Author.objects.create(authorUser=User.objects.get(pk=user.id))
    return redirect('http://127.0.0.1:8000/NEWS/')



class SignUp(CreateView):
    model = User
    form_class = SignupForm
    success_url = '/accounts/login'
    template_name = 'registration/signup.html'