import requests
import requests_cache
from datetime import date, timedelta
from collections import namedtuple
import argparse
import json
import os

repository_info_class = namedtuple('RepoInfo', ['owner', 'name', 'url', 'issues'])


def get_repositories_json(url, days_interval, repositories_limit, sort='stars', order='desc'):
    days_ago = (date.today() - timedelta(days=days_interval)).isoformat()
    params = {'q': 'created:>{}'.format(days_ago),
              'sort': sort,
              'per_page': str(repositories_limit),
              'order': order
              }
    try:
        repositories_json = requests.get(url, params=params).json()["items"]
    except (ConnectionError, json.decoder.JSONDecodeError):
        repositories_json = None
    return repositories_json


def get_repositories_base_info_list(repositories_json):
    return [repository_info_class(repo['owner']['login'], repo['name'], repo["html_url"],
                                  get_open_issues(repo['owner']['login'], repo['name']))
            for repo in repositories_json]


def get_open_issues(repo_owner, repo_name):
    git_request = requests.get('https://api.github.com/repos/{}/{}/issues'.format(repo_owner, repo_name))
    repo_issues_list = git_request.json()
    return [repo_issue for repo_issue in repo_issues_list if 'pull_request' not in repo_issue]


def output_repositories(repositories_namedtuple):
    for index, repo in enumerate(repositories_namedtuple):
        print(
            '\n {number} '
            '\n\t owner: {repo.owner}'
            '\n\t name: {repo.name}'
            '\n\t url: {repo.url}'
            '\n\t\t\t Open {N} issues:'.format(number=index+1, repo=repo, N=len(repo.issues))
        )
        if repo.issues:
            for issue in repo.issues:
                print('\t\t %s' % issue['url'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Displays 20 the most popular repositories")
    parser.add_argument("-cachetime", "--cache_time", default=600, type=int,
                        dest="cache_time", help="Set cache time interval")
    parser.add_argument('-clearcache', '--clear_cache', action='store_true', help='Clear cache file')

    if not os.path.exists('_cache'):
        os.mkdir('_cache')
    requests_cache.install_cache('_cache/page_cache', backend='sqlite', expire_after=parser.parse_args().cache_time)

    if parser.parse_args().clear_cache:
        requests_cache.clear()


    repositories_json = get_repositories_json('https://api.github.com/search/repositories', 7, 20)
    if repositories_json is None:
        print('Ошибочные входные данные. Проверьте наличие корректных внешних данных')
    else:
        repositories_list = get_repositories_base_info_list(repositories_json)
        print('\n20 репозиториев, созданные за последнюю неделю, с наибольшим количеством звёзд '
              'с количеством открытых issues со ссылками:')
        output_repositories(repositories_list)
