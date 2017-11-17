
import json
import os
import datetime


class JsonCache(object):
    """Abstract class for caching decorator"""
    file_path = 'cache_json.txt'
    ttl = 20
    expired = None
    cache = None

    def __init__(self, cache_file_path='cache.json', ttl=60):
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
                return cache_data
        return wrapper

    def store_data(self, data):
        _data = {}
        self.set_expired()
        _data['expired'] = self.expired
        _data['cache'] = data
        self.dump_json_data(_data)

    def check_expired(self):
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
    pass

