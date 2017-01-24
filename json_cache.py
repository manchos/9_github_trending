import json
import os
from cachepy import Cache
import time
import requests
from urllib.parse import urljoin
import datetime
TTL =600

_expired = datetime.datetime.now() + datetime.timedelta(seconds=ttl)







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
    file_path = 'cache_json.txt'
    ttl = 20
    expired = None

    def __init__(self, file_path='cache.json', ttl=60):
        with open(cache_file_path, 'tw', encoding='utf-8') as file_handler:
            try:
                self.expired = json.load(file_handler)['expired']
            except NameError:
                print('Это что ещё такое?')
                self.expired = None
            self.ttl = ttl
            self.file_path = file_path


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
                load_json_data
            if load_json_data(cache_file)
            if result is not None:
                return result
            else:
                func
            return result
        return wrapper


    def store_data(self, data):
        if not self.expired:
            self.expired = datetime.datetime.now() + datetime.timedelta(seconds=self.ttl)
        data['expired'] = self.expired
        data['cache'] = data
        self.dump_json_data(data)


    def check_expired(self):
        if self.expired:
            if self.expired < datetime.datetime.now():
                return False
            else:
                return True


    def get_data(self):
        if self.check_expired():


        datetime.datetime.now().timestamp()
        if ttl and datetime.datetime.now().timestamp() > res[1]:
            res = None
            del self[chash]

class Cache(BaseCache):
    '''Caching decorator constructor'''


if __name__ == '__main__':
    print(get_open_issues_amount('developit', 'mitt'))