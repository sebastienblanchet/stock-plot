#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" redditTickerCounter.py - count the number of stock ticker mentions in a
subreddit

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
from tickerValidator import TickerValidator


def print_ticker_count(tbl):
    """ print a ticker count table. 
    
    :param tbl: the input dictionary with ticker count
    :return: a string containing the formatted output
    """
    s = "ticker:\tcount:\n"
    for i in tbl.items():
        s += str(i[0]) + "\t" + str(i[1]) + "\n"
    return s


def count_subreddit_ticker(s_name, s_time, e_time, dbfn, result=None, debug=0):
    """ count the stock ticker mention in a subreddit.

    :param s_name: subreddit name
    :param s_time: start time as a datetime object
    :param e_time: end time as a datetime object
    :param dbfn:  backing file which stores the ticker database
    :param result: optionally result table from a previous run - the results
                from a new run will be added to this table
    :param debug: whether we get the TickerValidator to print debug messages
    :return: a dictionary containing the the number of mentions of each valid
            ticker symbol
    """
    if result is None:
        result = {}
    pattern = r"\b[a-z]{3,5}\b|\b[A-Z]{3,5}\b"
    s_counter = SubmissionCounter(s_name, s_time, e_time, pattern, case=1,
                                  result=result)
    s_counter.get_result()
    c_counter = CommentCounter(s_name, s_time, e_time, pattern, case=1,
                               result=s_counter.result)
    c_counter.get_result()

    validator = TickerValidator(dbfn, debug)
    validator.validate_dict(c_counter.result)
    return result
