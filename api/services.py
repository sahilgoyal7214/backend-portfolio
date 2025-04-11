import requests as re
from .models import Project, Skill, Category



class GitHub:
    GITHUB_API_LINK = "https://api.github.com/users/sahilgoyal7214/repos"

    def fetch(self):
        res = re.get(url=self.GITHUB_API_LINK)
        if res.status_code == 200:
            data = res.json()
            for project in data:
                if project["topics"] is not None:
                    if project["homepage"] is not None:
                        deployment_url = project["html_url"]

                    projects_list = Project.objects.filter(
                        github_url=project["html_url"]
                    )
                    if projects_list.exists():
                        project_obj = projects_list.first()
                        if project_obj.title != project["name"]:
                            project_obj.title = project["name"]
                        if project_obj.description != project["description"]:
                            project_obj.description = project["description"]
                        if project_obj.deployment_url != deployment_url:
                            project_obj.deployment_url = deployment_url
                        if project_obj.github_url != project["html_url"]:
                            project_obj.github_url = project["html_url"]
                    else:
                        project_obj = Project.objects.create(
                            title=project["name"],
                            description=project["description"],
                            github_url=project["html_url"],
                            deployment_url=deployment_url,
                        )

                    a = set(project["topics"])
                    b = set(project_obj.topics.values_list("name", flat=True))
                    b = set(map(str.lower, list(b)))
                    intersection = a.intersection(b)
                    union = a.union(b)
                    datbase = list(b - intersection)
                    github = list(a - intersection)

                    if len(union - intersection) != 0:
                        for topic in list(union):
                            if topic in list(github):
                                topic_obj = Skill.objects.filter(name__icontains=topic)
                                if topic_obj.exists():
                                    project_obj.topics.add(topic_obj.first())
                                else:
                                    category_obj, _ = Category.objects.get_or_create(
                                        name="Others"
                                    )
                                    topic_obj = Skill.objects.create(
                                        name=topic, category=category_obj
                                    )
                                    project_obj.topics.add(topic_obj)
                            # if topic in list(datbase):
                            #     topic_obj = Skill.objects.filter(name__icontains=topic)
                            #     project_obj.topics.remove(topic_obj.first())
                    project_obj.save()

    # def load_skills(self):
    # from django.conf import settings
    # import json

    # with open(settings.BASE_DIR / "test.json") as f:
    #     data = json.load(f)
    #     for category, skills in data.items():
    # print(category, skills)
    # category_obj, _ = Category.objects.get_or_create(name=category)
    # for skill in skills:
    #     skill_obj = Skill.objects.get_or_create(name=skill, category=category_obj)
    # from django.db.models import Count

    # lst = (
    #     Skill.objects.values("name")
    #     .annotate(Count("id"))
    #     .order_by()
    #     .filter(id__count__gt=1)
    # )
    # print(lst)
    # data = [
    # "name": [categories]
    # ]
    # skills = []
    # for skill in lst:
    #     name = skill["name"]
    #     dup_skills = Skill.objects.filter(name=name)
    #     data = {}
    #     for sk in dup_skills:
    #         name, cat = sk.name, sk.category
    #         if name not in data:
    #             data[name] = [cat.name]
    #         else:
    #             data[name].append(cat.name)
    #     skills.append(data)

    # import json

    # not_needed = []
    # with open("skills.json", "r") as f:
    #     data = json.load(f)
    #     for d in data:
    #         for skills, cats in d.items():
    #             skill = (
    #                 Skill.objects.filter(name=skills)
    #                 .exclude(category__name__icontains=cats[0])
    #                 .first()
    #             )
    #             not_needed.append(skill)

    # print(not_needed)
    # for skill in not_needed:
    #     skill.delete()

    # category_obj, _ = Category.objects.get_or_create(name=category)
    # for skill in skills:
    #     skill_obj = Skill.objects.get_or_create(name=skill, category=category_obj)
