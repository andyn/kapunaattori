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


def main():
	cache = WordCache(CACHE_DIRECTORY, WORDLIST_DIRECTORY)
	params = sys.argv
	num_words = 1
	word = "kapu"

	# Support multiple words at once
	if len(params) > 2 and params[1] == "-n":
		try:
			num_words = int(params[2])
		except ValueError:
			print("{} is not a valid number".format(params[2]), file=sys.stderr)
			sys.exit(1)
		params.pop(1)
		params.pop(1)

	# Allow the user to specify the word
	if len(params) > 1:
		word = params[1].lower()
		params.pop(1)

	# Get all possible positions to split the word
	try:
		parts = list(split_word(word))
	except Exception:
		print("You need at least two letters to get any meaningful results", file=sys.stderr)
		sys.exit(1)
	
	while num_words > 0 and len(parts) > 0:
		first, second = choice(parts)
		try:
			prefixes = cache.open_prefix(first).readlines()
			suffixes = cache.open_suffix(second).readlines()

			print("{}{}".format(
				choice(prefixes).rstrip(),
				choice(suffixes).rstrip()))
			num_words -= 1

		except IndexError:
			# Either of the two random.choices got an empty string,
			# so try again with another permutation. Don't try this one again
			parts.remove((first, second))
			pass


if __name__ == "__main__":
	main()

