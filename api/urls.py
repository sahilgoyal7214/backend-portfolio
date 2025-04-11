from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProjectViewSet,
    CategoryViewSet,
    ExperienceViewSet,
    EducationViewSet,
    ContactViewSet,
    ResumeViewSet,
    ProfileViewSet
)

router = DefaultRouter()
router.register("projects", ProjectViewSet)
router.register("categories", CategoryViewSet)
router.register("experiences", ExperienceViewSet)
router.register("educations", EducationViewSet)
router.register("contacts", ContactViewSet)
router.register("resumes", ResumeViewSet)
router.register("profiles", ProfileViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
