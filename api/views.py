from rest_framework.viewsets import ModelViewSet
from django.contrib import messages
from django.shortcuts import redirect
from .services import GitHub, GitHubAnalyzer
from .serializers import ProjectSerializer, CategorySerializer,ExperienceSerializer,EducationSerializer,ContactSerializer,ResumeSerializer,ProfileSerializer,StatsticSerializer
from .models import Project, Category,Experience,Education,Contact,Resume,Profile,Statstic
from pathlib import Path
import environ

BASE_DIR = Path(__file__).resolve().parent.parent
# Environment Variables
environ.Env.read_env(BASE_DIR / ".env")
env = environ.Env(
    GITHUB_USERNAME=(str, ""),
)

class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.filter(is_visible=True)
    serializer_class = ProjectSerializer
    http_method_names = ["get"]
    filterset_fields = ["topics__name"]


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    http_method_names = ["get"]

class ExperienceViewSet(ModelViewSet):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    http_method_names = ["get"]
    
class EducationViewSet(ModelViewSet):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    http_method_names = ["get"]
    
class ResumeViewSet(ModelViewSet):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    http_method_names = ["get"]
    
class ContactViewSet(ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    http_method_names = ["post"]
    
class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    http_method_names = ["get"]

class StatsticViewSet(ModelViewSet):
    queryset = Statstic.objects.all()
    serializer_class = StatsticSerializer
    http_method_names = ["get"]


def fetch_project(request):
    if request.user.is_authenticated:
        GitHub().fetch()
        messages.success(request, "Projects fetched successfully.")
        return redirect("/admin/api/project/")
    return redirect("/admin/")

def fetch_Statstic(request):
    if request.user.is_authenticated:
        GitHubAnalyzer().analyze()
        messages.success(request, "Statistics updated successfully.")
        return redirect("/admin/api/statstic/")
    return redirect("/admin/")