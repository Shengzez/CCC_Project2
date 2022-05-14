CCC Project2
======

[![Python Versions](https://img.shields.io/pypi/pyversions/tweepy?label=Python)](https://pypi.org/project/tweepy/)
[![Twitter API v1.1](https://img.shields.io/endpoint?url=https%3A%2F%2Ftwbadges.glitch.me%2Fbadges%2Fstandard)](https://developer.twitter.com/en/docs/twitter-api/v1)
[![Twitter API v2](https://img.shields.io/endpoint?url=https%3A%2F%2Ftwbadges.glitch.me%2Fbadges%2Fv2)](https://developer.twitter.com/en/docs/twitter-api)
[![Code of Conduct](https://img.shields.io/badge/code%20of%20conduct-Ansible-silver.svg)](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html)
Installation
------------

Use the follow command to clone the project
:

    git clone https://github.com/Shengzez/CCC_Project2.git

Tweet Crawler
------------
Use the follow command to run Tweet Streamer locally
:

    python3 TwitterStreamer/tweetStreamer.py -l [144, -38.4, 145.5, -37.5]

Where [144, -38.4, 145.5, -37.5] is the specifed bouding box for harvesting(south-west and north-east corner) 

Use the follow command to run Tweet Searcher locally
:

    python3 TwitterStreamer/tweetSearcher.py 
    
Python 3.7 - 3.10 are supported.  

Front End
------------
You can view the statistical results by visiting:

 http://172.26.128.133:3000/

Remember to use Unimelb VPN to grant access to our server

Alternatively, install directly from the GitHub repository and run:

    cd /file_path_to_github_package/FrontEnd
    npm i
    npm start

To view the front end locally

Links
-----


- [Twitter API Documentation](https://developer.twitter.com/en/docs/twitter-api)
- [Tweepy](http://www.tweepy.org/)
- [CouchDB](https://github.com/djc/couchdb-python/)
- [Flask](https://flask-restful.readthedocs.io/en/latest/ )
- [Ansible](https://docs.ansible.com/ansible/latest/index.html )
- [Docker](https://docs.docker.com/)
- [Youtube](https://Youtube.com)
