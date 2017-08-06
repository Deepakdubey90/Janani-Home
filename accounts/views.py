# @Author: Tushar Agarwal(tusharcoder) <tushar>
# @Date:   2017-07-23T11:01:58+05:30
# @Email:  tamyworld@gmail.com
# @Filename: views.py
# @Last modified by:   tushar
# @Last modified time: 2017-08-06T15:22:56+05:30



from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import ugettext_lazy as _
from .forms import SignupForm, UserCompletionForm, ProfileCompletionForm
from .forms import ProfileForm, UserForm, PasswordChangeForm
from .tokens import account_activation_token
from educational_need.models import EducationalNeed
import json
from .models import State


def signup(request):
    if request.user.is_authenticated():
        return redirect('view_profile')
    else:
        if request.method == 'POST':
            form = SignupForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                subject = 'Activate your account on Janani Care.'
                message = render_to_string('accounts/activation_email.html', {
                    'user':user, 'domain':current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                toemail = form.cleaned_data.get('email')
                email = EmailMessage(subject, message, to=[toemail])
                email.send()
                return render(request, 'accounts/activation_pending.html')
        else:
            form = SignupForm()
        return render(request, 'accounts/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if request.method == 'POST':
        user_form = UserCompletionForm(request.POST, instance=user)
        profile_form = ProfileCompletionForm(request.POST, instance=user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user.is_active = True
            user_form.save()
            profile_form.save()
            login(request, user)
            return render(request, 'accounts/activation_completed.html')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserCompletionForm()
        profile_form = ProfileCompletionForm()
        if user is not None and account_activation_token.check_token(user, token):
            pass
        else:
            return HttpResponse('Activation link is invalid!')
    return render(request, 'accounts/complete_registration.html',
                  {'user_form': user_form, 'profile_form': profile_form})


@login_required
def view_profile(request):
    educational_needs = EducationalNeed.objects.filter(user=request.user)
    template = 'accounts/view_profile.html'
    context = {'educational_needs': educational_needs}
    return render(request, template, context)


@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('Your profile was successfully updated!'))
            return redirect('view_profile')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'accounts/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


@login_required
@transaction.atomic
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form
    })

def StateAjaxView(request):
    """function to render the states accourding to the city passed"""
    try:
        country_id = request.GET.get('country_id')
        return HttpResponse(json.dumps(tuple(i for i in State.objects.filter(country_id=country_id).values('name','id','code'))),content_type='application/json')
    except Exception as e:
        return HttpResponse(json.dumps([]),content_type='application/json')
