from django.contrib import admin
from .models import SkillProfile, Skills, Project, Assessment, TypeSkill, Relationships, TypeRelationship


# Register your models here.
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_visible', 'status_project', 'published']
    list_display_links = ['name', 'is_visible', 'status_project', 'published']
    search_fields = ['name', 'is_visible', 'status_project']
    list_filter = ['is_visible', 'status_project']
    list_per_page = 20


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ['profile_id', 'skill_id', 'rate']
    search_fields = ['profile_id', 'skill_id', 'rate']
    list_filter = ['skill_id']
    list_per_page = 20


@admin.register(Relationships)
class RelationshipsAdmin(admin.ModelAdmin):
    list_filter = ['type_relationship']
    list_per_page = 20


@admin.register(TypeRelationship)
class RelationshipsTypeAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_per_page = 20


@admin.register(Skills)
class SkillsAdmin(admin.ModelAdmin):
    list_display = ['name', 'approved', 'type_skill']
    list_display_links = ['name', 'approved', 'type_skill']
    search_fields = ['name', 'type_skill']
    list_filter = ['approved']
    list_per_page = 20


@admin.register(TypeSkill)
class TypeSkillsAdmin(admin.ModelAdmin):
    list_display = ['title']
    list_per_page = 20


@admin.register(SkillProfile)
class SkillProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'surname')

    fieldsets = (
        (None, {
            'fields': ('area', 'skills_user', 'interests', 'grade', 'private')
        }),
    )
