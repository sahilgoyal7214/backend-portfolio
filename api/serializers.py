from rest_framework.serializers import ModelSerializer
from .models import Project, Skill, Category, Experience, Education,Contact,Resume,Profile,Statstic
from .services import GitHub, GitHubAnalyzer


class ProjectSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = "__all__"
        depth = 1

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["topics"] = [topic.name for topic in instance.topics.all()]
        return representation


class SkillSerializer(ModelSerializer):

    class Meta:
        model = Skill
        fields = "__all__"
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        projects = Project.objects.filter(topics=instance)
        used_projects = [project.title for project in projects]
        if len(used_projects) != 0:
            return representation


class CategorySerializer(ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = "__all__"

    def to_representation(self, instance):
        # service = GitHub()
        # service.fetch()
        representation = super().to_representation(instance)
        skills = representation["skills"]
        representation["skills"] = [skill for skill in skills if skill is not None]
        return representation

class ExperienceSerializer(ModelSerializer):
    class Meta:
        model = Experience
        fields = "__all__"
        depth = 1

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["skills"] = [skill.name for skill in instance.skills.all()]
        return representation

class EducationSerializer(ModelSerializer):
    class Meta:
        model = Education
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation

class ContactSerializer(ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation

class ResumeSerializer(ModelSerializer):
    class Meta:
        model = Resume
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation

class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"
        depth = 1

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation

class StatsticSerializer(ModelSerializer):
    class Meta:
        model = Statstic
        fields = "__all__"

    def to_representation(self, instance):
        # service = GitHubAnalyzer()
        # service.analyze()
        representation = super().to_representation(instance)
        return representation