from django.contrib.auth import login
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from config.settings import EMAIL_HOST_USER

from .forms import UserRegisterForm
from .models import User


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        self.send_welcome_email(user.email)
        return super().form_valid(form)

    def send_welcome_email(self, user_email):

        send_mail(
            subject="Добро пожаловать в наш сервис!",
            message="Вы успешно зарегистрированы на нашем сервисе!",
            from_email=EMAIL_HOST_USER,
            recipient_list=[
                user_email,
            ],
        )
