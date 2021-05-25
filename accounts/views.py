from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http.response import Http404
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
import os
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.shortcuts import render


TEMP_PROFILE_IMAGE_NAME = "temp_profile_image.png"


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'registration/signup.html'


class UserView(ListView):
    model = CustomUser
    template_name = 'registration/account.html'



class UserUpdate(UpdateView, LoginRequiredMixin, UserPassesTestMixin):
    form_class = CustomUserChangeForm
    model = CustomUser
    template_name = 'registration/edit_account.html'
    pk_url_kwarg = 'user_id'


    def delete_profile_image(self, user_id):
        try:
            user = get_object_or_404(CustomUser, id=user_id)
            profile_image = user.profile_image
            if profile_image != 'images/accounts/profiles/default_image.jpg':
                profile_image.delete(save=False)
                os.rmdir('media/images/accounts/profiles/%s' % user_id)
                CustomUser.objects.filter(pk=user_id).update(profile_image='images/accounts/profiles/default_image.jpg')
                return HttpResponseRedirect(reverse('accounts:user_view', args=[str(user.pk)]))
            else:
                return HttpResponseRedirect(reverse('accounts:user_view', args=[str(user.pk)]))
                

        except CustomUser.DoesNotExist:
            raise Http404("No User matches the given query.")
    





    


    









 