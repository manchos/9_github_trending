import json
import os

import time
import requests
from urllib.parse import urljoin
import datetime
from datetime import date, timedelta
from collections import namedtuple

TTL =600
URL = 'https://api.github.com'
DAYS_INTERVAL = 7
REPOSITORIES_LIMIT = 20

_expired = datetime.datetime.now() + datetime.timedelta(seconds=TTL)


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


# Декоратор - это функция, ожидающая ДРУГУЮ функцию в качестве параметра
def cache(func):
    def wrapper():
        print("Я - код, который отработает до вызова функции")
        func()
        print("А я - код, срабатывающий после")


class JsonCache(object):
    """Abstract class for caching decorator"""
    file_path = 'cache_json.txt'
    ttl = 20
    expired = None
    cache = None

    def __init__(self, cache_file_path='cache.json', ttl=60):
        # if self.load_json_data():
        #     self.ttl = ttl
        self.ttl = ttl
        self.file_path = cache_file_path
        if not os.path.exists(self.file_path):
            with open(cache_file_path, mode='tw', encoding='utf-8') as file_handler:
                self.expired = 'init'
        try:
            with open(self.file_path, encoding='utf8') as file_handler:
                self.expired = json.load(file_handler)['expired']
        except json.decoder.JSONDecodeError:
            self.expired = 'init'

    def dump_json_data(self, data):
        with open(self.file_path, mode='w', encoding='utf-8') as file_handler:
            json.dump(data, file_handler)

    def load_json_data(self):
        # Return the dictionary of bars
        if not os.path.exists(self.file_path):
            return None
        with open(self.file_path, encoding='utf8') as file_handler:
            return json.load(file_handler)

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            if self.check_expired():
                print(self.expired)
                cache_data = func(*args, **kwargs)
                self.store_data(cache_data)
            else:
                cache_data = self.get_data()
            if cache_data is not None:
                # print(cache_data)
                return cache_data
        return wrapper

    def store_data(self, data):
        _data = {}
        self.set_expired()
        _data['expired'] = self.expired
        _data['cache'] = data
        self.dump_json_data(_data)


    def check_expired(self):
        time = datetime.datetime.now().timestamp()
        if self.expired:
            if self.expired == 'init':
                self.set_expired()
                return True
            if self.expired > datetime.datetime.now().timestamp():
                return False
            else:
                return True

    def set_expired(self):
        self.expired = (datetime.datetime.now() + datetime.timedelta(seconds=self.ttl)).timestamp()

    def get_data(self):
        return self.load_json_data()['cache']

class Cache(JsonCache):
    '''Caching decorator constructor'''


repo1_cache = Cache('cache_repo.txt', 600)
repo_cache = Cache('cache_repo.json', ttl=600)
repo_and_issues = Cache('cache_repo_and_issues.json', ttl=600)
repository_info_class = namedtuple('RepoInfo', ['owner', 'name', 'url', 'issues'])


def get_open_issues_amount(repo_owner, repo_name):
    git_request = requests.get('https://api.github.com/repos/{}/{}/issues'.format(repo_owner, repo_name))
    repo_issues_list = git_request.json()
    return [repo_issue for repo_issue in repo_issues_list if 'pull_request' not in repo_issue]

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


@repo_and_issues
def get_repositories_and_issues(repositories_info):
    repositories_and_issues = []
    for repo in repositories_info:
        issues = get_open_issues_amount(repo['owner']['login'], repo['name'])
        repositories_and_issues.\
            append(repository_info_class(repo['owner']['login'], repo['name'], repo["html_url"], issues))
    return repositories_and_issues



def output_repositories_and_issues(repositories_info):
    for repo in repositories_info:
        print(repo)


if __name__ == '__main__':
    # get_open_issues_amount('developit', 'mitt')
    full = get_trending_repositories(URL, DAYS_INTERVAL, REPOSITORIES_LIMIT)
    fulliss = get_repositories_and_issues(full)
    print()
    for repo in fulliss:
        repo = repository_info_class(*repo)
        print(' \n owner: %s \n name: %s \n url: %s \n\n \t\t Open issues:' % (repo.owner, repo.name, repo.url))
        if (repo.issues):
            for issue in repo.issues:
                #print(' issue url: %s \n' % issue['url'])
                print('\t\t'+issue['url'])
        else:
            print('\t\tThere are no open issues.')
