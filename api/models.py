from django.db import models
from django.core.exceptions import ValidationError


def list_of_strings(value):
    if not isinstance(value, list):
        raise ValidationError("This field must be a list.")
    for item in value:
        if not isinstance(item, str):
            raise ValidationError(f"All elements must be strings. Found: {type(item).__name__}")


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Skill(models.Model):
    name = models.CharField(max_length=100)
    image = models.TextField(blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="skills"
    )

    class Meta:
        unique_together = ["name", "category"]

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="projects/", blank=True, null=True)
    deployment_url = models.URLField(blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    is_visible = models.BooleanField(default=True)
    topics = models.ManyToManyField(Skill, related_name="projects", blank=True)

    def __str__(self):
        return self.title


class Experience(models.Model):
    title = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=False)
    skills = models.ManyToManyField(Skill, related_name="experiences", blank=True)
    company_logo = models.ImageField(upload_to="companies/", blank=True, null=True)

    def __str__(self):
        return self.title


class Education(models.Model):
    institute = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    degree = models.CharField(max_length=100)
    grade = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=False)
    institute_logo = models.ImageField(upload_to="institutes/", blank=True, null=True)

    def __str__(self):
        return self.instiute


class Resume(models.Model):
    name = models.CharField(max_length=100)
    resume = models.FileField(upload_to="resumes/", blank=True, null=True)

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100, blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Profile(models.Model):
    name = models.CharField(max_length=100)
    roles = models.JSONField(default=list, validators=[list_of_strings])
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="profiles/", blank=True, null=True)
    resume = models.ForeignKey(
        Resume, on_delete=models.CASCADE, related_name="profiles", blank=True, null=True
    )

    def __str__(self):
        return self.name
