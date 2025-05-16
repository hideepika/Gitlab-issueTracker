import time
import requests
from prometheus_client import start_http_server, Gauge

GITLAB_URL = "http://gitlab"
ACCESS_TOKEN = "your_token_here"
SCRAPE_INTERVAL = 60
headers = {"Private-Token": ACCESS_TOKEN}

open_issues = Gauge("gitlab_issues_open_total", "Open issues", ["project"])
closed_issues = Gauge("gitlab_issues_closed_total", "Closed issues", ["project"])
assigned_issues = Gauge("gitlab_issues_assigned_total", "Assigned issues", ["project", "assignee"])

def fetch_issues(project_id, project_name):
    page = 1
    while True:
        url = f"{GITLAB_URL}/api/v4/projects/{project_id}/issues?per_page=100&page={page}"
        r = requests.get(url, headers=headers)
        if r.status_code != 200:
            break
        data = r.json()
        if not data:
            break
        for issue in data:
            state = issue["state"]
            assignees = issue.get("assignees", [])
            if state == "opened":
                open_issues.labels(project=project_name).inc()
            elif state == "closed":
                closed_issues.labels(project=project_name).inc()
            for a in assignees:
                assigned_issues.labels(project=project_name, assignee=a["username"]).inc()
        page += 1

def fetch_all_projects():
    url = f"{GITLAB_URL}/api/v4/projects?membership=true&per_page=100"
    r = requests.get(url, headers=headers)
    return r.json() if r.status_code == 200 else []

def collect_metrics():
    while True:
        print("Collecting GitLab issue metrics...")
        open_issues.clear()
        closed_issues.clear()
        assigned_issues.clear()
        for project in fetch_all_projects():
            fetch_issues(project["id"], project["path_with_namespace"])
        time.sleep(SCRAPE_INTERVAL)

if __name__ == "__main__":
    start_http_server(9200)
    collect_metrics()