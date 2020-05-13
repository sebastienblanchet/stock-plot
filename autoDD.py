#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" AutoDD - Automatically does the so called "due diligence" for you.

Copyright (C) 2020  Fufu Fang
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

__author__ = "Fufu Fang"
__copyright__ = "The GNU General Public License v3.0"

from redditTickerCounter import count_subreddit_ticker, print_ticker_count
from datetime import timedelta, datetime

if __name__ == '__main__':
    e_time = datetime.now()
    s_time = e_time - timedelta(1)
    t = count_subreddit_ticker("pennystocks", s_time, e_time,
                               "tickers.pickle", debug=1)
    print_ticker_count(t)