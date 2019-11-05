from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, UserManager
from django.utils import timezone
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


# Create your models here.


class AccountManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        # username = self.model.normalize_username(username)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        _default_profile, _ = Profile.objects.get_or_create(surname="Service", name=":", patronymic=":")
        extra_fields.setdefault('profile', _default_profile)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class UsernameValidator(RegexValidator):
    regex = r'^[\w.-]+$'
    message = 'Enter a valid username. This value may contain only letters, ' \
              'numbers, and /./-/_ characters.'
    flags = 0


class BaseAccount(AbstractBaseUser, PermissionsMixin):
    username_validator = UsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator, ],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = models.EmailField(_('email address'), unique=True)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)

    objects = AccountManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    class Meta:
        verbose_name = "аккаунт"
        verbose_name_plural = "аккаунты"
        abstract = True

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)
        #

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        if self.profile:
            full_name = '%s %s %s' % (self.profile.surname.capitalize(),
                                      self.profile.name.capitalize(),
                                      self.profile.patronymic.capitalize())
        else:
            full_name = "-empty-"
        return full_name.strip()
    get_full_name.short_description = 'ФИО'

    def get_short_name(self):
        """Return the short name for the user."""
        if self.profile:
            full_name = '%s %s. %s.' % (self.profile.surname.capitalize(),
                                        self.profile.name[0:1].upper(),
                                        self.profile.patronymic[0:1].upper())
        else:
            full_name = "-empty-"
        return full_name.strip()
    #
    # def email_user(self, subject, message, from_email=None, **kwargs):
    #     """Send an email to this user."""
    #     send_mail(subject, message, from_email, [self.email], **kwargs)


class UserAccount(BaseAccount):
    class Meta(BaseAccount.Meta):
        swappable = 'AUTH_USER_MODEL'


class Profile(models.Model):
    surname = models.CharField(max_length=100, verbose_name="Фамилия", null=False, blank=False)
    name = models.CharField(max_length=100, verbose_name="Имя", null=False, blank=False)
    patronymic = models.CharField(max_length=100, verbose_name="Отчество", null=False, blank=False)
    dob = models.DateField(null=True, blank=True, verbose_name="дата рождения")
    vk_link = models.URLField(verbose_name="профиль вконтакте", blank=True, default="")
    phone_number = models.CharField(max_length=12, verbose_name="номер телефона")
    identify_data = models.CharField(max_length=11, verbose_name="Паспортные данные", blank=True)

    class Meta:
        verbose_name = "профиль"
        verbose_name_plural = "профили"
