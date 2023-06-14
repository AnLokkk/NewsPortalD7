from django.urls import path
from .views import upgrade_user


urlpatterns = [
    path('', upgrade_user, name='acc_upgrade')
]