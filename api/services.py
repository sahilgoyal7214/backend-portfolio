import requests as re
from datetime import datetime
from .models import Project, Skill, Category,Statstic
from pathlib import Path
import environ 
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Environment Variables
environ.Env.read_env(BASE_DIR / ".env")
env = environ.Env(
    GITHUB_API_LINK=(str, ""),
    GITHUB_API_TOKEN=(str, ""),
    GITHUB_USERNAME=(str, ""),
)


class GitHub:
    def __init__(self ):
        self.username = env("GITHUB_USERNAME")
        self.token = env("GITHUB_API_TOKEN")
        self.headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {self.token}",
            "User-Agent": "commit-counter"
        }
        self.GITHUB_API_LINK = "https://api.github.com/user/repos?per_page=100&visibility=all"  
    # def fetch(self):
    #     res = re.get(url=self.GITHUB_API_LINK, headers=self.headers)
    #     if res.status_code == 200:
    #         data = res.json()
    #         for project in data:
    #             if project["topics"] is not None:
    #                 if project["homepage"] is not None:
    #                     deployment_url = project["html_url"]

    #                 projects_list = Project.objects.filter(
    #                     github_url=project["html_url"]
    #                 )
    #                 if projects_list.exists():
    #                     project_obj = projects_list.first()
    #                     if project_obj.title != project["name"]:
    #                         project_obj.title = project["name"]
    #                     if project_obj.description != project["description"]:
    #                         project_obj.description = project["description"]
    #                     if project_obj.deployment_url != deployment_url:
    #                         project_obj.deployment_url = deployment_url
    #                     if project_obj.github_url != project["html_url"]:
    #                         project_obj.github_url = project["html_url"]
    #                 else:
    #                     project_obj = Project.objects.create(
    #                         title=project["name"],
    #                         description=project["description"],
    #                         github_url=project["html_url"],
    #                         deployment_url=deployment_url,
    #                     )

    #                 a = set(project["topics"])
    #                 b = set(project_obj.topics.values_list("name", flat=True))
    #                 b = set(map(str.lower, list(b)))
    #                 intersection = a.intersection(b)
    #                 union = a.union(b)
    #                 datbase = list(b - intersection)
    #                 github = list(a - intersection)

    #                 if len(union - intersection) != 0:
    #                     for topic in list(union):
    #                         if topic in list(github):
    #                             topic_obj = Skill.objects.filter(name__icontains=topic)
    #                             if topic_obj.exists():
    #                                 project_obj.topics.add(topic_obj.first())
    #                             else:
    #                                 category_obj, _ = Category.objects.get_or_create(
    #                                     name="Others"
    #                                 )
    #                                 topic_obj = Skill.objects.create(
    #                                     name=topic, category=category_obj
    #                                 )
    #                                 project_obj.topics.add(topic_obj)
    #                         # if topic in list(datbase):
    #                         #     topic_obj = Skill.objects.filter(name__icontains=topic)
    #                         #     project_obj.topics.remove(topic_obj.first())
    #                 project_obj.save()

    def fetch(self, include_forks=True):
        page = 1
        while True:
            url = f"{self.GITHUB_API_LINK}&page={page}"
            res = re.get(url, headers=self.headers)
            if res.status_code != 200:
                print(f"❌ Failed to fetch GitHub repos: {res.status_code} - {res.text}")
                break

            data = res.json()
            if not data:
                break

            for project in data:
                if not include_forks and project.get("fork"):
                    continue  # Skip forked repos if specified

                topics = project.get("topics", [])
                homepage = project.get("homepage", "")
                github_url = project.get("html_url")

                if not github_url:
                    continue

                # Find or create the corresponding project
                project_obj, created = Project.objects.get_or_create(
                    github_url=github_url,
                    defaults={
                        "title": project["name"],
                        "description": project.get("description", ""),
                        "deployment_url": homepage or github_url,
                    }
                )

                # Update fields if changed
                updated = False
                if project_obj.title != project["name"]:
                    project_obj.title = project["name"]
                    updated = True
                if project_obj.description != project.get("description", ""):
                    project_obj.description = project.get("description", "")
                    updated = True
                if project_obj.deployment_url != (homepage or github_url):
                    project_obj.deployment_url = homepage or github_url
                    updated = True

                if updated:
                    project_obj.save()

                # Sync topics
                current_topics = set(project_obj.topics.values_list("name", flat=True))
                github_topics = set(topics)
                to_add = github_topics - current_topics

                for topic in to_add:
                    skill_qs = Skill.objects.filter(name__iexact=topic)
                    if skill_qs.exists():
                        skill = skill_qs.first()
                    else:
                        category, _ = Category.objects.get_or_create(name="Others")
                        skill = Skill.objects.create(name=topic, category=category)
                    project_obj.topics.add(skill)

            page += 1

class GitHubAnalyzer:
    def __init__(self ):
        self.username = env("GITHUB_USERNAME")
        self.token = env("GITHUB_API_TOKEN")
        self.headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {self.token}",
            "User-Agent": "commit-counter"
        }

    def get_repos(self):
        repos = []
        page = 1
        while True:
            url = f"https://api.github.com/user/repos?per_page=100&page={page}&visibility=all"
            response = re.get(url, headers=self.headers)
            if response.status_code != 200:
                print(f"Error fetching repos: {response.status_code} - {response.text}")
                break
            batch = response.json()
            if not batch:
                break
            repos.extend(batch)
            page += 1
        return repos

    def get_commit_count(self, owner, repo):
        seen_commits = set()
        total_commits = 0

        branches_url = f"https://api.github.com/repos/{owner}/{repo}/branches"
        response = re.get(branches_url, headers=self.headers)
        if response.status_code != 200:
            print(f"Failed to get branches for {repo}: {response.status_code}")
            return 0

        branches = response.json()
        for branch in branches:
            branch_name = branch["name"]
            url = f"https://api.github.com/repos/{owner}/{repo}/commits?sha={branch_name}&author={self.username}&per_page=100"
            response = re.get(url, headers=self.headers)
            if response.status_code != 200:
                print(f"Failed to get commits for {repo} on branch {branch_name}: {response.status_code}")
                continue

            while True:
                commits = response.json()
                for commit in commits:
                    sha = commit["sha"]
                    if sha not in seen_commits:
                        seen_commits.add(sha)
                        total_commits += 1

                if 'Link' not in response.headers:
                    break

                next_link = None
                for part in response.headers['Link'].split(','):
                    if 'rel="next"' in part:
                        next_link = part.split(';')[0].strip()[1:-1]
                        break
                if not next_link:
                    break
                response = re.get(next_link, headers=self.headers)

        return total_commits

    def get_account_age(self):
        url = f"https://api.github.com/users/{self.username}"
        response = re.get(url, headers=self.headers)
        if response.status_code == 200:
            user_data = response.json()
            creation_date = user_data.get("created_at")
            if creation_date:
                creation_year = int(creation_date.split('-')[0])
                current_year = datetime.utcnow().year
                return current_year - creation_year
        else:
            print(f"Failed to fetch user data: {response.status_code}")
        return None

    def analyze(self):
        repos = self.get_repos()
        total_commits = 0
        print(f"🔍 Found {len(repos)} repositories.")
        for repo in repos:
            name = repo["name"]
            owner = repo["owner"]["login"]
            commits = self.get_commit_count(owner, name)
            total_commits += commits

        print(f"👨‍💻 Total commits: {total_commits}")

        age = self.get_account_age()
        print(f"👨‍💻 Years of experience: {age}")
        # Step 1: Category names to exclude
        excluded_category_names = ["Machine Learning & AI", "Others", "Soft Skills & Collaboration"]

        # Step 2: Get excluded categories
        excluded_categories = Category.objects.filter(name__in=excluded_category_names)

        # Step 3: Get all visible project topics (skills), excluding those from excluded categories
        visible_skills = Skill.objects.filter(
            projects__is_visible=True
        ).exclude(
            category__in=excluded_categories
        ).values_list("name", flat=True).distinct()

        # Step 4: Convert to a set if needed
        technologies_mastered = len(set(visible_skills)) 

        # technologies_mastered = len(set([skill for skill in Project.objects.filter(is_visible=True).values_list("topics__name", flat=True)]))
        print(f"👨‍💻 Technologies mastered: {technologies_mastered}")

        Project_completed = len(set([project for project in Project.objects.filter(is_visible=True).values_list("title", flat=True)]))
        print(f"👨‍💻 Projects completed: {Project_completed}")
        if age:
            age = int(age)
        else:
            age = 0
        Statstic_obj, _ = Statstic.objects.get_or_create(username=self.username)
        Statstic_obj.commits = total_commits
        Statstic_obj.technologies_mastered = technologies_mastered
        Statstic_obj.projects_completed = Project_completed
        Statstic_obj.year_of_experience = age
        Statstic_obj.save()