from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.urls import reverse_lazy
from members.forms import SignUpForm, EditProfileForm, PasswordChangingForm, ProfilePageForm
from django.contrib.auth.views import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.views.generic import DetailView, CreateView
from the_blog.models import Profile

class EditProfilePageView(generic.UpdateView):
    model = Profile
    template_name = 'registration/edit_profile_page.html'
    fields = ['bio', 'website_url', 'profile_pic', 'fb_url', 'instagram_url', 'twitter_url', 'pintrest_url']
    success_url = reverse_lazy('home')



class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'registration/user_profile.html'

    def get_context_data(self, *args,  **kwargs):
        users =  Profile.objects.all()
        context = super(ShowProfilePageView, self).get_context_data(*args,  **kwargs)
        page_user = get_object_or_404(Profile, id=self.kwargs['pk'])
        context["page_user"] = page_user
        return context


class CreateProfilePageView(CreateView):
    model = Profile
    template_name = 'registration/create_user_profile_page.html'
    form_class = ProfilePageForm

    def form_valid(self, form):
        form.instance.user = self.request.user  # Assign the current user to the profile
        return super().form_valid(form)




class PasswordsChangeView(PasswordChangeView):
	form_class = PasswordChangingForm
	#form_class = PasswordChangeForm
	success_url = reverse_lazy('password_success')
	#success_url = reverse_lazy('home')

def password_success(request):
	return render(request, 'registration/password_success.html', {})

class UserRegisterView(generic.CreateView):
    form_class = SignUpForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

class UserEditView(generic.UpdateView):
    form_class = EditProfileForm
    template_name = 'registration/edit_profile.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user
