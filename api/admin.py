from django.contrib import admin
from .models import Project, Skill, Category, Experience, Education, Resume, Contact, Profile
from django.contrib.auth.models import User, Group
from .services import GitHub
from django.contrib import messages

# Register your models here.

admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    list_display_links = list_display
    search_fields = ["name"]


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ["name", "category"]
    list_display_links = list_display
    list_filter = ["category"]
    search_fields = ["name", "category__name"]


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["title", "is_visible", "skills"]
    # list_display_links = list_display
    list_editable = ["is_visible"]
    search_fields = ["title", "topics__name"]
    list_filter = ["is_visible", "topics"]
    actions = ["fetch_project"]
    filter_horizontal = ["topics"]

    def skills(self, obj):
        return ", ".join([topic.name for topic in obj.topics.all()])

    skills.short_description = "topics"

    @admin.action(description="Fetch latest projects from GitHub")
    def fetch_project(self, request, queryset):
        service = GitHub()
        service.fetch()
        messages.success(request, "Projects fetched successfully")


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ["title", "company", "start_date", "end_date", "is_current"]
    list_display_links = list_display
    search_fields = ["title", "company"]
    list_filter = ["is_current", "start_date", "end_date"]


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ["institute", "degree", "grade"]
    list_display_links = list_display
    search_fields = ["institute", "degree", "grade"]
    list_filter = ["degree", "grade"]


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ["name"]
    list_display_links = list_display
    search_fields = ["name"]


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "message"]
    list_display_links = list_display
    search_fields = ["name", "email", "message"]
    list_filter = ["created_at"]

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["name", "roles"]
    list_display_links = list_display
    search_fields = ["name", "roles"]
    list_filter = ["roles"]