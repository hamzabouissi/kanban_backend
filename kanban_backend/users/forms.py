from django import forms
from django.contrib.auth import forms as admin_forms, password_validation
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UserChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User
        fields = ("username", "email", "user_type")


class UserCreationForm(admin_forms.UserCreationForm):
    pass
    # class Meta(admin_forms.UserCreationForm.Meta):
    #     model = User
    #     fields = ("username", "email", "user_type")
    #     error_messages = {
    #         "username": {"unique": _("This username has already been taken.")}
    #     }


