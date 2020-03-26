from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserAccount, Profile


class FormRegister(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required', label="Email:")
    surname = forms.CharField(max_length=100, label="Фамилия:")
    name = forms.CharField(max_length=100, label="Имя:")
    patronymic = forms.CharField(max_length=100, label="Отчество:")
    dob = forms.DateField(label="Дата рождения:")
    vk_link = forms.URLField(required=False, label="ссылка vk:")
    phone_number = forms.CharField(max_length=12, label="Номер телефона:")


    # Стилизация формы
    def __init__(self, *args, **kwargs):
        super(FormRegister, self).__init__(*args, **kwargs)

        # for item in self.fields:
        #     self.fields[item].widget = forms.scss.TextInput(attrs={'class':'form-control'})

        self.fields['username'].widget = forms.TextInput(attrs={'class': 'form-control',})
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control', })
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control', })

        self.fields['email'].widget = forms.TextInput(attrs={'class': 'form-control', })
        self.fields['surname'].widget = forms.TextInput(attrs={'class': 'form-control',})
        self.fields['name'].widget = forms.TextInput(attrs={'class': 'form-control', })
        self.fields['dob'].widget = forms.DateInput(attrs={'class': 'form-control', })
        self.fields['patronymic'].widget = forms.TextInput(attrs={'class': 'form-control', })
        self.fields['vk_link'].widget = forms.TextInput(attrs={'class': 'form-control', })
        self.fields['phone_number'].widget = forms.TextInput(attrs={'class': 'form-control', })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        # profile =
        if commit:
            prof = Profile.objects.create(
                surname      = self.cleaned_data['surname'],
                name         = self.cleaned_data['name'],
                patronymic   = self.cleaned_data['patronymic'],
                dob          = self.cleaned_data['dob'],
                vk_link      = self.cleaned_data['vk_link'],
                phone_number = self.cleaned_data['phone_number'],
            )
            user.profile = prof
            user.save()
        return user

    class Meta:
        model = UserAccount
        fields = ('username', 'email', 'password1', 'password2')