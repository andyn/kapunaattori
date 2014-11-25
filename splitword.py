#!/usr/bin/env python3
# encoding: utf-8


# Splits a word into multiple parts
def split_word(word):
	if len(word) < 2:
		raise Exception("You obviously need at least two letters to split a word")
	split_indexes = list(range(1, len(word)))
	for i in split_indexes:
		first_part = word[:i]
		second_part = word[i:]
		yield (first_part, second_part)

