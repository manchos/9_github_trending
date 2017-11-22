import requests
from urllib.parse import urljoin
from datetime import date, timedelta
from collections import namedtuple
from json_cache import Cache
import argparse


URL = 'https://api.github.com'
DAYS_INTERVAL = 7
REPOSITORIES_LIMIT = 20

repo_cache = Cache('cache_repo.json', ttl=600)
repo_and_issues = Cache('cache_repo_and_issues.json', ttl=600)
repository_info_class = namedtuple('RepoInfo', ['owner', 'name', 'url', 'issues_amount'])
TTL = 600


repo_cache = Cache('cache_repo.json', ttl=TTL)
repo_and_issues = Cache('cache_repo_and_issues.json', ttl=TTL)
repository_info_class = namedtuple('RepoInfo', ['owner', 'name', 'url', 'issues'])


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


def get_open_issues(repo_owner, repo_name):
    git_request = requests.get('https://api.github.com/repos/{}/{}/issues'.format(repo_owner, repo_name))
    repo_issues_list = git_request.json()
    return [repo_issue for repo_issue in repo_issues_list if 'pull_request' not in repo_issue]


@repo_and_issues
def get_repositories_and_issues(repositories_info):
    repositories_and_issues = []
    for i, repo in enumerate(repositories_info):
        owner, repo_name = repo['owner']['login'], repo['name']
        issues = get_open_issues(owner, repo_name)
        repositories_and_issues.append(repository_info_class(owner, repo_name, repo["html_url"], issues))
    return repositories_and_issues




def output_repositories_and_issues(repositories_and_issues):
        for repo in repositories_and_issues:
            repo = repository_info_class(*repo)
            print(' \n owner: %s \n name: %s \n url: %s \n\n \t\t Open %d issues:' %
                  (repo.owner, repo.name, repo.url, len(repo.issues)))
            if (repo.issues):
                for issue in repo.issues:
                    print('\t\t %s' % issue['url'])
            else:
                print('\t\t There are no open issues.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Displays 20 the most popular repositories")
    parser.add_argument("-cashetime", "--clear_time", default='', type=str, dest="cache_time", help="Clear cache file")
    parser.add_argument('-clearcache', '--clear_cache', action='store_true', help='Clear cache file"')
    args = parser.parse_args()
    repos = get_trending_repositories(URL, DAYS_INTERVAL, REPOSITORIES_LIMIT)
    repos_and_issues = get_repositories_and_issues(repos)
    output_repositories_and_issues(repos_and_issues)
