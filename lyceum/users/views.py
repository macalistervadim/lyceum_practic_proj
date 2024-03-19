import django.conf
import django.contrib.auth
import django.contrib.auth.forms
import django.contrib.auth.tokens
import django.core.signing
import django.core.mail
import django.shortcuts
import django.template.loader
import django.utils.encoding
import django.utils.http
import django.utils.translation as translation
import django.urls
import django.http

import users.forms
import users.models

def registration(request):
    template = "users/signup.html"
    if request.method == 'POST':
        form = users.forms.SignUpForm(request.POST)
        signer = django.core.signing.TimestampSigner()
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = django.conf.settings.DEFAULT_USER_IS_ACTIVE
            user.is_staff = False
            user.save()

            signed_username = signer.sign(user.username)
            activate_link = request.build_absolute_uri(django.urls.reverse('users:activate', kwargs={'signed_username': signed_username}))
            django.core.mail.send_mail(
                subject="Активация профиля",
                message=django.template.loader.render_to_string('users/activation_email.txt', {'activate_link': activate_link}),
                from_email=django.conf.settings.EMAIL_HOST,
                recipient_list=[form.cleaned_data["email"]]
            )

            if django.conf.settings.DEFAULT_USER_IS_ACTIVE == True:
                django.contrib.messages.add_message(
                    request, django.contrib.messages.SUCCESS, translation.gettext_lazy("Вы зарегистрированы. Войдите с новыми данными")
                )
            else:
                django.contrib.messages.add_message(
                    request, django.contrib.messages.WARNING, translation.gettext_lazy("Вам необходимо активировать Ваш профиль. Проверьте указанную почту")
                )

            return django.shortcuts.redirect('users:login')
            
    else:
        form = users.forms.SignUpForm()
    context = {
        "form": form
    }
    return django.shortcuts.render(request, template, context)

def activate(request, signed_username):
    template = "users/activation_success.html"
    UserModel = django.contrib.auth.get_user_model()
    signer = django.core.signing.TimestampSigner()

    try:
        username = signer.unsign(signed_username, max_age=3600*12)
        user = UserModel.objects.get(username=username)
    except (django.core.signing.BadSignature, UserModel.DoesNotExist):
        return django.http.HttpResponseNotFound("Неверная или просроченная ссылка активации")



    user.is_active = True
    user.save()

    return django.shortcuts.render(request, template)

def user_list(request):
    template = "users/user_list.html"
    users = django.contrib.auth.get_user_model().objects.filter(is_active=True)
    
    context = {
        "user_list": users,
    }
    return django.shortcuts.render(request, template, context)

def user_detail(request, pk):
    template = "users/user_detail.html"
    user_info = django.shortcuts.get_object_or_404(users.models.Profile.objects.user_detail(pk))
    print(user_info)
    context = {
        "user": user_info,
    }
    return django.shortcuts.render(request, template, context)