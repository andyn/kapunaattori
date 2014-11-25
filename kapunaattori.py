#!/usr/bin/env python3
# encoding: utf-8


from __future__ import print_function
import os
from random import choice
from splitword import split_word
import sys
from wordcache import WordCache


# "This directory" is the directory that contains this script file
THIS_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

# Cache and word list directories. Change if you want them somewhere else
CACHE_DIRECTORY = "{}/cache".format(THIS_DIRECTORY)
WORDLIST_DIRECTORY = "{}/wordlists".format(THIS_DIRECTORY)


cache = WordCache(CACHE_DIRECTORY, WORDLIST_DIRECTORY)

# Use either a user-supplied word or the default, "kapu"
if len(sys.argv) > 1:
	word = sys.argv[1]
else:
	word = "kapu"

# Try ones split in the middle first
for (first, second) in split_word(word):
	try:
		prefixes = cache.open_prefix(first).readlines()
		suffixes = cache.open_suffix(second).readlines()

		print("{}{}".format(
			choice(prefixes).rstrip(),
			choice(suffixes).rstrip()))
		break

	except IndexError:
		# Either of the two random.choices got an empty string,
		# so try again with another permutation
		pass

