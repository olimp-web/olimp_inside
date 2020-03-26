from django.contrib import admin
from .models import SkillProfile, Skills, Project, Assessment, TypeSkill, Relationships, TypeRelationship


# Register your models here.
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'profile_id', 'skill_id', 'rate']
    search_fields = ['profile_id', 'skill_id', 'rate']
    list_filter = ['skill_id']
    list_per_page = 10


@admin.register(Relationships, TypeRelationship)
class RelationshipsAdmin(admin.ModelAdmin):
    pass


@admin.register(Skills, TypeSkill)
class SkillsAdmin(admin.ModelAdmin):
    # list_display = ['name']
    list_per_page = 10


@admin.register(SkillProfile)
class SkillProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'surname')

    fieldsets = (
        (None, {
            'fields': ('area', 'skills_user', 'interests', 'grade', 'private')
        }),
    )
