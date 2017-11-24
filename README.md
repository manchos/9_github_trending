# Github Trends

Displays 20 the most popular repositories from https://api.github.com for the last week.

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)

# Using

Run the script
```#!bash
$ python github_trending.py


optional arguments:
  -h, --help            show this help message and exit
  -cachetime CACHE_TIME, --cache_time CACHE_TIME
                        Set cache time interval
  -clearcache, --clear_cache
                        Clear cache file
```

and get repositories like this:
```#!bash
owner: owner_repository
name: name_repository
url: url_repository

 		 Open n issues:
 		 1_url_repository
 		 .
 		 .
 		 n_url_repository
```

# Requirement

Python >= 3.5

requests==2.18.4

request_cache==0.4.13
