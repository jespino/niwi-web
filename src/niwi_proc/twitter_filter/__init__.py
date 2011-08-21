# -*- coding: utf-8 -*-

from celery.decorators import task
from django.utils import simplejson
from niwi.models import Link
import requests

@task(name="filter-twitter-links")
def filter_links():
    response = requests.get("http://api.twitter.com/1/statuses/user_timeline.json?count=6&screen_name=niwibe&include_rts=true&include_entities=true")
    if response.status_code != 200:
        return False

    tweets = simplejson.loads(response.content)
    for tweet in tweets:
        if "entities" not in tweet:
            continue

        entities = tweet['entities']
        if 'hashtags' not in entities:
            continue

        valid_hashtag = False
        for htag in entities['hashtags']:
            if "text" in htag and htag['text'] == 'niwibe':
                valid_hashtag = True
                break
        
        if not valid_hashtag:
            continue

        if "urls" not in entities:
            continue
        
        urls_list = []
        for url in entities['urls']:
            if "expanded_url" in url:
                urls_list.append(url["expanded_url"])
            elif "url" in url:
                urls_list.append(url["url"])

        counter = 0
        for url in urls_list:
            if Link.objects.filter(url=url).exists():
                continue
            
            Link.objects.create(url=url)
            counter += 1

        return counter
