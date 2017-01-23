import requests
from urllib.parse import urljoin
from datetime import date, timedelta
from collections import namedtuple
import json
import os
from cachepy import Cache
import time
from functools import lru_cache

URL = 'https://api.github.com'
DAYS_INTERVAL = 7
REPOSITORIES_LIMIT = 20
repo_cache = Cache('cache_repo.dat', ttl=600)
repo_and_issues = Cache('cache_repo_and_issues.dat', ttl=600)

repository_info_class = namedtuple('RepoInfo', ['owner', 'name', 'url', 'issues_amount'])







#os.stat('/file1.txt').st_mtime

@repo_cache
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
    if not os.path.exists('json.txt') or (time.time() - os.stat('json.txt').st_mtime/60) > 10:
        git_request = requests.get('https://api.github.com/repos/{}/{}/issues'.format(repo_owner, repo_name))
        repo_issues_list = git_request.json()
        aas = [repo_issue for repo_issue in repo_issues_list if 'pull_request' not in repo_issue]
        ars = {(repo_owner, repo_name): aas}
        dump_json_data('json.txt', ars)
    else:
        issues = load_json_data('json.txt')
    return issues


@repo_and_issues
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
 #   full = get_trending_repositories(URL, DAYS_INTERVAL, REPOSITORIES_LIMIT)
  #  print(os.stat('json.txt').st_mtime)
  #  print((time.time() - os.stat('json.txt').st_mtime)/60)
    # full_iss = get_repositories_and_issues(full)
  # output_repositories_and_issues(full_iss)
    print(get_open_issues_amount('developit', 'mitt'))
#    print(get_repositories_and_issues(full))
#    &sort = stars
# search?q=cats+stars%3A">+10"
    # created:<2011-01-01
# 'developit', name='mitt'
    search = ">"
    print("https://api.github.com/search/repositories?q=created:>%s&sort=stars&order=desc" % str(date))
