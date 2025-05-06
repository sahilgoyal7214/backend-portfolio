from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProjectViewSet,
    CategoryViewSet,
    ExperienceViewSet,
    EducationViewSet,
    ContactViewSet,
    ResumeViewSet,
    ProfileViewSet,
    StatsticViewSet,
    fetch_project, 
    fetch_Statstic

)

router = DefaultRouter()
router.register("projects", ProjectViewSet)
router.register("categories", CategoryViewSet)
router.register("experiences", ExperienceViewSet)
router.register("educations", EducationViewSet)
router.register("contacts", ContactViewSet)
router.register("resumes", ResumeViewSet)
router.register("profiles", ProfileViewSet)
router.register("Statstic", StatsticViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("fetch-projects/", fetch_project, name="fetch_projects"),
    path("fetch-statistics/", fetch_Statstic, name="fetch_statistics"),
]
