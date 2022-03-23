from dataclasses import field

from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordResetForm,
    SetPasswordForm,
)
from django_countries.widgets import CountrySelectWidget

from .models import Address, Customer


class UserAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["full_name", "phone", "address_line", "address_line2", "town_city", "postcode"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["full_name"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Full Name"}
        )
        self.fields["phone"].widget.attrs.update({"class": "form-control mb-2 account-form", "placeholder": "Phone"})
        self.fields["address_line"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Address 1"}
        )
        self.fields["address_line2"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Address 2"}
        )
        self.fields["town_city"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Town/City"}
        )
        self.fields["postcode"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Post code"}
        )


class UserLoginForm(AuthenticationForm):

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control mb-3", "placeholder": "Username", "type": "text", "id": "login-username"}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password", "id": "login-pwd"})
    )


class UserRegistrationForm(forms.ModelForm):
    user_name = forms.CharField(
        label="Enter Username", max_length=50, min_length=4, required=True, help_text="Required"
    )
    email = forms.EmailField(
        max_length=100, help_text="Required", error_messages={"required": "You would need a valid email"}
    )
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repeat Password", widget=forms.PasswordInput)

    class Meta:
        model = Customer
        fields = ("user_name", "email")

    def clean_username(self):
        """Prevent existing user_name from registration"""
        user_name = self.cleaned_data["user_name"].lower()
        user_qrs = Customer.objects.filter(user_name=user_name)
        if user_qrs.exists():
            raise forms.ValidationError("This username already exit.!")
        return user_name

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError("Password do not match")
        return cd["password2"]

    def clean_email(self):
        """Prevent existing email from registration"""
        email = self.cleaned_data["email"]
        user_qrs = Customer.objects.filter(email=email).exists()
        if user_qrs:
            raise forms.ValidationError("Please use another Email, that is already taken!")
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["user_name"].widget.attrs.update({"class": "form-control mb-3", "placeholder": "Username"})
        self.fields["email"].widget.attrs.update(
            {"class": "form-control mb-3", "placeholder": "E-mail", "name": "email", "id": "id_email"}
        )
        self.fields["password"].widget.attrs.update({"class": "form-control mb-3", "placeholder": "Password"})
        self.fields["password2"].widget.attrs.update({"class": "form-control", "placeholder": "Repeat Password"})


class UserEditForm(forms.ModelForm):

    email = forms.EmailField(
        label="Account email (can not be changed)",
        max_length=200,
        widget=forms.TextInput(
            attrs={"class": "form-control mb-3", "placeholder": "email", "id": "form-email", "readonly": "readonly"}
        ),
    )

    first_name = forms.CharField(
        label="First Name",
        min_length=4,
        max_length=50,
        widget=forms.TextInput(
            attrs={"class": "form-control mb-3", " placeholder": "Firstname", "id": "form-firstname"}
        ),
    )

    class Meta:
        model = Customer
        fields = ("email", "first_name")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].required = True
        self.fields["email"].required = True


class PwdResetForm(PasswordResetForm):

    email = forms.EmailField(
        max_length=254,
        widget=forms.TextInput(attrs={"class": "form-control mb-3", "placeholder": "Email", "id": "form-email"}),
    )

    def clean_email(self):
        email = self.cleaned_data["email"]
        u = Customer.objects.filter(email=email)
        if not u:
            raise forms.ValidationError("Unfortunatley we can not find that email address")
        return email


class PwdResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control mb-3", "placeholder": "New Password", "id": "form-newpass"}
        ),
    )
    new_password2 = forms.CharField(
        label="Repeat password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control mb-3", "placeholder": "New Password", "id": "form-new-pass2"}
        ),
    )
