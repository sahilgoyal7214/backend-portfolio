from rest_framework.viewsets import ModelViewSet
from .serializers import ProjectSerializer, CategorySerializer,ExperienceSerializer,EducationSerializer,ContactSerializer,ResumeSerializer,ProfileSerializer
from .models import Project, Category,Experience,Education,Contact,Resume,Profile


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