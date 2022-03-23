from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from orders.views import user_orders

from .forms import UserAddressForm, UserEditForm, UserRegistrationForm
from .models import Address, Customer
from .tokens import account_activation_token

# Create your views here.


@login_required
def dashboard(request):
    orders = user_orders(request)
    return render(request, "account/dashboard/dashboard.html", {"orders": orders})


@login_required
def edit_details(request):

    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        print(user_form.is_valid())
        if user_form.is_valid():
            user_form.save()

    else:
        user_form = UserEditForm(instance=request.user)

    return render(request, "account/dashboard/edit_details.html", {"user_form": user_form})


@login_required
def delete_user(request):
    user = Customer.objects.get(user_name=request.user)
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
        user = Customer.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Customer.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect("account:dashboard")
    else:
        return render(request, "account/registration/activation_invalid.html")


# Address


@login_required
def view_address(request):
    addresses = Address.objects.filter(customer=request.user)
    return render(request, "account/dashboard/addresses.html", {"addresses": addresses})


@login_required
def add_address(request):
    if request.method == "POST":
        address_form = UserAddressForm(data=request.POST)
        if address_form.is_valid():
            address_form = address_form.save(commit=False)
            address_form.customer = request.user
            address_form.save()
            return HttpResponseRedirect(reverse("account:addresses"))
    else:
        address_form = UserAddressForm()
    return render(request, "account/dashboard/edit_addresses.html", {"form": address_form})


@login_required
def edit_address(request, id):
    if request.method == "POST":
        address = Address.objects.get(pk=id, customer=request.user)
        address_form = UserAddressForm(instance=address, data=request.POST)
        if address_form.is_valid():
            address_form.save()
            return HttpResponseRedirect(reverse("account:addresses"))
    else:
        address = Address.objects.get(pk=id, customer=request.user)
        address_form = UserAddressForm(instance=address)
    return render(request, "account/dashboard/edit_addresses.html", {"form": address_form})


@login_required
def delete_address(request, id):
    address = Address.objects.filter(pk=id, customer=request.user)
    address.delete()
    return redirect("account:addresses")


@login_required
def set_default(request, id):
    Address.objects.filter(customer=request.user, default=True).update(default=False)
    Address.objects.filter(pk=id, customer=request.user).update(default=True)
    return redirect("account:addresses")
