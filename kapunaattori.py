#!/usr/bin/env python3

import os
from random import choice
import sys

WORDLIST = "kotus_sanat.txt"


def create_cache_file(input, output_filename, filter):
	outfile = open(output_filename, "w")
	for line in input:
		stripped = line.rstrip()
		if filter(stripped):
			outfile.write(stripped)
			outfile.write("\n")

def create_cache_dir(cache_location):
	try:
		os.mkdir(cache_location)
	except OSError:
		pass
	
	# Cache files
	with open(WORDLIST, "r") as word_file:
		words = word_file.readlines()
		filters = [
			# Words that end in "ka"
			["{}/ka.txt".format(cache_location),   lambda s: s.endswith("ka")],

			# Words that start with "pu"
			["{}/pu.txt".format(cache_location),   lambda s: s.startswith("pu")],

			# Just for fun, but we're not getting random results from here
			["{}/kapu.txt".format(cache_location), lambda s: "kapu" in s],
		]

		for f in filters:
			print("Caching {}".format(f[0]), file=sys.stderr)
			create_cache_file(words, *f)


# File cache dir
file_location = os.path.dirname(os.path.realpath(__file__))
cache_location = "{}/cache".format(file_location)
create_cache_dir(cache_location)

ka = open("{}/ka.txt".format(cache_location), "r").readlines()
pu = open("{}/pu.txt".format(cache_location), "r").readlines()

print("{}{}".format(choice(ka).rstrip(), choice(pu).rstrip()))
