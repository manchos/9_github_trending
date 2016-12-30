import requests
from urllib.parse import urljoin
from datetime import date, timedelta
from collections import namedtuple

URL = 'https://api.github.com'
DAYS_INTERVAL = 7
REPOSITORIES_LIMIT = 20

repository_info_class = namedtuple('RepoInfo', ['owner', 'name', 'url', 'issues_amount'])


def get_trending_repositories(url, days_interval, repositories_limit):
    search_url = urljoin(url, 'search/repositories')
    days_ago = (date.today() - timedelta(days=days_interval)).isoformat()
    params = {'q': 'created:>{}'.format(days_ago),
              'sort': 'stars',
              'per_page': str(repositories_limit),
              'order': 'desc'
              }
    repositories_info = requests.get(search_url, params=params).json()["items"]
    return repositories_info


def get_open_issues_amount(repo_owner, repo_name):
    git_request = requests.get('https://api.github.com/repos/{}/{}/issues'.format(repo_owner, repo_name))
    repo_issues_list = git_request.json()
    if not repo_issues_list['message']:
        return [repo_issue for repo_issue in repo_issues_list if 'pull_request' not in repo_issue]
    else:
        return None


def get_repositories_and_issues(repositories_info):
    repositories_and_issues = []
    for repo in repositories_info:
        issues = get_open_issues_amount(repo['owner']['login'], repo['name'])
        repositories_and_issues.\
            append(repository_info_class(repo['owner']['login'], repo['name'], repo["html_url"], issues))
    return repositories_and_issues
    # [repository_info_class(repo['owner']['login'], repo['name'], repo["html_url"], [])
    #  for repo in repositories_info]


def output_repositories_and_issues(repositories_info):
    for repo in repositories_info:
        print(repo)


if __name__ == '__main__':
    print(date.today())
    # full = get_trending_repositories(URL, DAYS_INTERVAL, REPOSITORIES_LIMIT)
    print(' ')
    # full_iss = get_repositories_and_issues(full)
#   output_repositories_and_issues(full_iss)
    print(get_open_issues_amount('developit', 'mitt'))
#     print(get_repositories_and_issues(full))
#    &sort = stars
# search?q=cats+stars%3A">+10"
    # created:<2011-01-01
# 'developit', name='mitt'
    search = ">"
    print("https://api.github.com/search/repositories?q=created:>%s&sort=stars&order=desc" % str(date))
