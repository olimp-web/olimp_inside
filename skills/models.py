from django.db import models

# Create your models here.


class Skill(models.Model):
    parent = models.ForeignKey('Skill', related_name="childs", on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=240)
    available = models.BooleanField()

    @classmethod
    def tree(cls):
        pass


class SkillQualify(models.Model):
    project = models.ForeignKey('QualificationProject', on_delete=models.CASCADE)
    skill = models.ForeignKey('Skill', on_delete=models.CASCADE)
    requested_level = models.PositiveSmallIntegerField()
    confirmed_level = models.PositiveSmallIntegerField()


class QualificationProject(models.Model):
    title = models.CharField(max_length=30)
    owner = models.ForeignKey('accounts.UserAccount', on_delete=models.CASCADE, related_name="owned_project")
    skills = models.ManyToManyField('Skill', through=SkillQualify)
    expert = models.ForeignKey('accounts.UserAccount', related_name="validated_project", on_delete=models.SET_NULL,
                               null=True, blank=True)
