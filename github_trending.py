import requests
import requests_cache
from urllib.parse import urljoin
from datetime import date, timedelta
from collections import namedtuple
import argparse

URL = 'https://api.github.com'
DAYS_INTERVAL = 7
REPOSITORIES_LIMIT = 20
repository_info_class = namedtuple('RepoInfo', ['owner', 'name', 'url', 'issues'])


def get_trending_repositories(url, days_interval, repositories_limit):
    search_url = urljoin(url, 'search/repositories')
    days_ago = (date.today() - timedelta(days=days_interval)).isoformat()
    params = {'q': 'created:>{}'.format(days_ago),
              'sort': 'stars',
              'per_page': str(repositories_limit),
              'order': 'desc'
              }
    repositories_full_info = requests.get(search_url, params=params).json()["items"]
    repositories_base_info = get_base_info_list(repositories_full_info)

    return repositories_base_info


def get_base_info_list(repositories_full_info):
    repositories_base_info = []
    for i, repo in enumerate(repositories_full_info):
        owner, repo_name = repo['owner']['login'], repo['name']
        issues = get_open_issues(owner, repo_name)
        repositories_base_info.append(repository_info_class(owner, repo_name, repo["html_url"], issues))
    return repositories_base_info


def get_open_issues(repo_owner, repo_name):
    git_request = requests.get('https://api.github.com/repos/{}/{}/issues'.format(repo_owner, repo_name))
    repo_issues_list = git_request.json()
    return [repo_issue for repo_issue in repo_issues_list if 'pull_request' not in repo_issue]


def output_repositories(repositories_namedtuple):
    for index, repo in enumerate(repositories_namedtuple):
        # repo = repository_info_class(*repo)
        print(
            '\n\n {number} '
            '\n\t owner: {repo.owner}'
            '\n\t name: {repo.name}'
            '\n\t url: {repo.url}'
            '\n\t\t\t Open {N} issues:'.format(number=index+1, repo=repo, N=len(repo.issues))
        )
        if len(repo.issues):
            for issue in repo.issues:
                print('\t\t %s' % issue['url'])



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Displays 20 the most popular repositories")
    parser.add_argument("-cachetime", "--cache_time", default=600, type=int, dest="cache_time", help="Set cache time interval")
    parser.add_argument('-clearcache', '--clear_cache', action='store_true', help='Clear cache file')

    requests_cache.install_cache('_cache/page_cache', backend='sqlite', expire_after=parser.parse_args().cache_time)
    if parser.parse_args().clear_cache:
        requests_cache.clear()

    # response, datetime = requests_cache.get_response_and_time()

    repositories = get_trending_repositories(URL, DAYS_INTERVAL, REPOSITORIES_LIMIT)
    print('\n20 репозиториев, созданные за последнюю неделю, с наибольшим количеством звёзд '
          'с количеством открытых issues со ссылками:')
    output_repositories(repositories)
