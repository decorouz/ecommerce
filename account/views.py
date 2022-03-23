from django.http import HttpResponse
from django.shortcuts import redirect, render
from .forms import UserRegistrationForm, UserEditForm

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .tokens import account_activation_token
from django.conf import settings
from django.core.mail import send_mail
from .models import UserBase
from orders.views import user_orders


# Create your views here.


@login_required
def dashboard(request):
    orders = user_orders(request)
    return render(
        request, "account/user/dashboard.html", {"orders": orders}
    )


@login_required
def edit_details(request):

    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        print(user_form.is_valid())
        if user_form.is_valid():
            user_form.save()

    else:
        user_form = UserEditForm(instance=request.user)

    return render(
        request,
        "account/user/edit_details.html",
        {"user_form": user_form}
    )


@login_required
def delete_user(request):
    user = UserBase.objects.get(user_name=request.user)
    user.is_active = False
    user.save()
    logout(request)
    return redirect("account:delete_confirmation")


def account_register(request):

    if request.user.is_authenticated:
        return redirect("account:dashboard")

    if request.method == "POST":
        registerForm = UserRegistrationForm(request.POST)

        if registerForm.is_valid():
            email = request.POST.get("email")
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data["email"]
            user.set_password(registerForm.cleaned_data["password"])
            user.is_active = False
            user.save()

            # Setup Email
            current_site = get_current_site(request)
            subject = "Activate your Account"
            message = render_to_string(
                "account/registration/account_activation_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )
            try:
                send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)

                return render(request, "account/registration/activation_email_sent.html", {"user": user})
            except Exception as e:
                print(e)  # e.message
                HttpResponse("We have a connection problem.")
    else:
        registerForm = UserRegistrationForm()
    return render(request, "account/registration/register.html", {"form": registerForm})


def activation_email_sent(request):
    return render(request, "activation_email_sent.html")


def account_activate(request, uidb64, token, backend="django.contrib.auth.backends.ModelBackend"):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserBase.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserBase.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect("account:dashboard")
    else:
        return render(request, "account/registration/activation_invalid.html")
