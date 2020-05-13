#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" redditRegexCounter.py - count the number of regex matches in a subreddit

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

from redditDownloader import SubmissionGenerator, CommentGenerator
import pickle
import re


class RegexCounter:
    """Class for counting the number of regex appearance from a generator
    """

    def __init__(self, gen, attr, pattern, case=0, dict=None):
        """
        :param gen: the generator for the items
        :param attr: the attributes within the item which contain the text
        :param pattern: the regex pattern to search
        :param case: whether we want to perform case conversion:
            - -1, convert to lower caser
            - 0, does not perform case conversion
            - 1, convert to upper case
        :param dict: the optional dictionary which contains previous results
        """
        if dict is None:
            dict = {}
        self._gen = gen
        self.attr = attr
        self.pattern = pattern
        self.case = case
        self.dict = dict

    def __iter__(self):
        return self

    def __next__(self):
        item = next(self._gen)
        for attr in self.attr:
            extracted = re.findall(self.pattern, getattr(item, attr))
            for word in extracted:
                if self.case == 0:
                    pass
                elif self.case == -1:
                    word = word.lower()
                elif self.case == 1:
                    word = word.upper()
                else:
                    raise ValueError("case must be either -1, 0, or 1")

                if word in self.dict:
                    self.dict[word] += 1
                else:
                    self.dict[word] = 1
        return self.dict

    def save_dict(self, fn):
        with open(fn, "wb") as f:
            pickle.dump(self.dict, f)

    def load_dict(self, fn):
        with open(fn, "rb") as f:
            self.dict = pickle.load(f)

    def get_result(self):
        for i in self:
            pass
        return self.dict


class SubmissionCounter(RegexCounter):
    """ Class for counting regex in a Reddit submission """

    def __init__(self, s_name, s_time, e_time, pattern, case=0, dict=None,
                 download_deleted=False):
        """
        :param s_name: subreddit name
        :param s_time: start time as a datetime object
        :param e_time: end time as a datetime object
        :param pattern: the regex pattern to search
        :param case: whether we want to perform case conversion:
            - -1, convert to lower caser
            - 0, does not perform case conversion
            - 1, convert to upper case
        :param dict: the optional dictionary which contains previous results
        :param download_deleted: whether to download deleted posts
        """
        if dict is None:
            dict = {}
        super().__init__(SubmissionGenerator(s_name, s_time, e_time,
                                             download_deleted),
                         ['title', 'selftext'], pattern, case, dict)


class CommentCounter(RegexCounter):
    """ Class for counting regex in a Reddit comment"""

    def __init__(self, s_name, s_time, e_time, pattern, case=0, dict=None):
        """
        :param s_name: subreddit name
        :param s_time: start time as a datetime object
        :param e_time: end time as a datetime object
        :param pattern: the regex pattern to search
        :param case: whether we want to perform case conversion:
            - -1, convert to lower caser
            - 0, does not perform case conversion
            - 1, convert to upper case
        :param dict: the optional dictionary which contains previous results
        """
        if dict is None:
            dict = {}
        super().__init__(CommentGenerator(s_name, s_time, e_time),
                         ['body'], pattern, case, dict)


if __name__ == '__main__':
    ## Test script

    from datetime import timedelta, datetime
    e_time = datetime.now()
    s_time = e_time - timedelta(1)
    s_name = 'pennystocks'
    pattern = "[A-Za-z]{3,4}"
    s_counter = SubmissionCounter(s_name, s_time, e_time, pattern, case=1)
    c_counter = CommentCounter(s_name, s_time, e_time, pattern, case=1)
    print('s_counter')
    print(s_counter.get_result())
    print('c_counter')
    print(c_counter.get_result())