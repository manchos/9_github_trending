import json
import os
from cachepy import Cache
import time
import requests
from urllib.parse import urljoin
import datetime
TTL =600

_expired = datetime.datetime.now() + datetime.timedelta(seconds=ttl)

def dump_json_data(filepath, data):
    with open(filepath, mode='w', encoding='utf-8') as f:
        json.dump(data, f)


def load_json_data(filepath):
    # Return the dictionary of bars
    if not os.path.exists(filepath):
        return None
    with open(filepath, encoding='utf8') as file_handler:
        return json.load(file_handler)


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


class BaseCache(object):
    """Abstract class for caching decorator"""

    def __init__(self, cache_file_path='cache.json', ttl=60):
        with open(cache_file_path, 'tw', encoding='utf-8') as f:
            pass
        self.ttl = ttl


        load_json_data(cache_file)
        self.ttl = ttl

    def dump_json_data(filepath, data):
        with open(filepath, mode='w', encoding='utf-8') as f:
            json.dump(data, f)

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            result = self.backend.get_data(chash, ttl=self.ttl)

            if result is not None:
                return result
            else:
                result = func(*args, **kwargs)
                self.backend.store_data(chash, result, key=self.key,
                                        ttl=self.ttl, noc=self.noc, ncalls=0)
            if isinstance(self.backend, FileBackend):
                self.backend.sync()
            return result
        return wrapper

class Cache(BaseCache):
    '''Caching decorator constructor'''


if __name__ == '__main__':
