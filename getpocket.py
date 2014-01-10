#!/usr/bin/env python
#
# vim: sw=4 ts=4 st=4
#
#  Copyright 2014 Felipe Borges <felipe10borges@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

'''A library that provides a Python interface to the Pocket API'''

__author__ = 'felipe10borges@gmail.com'
__version__ = '0.1'

import urllib
import urllib2
import simplejson
import sys

REQUEST_URI = 'http://github.com/felipeborges'

class Item(object):
    '''A Class representing a saved item.

    The Item structure exposes the folowing properties:

        item.id
        item.normal_url
        item.resolved_id
        item.resolved_url
        item.domain_id
        item.origin_domain_id
        item.response_code
        item.mime_type
        item.content_length
        item.encoding
        item.date_resolved
        item.date_published
        item.title
        item.excerpt
        item.word_count
        item.has_image
        item.has_video
        item.is_index
        item.is_article
        item.authors
        item.images
        item.videos
    '''
    def __init__(self, **kwargs):
        param_defaults = {
            'id' : None,
            'normal_url' : None,
            'resolved_id' : None,
            'resolved_url' : None,
            'domain_id' : None,
            'origin_domain_id' : None,
            'response_code' : None,
            'mime_type' : None,
            'content_length' : None,
            'encoding' : None,
            'date_resolved' : None,
            'date_published' : None,
            'title' : None,
            'excerpt' : None,
            'word_count' : None,
            'has_image' : None,
            'has_video' : None,
            'is_index' : None,
            'is_article' : None,
            'authors' : None,
            'images' : None,
            'videos' : None,
        }

        for (param, default) in param_defaults.iteritems():
            setattr(self, param, kwargs.get(param, default))

    def get_id(self):
        '''Get the unique identifier of this item.

        Returns:
            The unique id of this item.
        '''
        return self._id

    def set_id(self, id):
        '''Set the unique identifeir of this item.

        Args:
            id: 
                The unique id of this item.
        '''
        self._id = id

    def get_normal_url(self):
        '''Get the original url of this item.

        Returns:
            The original url for this item.
        '''
        return self._normal_url

    def get_resolved_id(self):
        '''Get the unique identifier of this resolved item.

        Returns:
            The resolved id of this item.
        '''
        return self._resolved_id



class PocketError(Exception):
    def __init__(self, reason, response = None):
        self.reason = unicode(reason)
        self.response = response

    def __str__(self):
        return self.reason

class Api(object):
    METHOD_URL = 'https://getpocket.com/v3/'
    REQUEST_HEADERS = { 'X-Accept': 'application/json' }

    ''' Pocket API '''
    def __init__(self, consumer_key = None, access_token = None, redirect_uri = REQUEST_URI):
        if consumer_key is not None and access_token is None:
            print >> sys.stderr, 'Pocket requires an Authentication Token for API calls.'
            print >> sys.stderr,  'If you are using this library from a command line utility, please'
            print >> sys.stderr,  'run the included get_access_token.py tool to generate one.'

            raise PocketError('Pocket requires an Authentication Token for all API access')

        self.set_credentials(consumer_key, access_token)

    def set_credentials(self, consumer_key, access_token):
        self._consumer_key = consumer_key
        self._access_token = access_token

    def _create_request(self, method, params):
        return urllib2.Request(Api.METHOD_URL + method, urllib.urlencode(params), Api.REQUEST_HEADERS)

    def add(self, url, title = None, tags = None, tweet_id = None):
        '''Add a Single Item to a user's Pocket list

        Args:
            url:
                The URL of the item you want to save.
            title:
                This can be included for cases where an item does not have a 
                title, which is typical for image or PDF URLs. If Pocket detects
                a title from the content of the page, this parameter will be 
                ignored.
            tags:
                A comma-separated list of tags to apply to the item.
            tweet_id:
                A reference to the tweet status id. This allows Pocket to show 
                the original tweet alongside the article.

        Returns:
            A getpocket.Item instance.
        '''
        params = {
            'consumer_key' : self._consumer_key,
            'access_token' : self._access_token,
            'url' : url
        }

        if title is not None:
            params['title'] = title

        if tags is not None:
            tag_str = ''
            for tag in tags:
                tag_str += tag + ','

            params['tags'] = tag_str

        if tweet_id is not None:
            params['tweet_id'] = tweet_id

        request = self._create_request('add', params)

        try:
            resp = urllib2.urlopen(request)
        except Exception, e:
            raise PocketError(e)

        json_response = simplejson.loads(resp.read())

        return self.new_from_json_dict(json_response)

    @staticmethod
    def new_from_json_dict(data):
        '''Create a new instanced based on a JSON dict.

        Args:
            data:
                A JSON dict, as converted from the JSON in the Pocket API

        Returns:
            A getpocket.Item instance
        '''
        item = data['item']
        status = data['status']

        return Item(id = item.get('id'),
                    normal_url = item.get('normal_url'),
                    resolved_id = item.get('resolved_id'),
                    resolved_url = item.get('resolved_url'),
                    domain_id = item.get('domain_id'),
                    origin_domain_id = item.get('origin_domain_id'),
                    response_code = item.get('response_code'),
                    mime_type = item.get('mime_type'),
                    content_length = item.get('content_length'),
                    encoding = item.get('encoding'),
                    date_resolved = item.get('date_resolved'),
                    date_published = item.get('date_published'),
                    title = item.get('title'),
                    excerpt = item.get('excerpt'),
                    word_count = item.get('word_count'),
                    has_image = item.get('has_image'),
                    has_video = item.get('has_video'),
                    is_index = item.get('is_index'),
                    is_article = item.get('is_article'),
                    authors = item.get('authors'),
                    images = item.get('images'),
                    videos = item.get('videos'))
