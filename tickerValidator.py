#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" StockValidator - validate whether a work is an actual stock ticker

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

import pickle
import yfinance
import sys


class TickerValidator:
    """This class validates whether a word is a valid ticker code

        We basically "learn" whether a word is a valid ticker code, and store
        it in a database
    """

    def __init__(self, fn):
        """
        constructor
        :param fn: backing file which stores
        """
        self.db = {}
        self.fn = fn
        try:
            self.load(fn)
        except FileNotFoundError:
            print("Creating a new database", file=sys.stderr)
            self.db = {}

    def __del__(self):
        """
        destructor
        """
        self.save(self.fn)

    def load(self, fn):
        """
        load the ticker database
        :param fn: database filename
        """
        with open(fn, "rb") as f:
            self.db = pickle.load(f)

    def save(self, fn):
        """
        save the ticker database
        :param fn: database filename
        """
        with open(fn, "wb") as f:
            pickle.dump(self.db, f)

    def remove(self, sym):
        """
        remove a ticker from the database
        """
        self.db.pop(sym, None)

    def set_sym(self, sym, bool):
        """
        Set a ticker symbol's state.
        """
        self.db[sym] = bool
        return bool

    @staticmethod
    def validate(sym):
        """
        Run an online check for the ticker symbol
        """
        try:
            ticker = yfinance.Ticker(sym)
            ticker.info
            r = True
        except (KeyError, ValueError, IndexError) as e:
            r = False
        return r

    def is_valid(self, sym):
        """
        Check if a ticker symbol is valid
        """
        try:
            r = self.db[sym]
        except KeyError:
            r = self.set_sym(sym, self.validate(sym))
        return r

    def revalidate_all(self):
        """
        revalidate all ticket symbols
        """
        print("")


if __name__ == '__main__':
    # Do something here
    print("Hello world!")
