from django import forms
from django.contrib.auth.forms import UserCreationForm

from users.models import User


class UserRegisterForm(UserCreationForm):
    email = forms.CharField(max_length=50, required=True)

    class Meta:
        model = User
        fields = ("email", "phone", "avatar", "country", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        fields_placeholders = {
            "email": "Укажите адрес электронной почты",
            "phone": "Введите номер телефона",
            "avatar": "",
            "country": "Укажите страну",
            "password1": "",
            "password2": "",
        }
        for field, placeholder in fields_placeholders.items():
            self.fields[field].widget.attrs.update({"class": "form-control"})
            if placeholder:
                self.fields[field].widget.attrs.update({"placeholder": placeholder})

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if phone and not phone.isdigit():
            raise forms.ValidationError("Номер должен состоять только их цифр.")
        return phone
