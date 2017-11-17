# Github Trends

Displays 20 the most popular repositories from https://api.github.com for the last week.

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)

# Using

Run the script
```#!bash
$ python github_trending.py
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

requests==2.11.1