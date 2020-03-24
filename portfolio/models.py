from django.core.validators import MinValueValidator
from django.db import models
from accounts.models import Profile


# Create your models here.
class SkillProfile(Profile):
    _PRIVATE_CHOICES = (
        ('0', 'Видно только мне'),
        ('1', 'Видно всем'),
        ('2', 'Видно друзьям'),
        ('3', 'Видно колегам'),
    )

    education = models.ForeignKey('Education',
                                  blank=True,
                                  null=True,
                                  on_delete=models.CASCADE,
                                  verbose_name='Образование')
    area = models.ManyToManyField(to='Skills',
                                  blank=True,
                                  related_name='area_user',
                                  verbose_name='Проффессиональная сфера')
    skills_user = models.ManyToManyField(to='Skills',
                                         blank=True,
                                         related_name='skill_user',
                                         verbose_name='Навыки пользоателя')
    interests = models.TextField(blank=True,
                                 null=True,
                                 verbose_name='Интересы пользователя')
    grade = models.SmallIntegerField(help_text='Уровнь владения навыком')
    private = models.CharField(max_length=1,
                               choices=_PRIVATE_CHOICES,
                               default='0',
                               verbose_name='приватность')

    class Meta:
        verbose_name = 'Навык пользователя'
        verbose_name_plural = 'Навыки пользователей'


class Education(models.Model):
    university = models.CharField(max_length=100,
                                  verbose_name="Университет")
    subdivision = models.CharField(max_length=100,
                                   verbose_name="Подразделение",
                                   help_text="Подразделение, факультет")
    department = models.CharField(max_length=100,
                                  verbose_name="Кафедра",
                                  help_text="кафедра")
    begin_year = models.SmallIntegerField(verbose_name="Год начала обучения",
                                          help_text="Начало обучения")
    end_year = models.SmallIntegerField(verbose_name="Год окончания обучения",
                                        help_text="Окончание обучения", )
    group = models.CharField(max_length=10,
                             verbose_name="Группа",
                             help_text="Группа")

    class Meta:
        verbose_name = 'высшее образование'
        verbose_name_plural = 'высшие образования'

    def __str__(self):
        return '{}: {}'.format(self.university, self.group)


class Skills(models.Model):
    name = models.CharField(max_length=200,
                            unique=True,
                            verbose_name='Название навыка')
    approved = models.BooleanField(default=False,
                                   verbose_name='Подтверждение навыка')
    type_skill = models.ForeignKey('TypeSkill',
                                   on_delete=models.CASCADE,
                                   verbose_name='Тип навыка')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Навык'
        verbose_name_plural = 'Навыки'


class TypeSkill(models.Model):
    title = models.CharField(max_length=250,
                             unique=True,
                             verbose_name='Название типа навыка')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тип навыка'
        verbose_name_plural = 'Типы навыка'


class TypeRelationship(models.Model):
    title = models.CharField(
        max_length=250,
        unique=True,
        verbose_name='Название типа связи')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тип связи'
        verbose_name_plural = 'Типы связей'


class Relationships(models.Model):
    to_skill = models.ManyToManyField(to=Skills, related_name='to_skill')
    from_skill = models.ManyToManyField(to=Skills, related_name='from_skill')
    type_relationship = models.ForeignKey(TypeRelationship,
                                          on_delete=models.CASCADE,
                                          verbose_name='Тип связи')

    class Meta:
        verbose_name = 'Связь'
        verbose_name_plural = 'Связи'


class Methods(models.Model):
    content = models.TextField(verbose_name='Содержание')
    rate_methods = models.IntegerField(default=0,
                                       validators=[MinValueValidator(0)],
                                       verbose_name='Оценка методики')

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = 'Методика'
        verbose_name_plural = 'Методики'


class Assessment(models.Model):
    profile_id = models.ForeignKey('accounts.UserAccount',
                                   on_delete=models.CASCADE,
                                   verbose_name='Пользователь')
    skill_id = models.ForeignKey('Skills',
                                 on_delete=models.CASCADE,
                                 verbose_name='Навыки')
    rate = models.IntegerField(verbose_name='Оценка',
                               validators=[MinValueValidator(0)])

    def __str__(self):
        return str(self.rate)

    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'


class Project(models.Model):
    PATH = ''

    TYPE_PROJECT = (
        ('1', 'Видимый'),
        ('2', 'Скрытый')
    )

    STATUS_PROJECT = (
        ('1', 'Текущий'),
        ('2', 'Завершенный'),
        ('3', 'Запланнированный')
    )

    name = models.CharField(max_length=250,
                            verbose_name='Название проекта')
    description = models.CharField(max_length=300,
                                   blank=True,
                                   null=True,
                                   verbose_name='Описание')
    photo = models.ImageField(upload_to=PATH,
                              blank=True,
                              null=True,
                              verbose_name='Путь к фотографии')
    is_visible = models.CharField(max_length=1,
                                  choices=TYPE_PROJECT,
                                  default='1',
                                  verbose_name='Тип проектв')
    status_project = models.CharField(max_length=1,
                                      choices=STATUS_PROJECT,
                                      default='1',
                                      verbose_name='Статус проекта')
    published = models.DateTimeField(auto_now_add=True,
                                     verbose_name='Дата добавления')

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
