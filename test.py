#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" test.py - Test scripts

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

from redditRegexCounter import SubmissionCounter, CommentCounter
from redditDownloader import SubmissionGenerator, CommentGenerator
from tickerValidator import TickerValidator
import os
import pickle


def reddit_downloader_test():
    """ Test redditDownloader.py """
    from datetime import timedelta, datetime

    e_time = datetime.now()
    s_time = e_time - timedelta(1)

    post_gen = SubmissionGenerator("pennystocks", s_time, e_time)
    comment_gen = CommentGenerator("pennystocks", s_time, e_time)

    print(next(post_gen))
    print(next(comment_gen))

    post_fn = "submission-" + post_gen.s_name + \
              str(datetime.now().isoformat()) + ".pickle"
    post_gen.save_all(post_fn)
    comment_fn = "comment-" + post_gen.s_name + \
                 str(datetime.now().isoformat()) + ".pickle"
    comment_gen.save_all(comment_fn)

    with open(post_fn, "rb") as f:
        posts = pickle.load(f)

    with open(comment_fn, "rb") as f:
        comments = pickle.load(f)

    os.remove(post_fn)
    os.remove(comment_fn)

    print("No. submission " + str(len(posts)))
    print(posts[1])
    print("No. comments " + str(len(comments)))
    print(comments[1])


def ticker_validator_test():
    # Test script
    db = TickerValidator("test.db", debug=1)
    print("Checking MSFT")
    print(db.is_valid("MSFT"))
    print("Checking MSFT")
    print(db.is_valid("MSFT"))
    print("Checking INVALID")
    print(db.is_valid("INVALID"))
    print("Checking INVALID")
    print(db.is_valid("INVALID"))
    db.revalidate_all()
    # Need that to avoid warning at exit
    del db


def reddit_regix_counter_test():
    from datetime import timedelta, datetime
    e_time = datetime.now()
    s_time = e_time - timedelta(1)
    s_name = "pennystocks"
    pattern = "[A-Za-z]{3,4}"
    s_counter = SubmissionCounter(s_name, s_time, e_time, pattern, case=1)
    print("s_counter")
    print(s_counter.get_result())
    c_counter = CommentCounter(s_name, s_time, e_time, pattern, case=1,
                               result=s_counter.result)
    print("c_counter")
    print(c_counter.get_result())