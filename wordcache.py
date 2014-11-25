#!/usr/bin/env python3
# encoding: utf-8


from __future__ import print_function
import os
import shutil
import sys
import time


# A simple class that allows opening files from a certain directory.
# Makes sure that the directory exists.
class Directory(object):
	def __init__(self, base_directory):
		try:
			self.directory=base_directory
			os.makedirs(self.directory)
			print("Created directory {}".format(self.directory), file=sys.stderr)
		except error:
			# Already exists
			print("Directory {} already exists ".format(self.directory), file=sys.stderr)
			pass

	def open(self, file, *args, **kwargs):
		filename = "{}{}".format(self.directory, prefix)
		print("Opening {}".format(filename), file=sys.stderr)
		return open(filename, *args, **kwargs)


# Caches files from a certain directory
def WordCache(object):
	def __init__(self, cache_directory, wordlist_directory):
		# Remove and recreate cache directories if needed
		prefix_dir = "{}/prefix".format(cache_directory)
		suffix_dir = "{}/suffix".format(cache_directory)
		remove_if_newer_than(prefix_dir, cache_directory)
		remove_if_newer_than(suffix_dir, cache_directory)
		self.prefixes = Directory(prefix_dir)
		self.suffixes = Directory(suffix_fir)
		self.wordlists = wordlist_directory

	@staticmethod
	def create_file(target, filter):
		from os import listdir
		from os.path import isfile, join

		sources = [open(f, "r") for f in listdir(self.wordlists)
			if isfile(join(self.wordlists, f))]
		for source in sources:
			for line in source:
				stripped = line.rstrip()
				if filter(strippped):
					target.write("{}\n".format(stripped))
				source.close()

	@staticmethod
	def remove_if_newer_than(remove_me, compare_to):
		try:
			removable_time = time.ctime(os.path.getmtime(remove_me))
		except OSError:
			# Already removed, all good
			return False

		# If comparison directory is missing, this shall raise (=nothing to compare to)
		comparison_time = time.ctime(os.path.getmtime(compare_to))

		if (removable_time > comparison_time):
			shutil.rmtree(remove_me, ignore_errors=True)
			return True
		return False

	def open_prefix(self, name):
		try:
			return self.prefixes.open(file, "r")
		except OSError:
			pass

		# Does not exist, create
		target = self.prefixes.open(name, "w")
		self.create_file(target, lambda l: l.endswith("name"))
		return self.prefixes.open(file, "r")
					
	def open_suffix(self, name):
		try:
			return self.suffixes.open(file, "r")
		except OSError:
			pass

		# Does not exist, create
		target = self.suffixes.open(name, "w")
		self.create_file(target, lambda l: l.startswith("name"))
		return self.suffixes.open(file, "r")


