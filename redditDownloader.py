#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" redditDownloader.py - Download posts and comments  from a subreddit

Copyright (C) 2020  Fufu Fang
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; w\without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

__author__ = "Fufu Fang"
__copyright__ = "The GNU General Public License v3.0"

from psaw import PushshiftAPI
import pickle

class RedditGenerator:
    def __init__(self, s_time, e_time):
        """ constructor
        :param s_time: start time as a datetime object
        :param e_time: end time as a datetime object
        """
        s_time = int(s_time.timestamp())
        e_time = int(e_time.timestamp())

    def __iter__(self):
        return self


class RedditPosts(RedditGenerator):
    """ Class for download Reddit posts """

    def __init__(self, s_name, s_time, e_time, download_deleted=False):
        """ constructor
        :param s_name: subreddit name
        :param download_deleted: whether to download deleted posts
        """
        super().__init__(s_time, e_time)
        self.download_deleted = download_deleted
        self._gen = PushshiftAPI().search_submissions(
            subreddit=s_name, after=s_time, before=e_time,
            filter=['title', 'selftext', 'author', 'permalink', 'score',
                    'upvote_ratio', 'removed_by_category', 'created_utc'])

    def __next__(self):
        while True:
            p = next(self._gen)
            if hasattr(p, 'removed_by_category'):
                if self.download_deleted:
                    return p
                else:
                    # skip deleted items if not needed
                    continue
            return p


class RedditComments(RedditGenerator):
    """ Class for download Reddit comments """

    def __init__(self, s_name, s_time, e_time):
        super().__init__(s_time, e_time)
        self._gen = PushshiftAPI().search_comments(
            subreddit=s_name, after=s_time, before=e_time,
            filter=['body', 'author', 'permalink', 'score', 'created_utc'])

    def __next__(self):
        while True:
            p = next(self._gen)
            if p.body == '[removed]':
                # skip empty item
                continue
            return p


if __name__ == '__main__':

    ## Test script ##
    from datetime import timedelta, datetime

    e_time = datetime.now()
    s_time = e_time - timedelta(1)
    post_gen = RedditPosts('pennystocks', s_time, e_time)
    comment_gen = RedditComments('pennystocks', s_time, e_time)
    print(next(post_gen))
    print(next(comment_gen))
    # print('No. submission ' + str(len(list(post_gen))))
    # print('No. comments ' + str(len(list(comment_gen))))
