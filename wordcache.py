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
		except:  # FIXME Pokemon exceptions because ocumentation says "except error" but it does not work
			# Already exists
			print("Directory {} already exists ".format(self.directory), file=sys.stderr)
			pass

	def open(self, file, *args, **kwargs):
		filename = "{}/{}".format(self.directory, file)
		print("Opening {}".format(filename), file=sys.stderr)
		return open(filename, *args, **kwargs)


# Caches files from a certain directory
class WordCache(object):
	def __init__(self, cache_directory, wordlist_directory):
		# Remove and recreate cache directories if needed
		prefix_dir = "{}/prefix".format(cache_directory)
		suffix_dir = "{}/suffix".format(cache_directory)
		self.remove_if_older_than(prefix_dir, wordlist_directory)
		self.remove_if_older_than(suffix_dir, wordlist_directory)
		self.prefixes = Directory(prefix_dir)
		self.suffixes = Directory(suffix_dir)
		self.wordlists = wordlist_directory

	def create_file(self, target, filter):
		from os import listdir
		from os.path import isfile, join

		print(self.wordlists)
		source_filenames = [join(self.wordlists, f) for f in listdir(self.wordlists)
			if isfile(join(self.wordlists, f))]
		source_files = [open(f, "r") for f in source_filenames]
		for source in source_files:
			for line in source:
				stripped = line.rstrip()
				if filter(stripped):
					print(stripped)
					target.write("{}\n".format(stripped))
			source.close()

	@staticmethod
	def remove_if_older_than(remove_me, compare_to):
		try:
			removable_time = time.ctime(os.path.getmtime(remove_me))
			print(removable_time)
		except OSError:
			# Already removed, all good
			print("Dir {} does not exist".format(remove_me), file=sys.stderr)
			return False

		# If comparison directory is missing, this shall raise (=nothing to compare against)
		comparison_time = time.ctime(os.path.getmtime(compare_to))
		print(comparison_time)

		if (removable_time < comparison_time):
			shutil.rmtree(remove_me, ignore_errors=True)
			print("Dir {} is older than {}".format(remove_me, compare_to), file=sys.stderr)
			return True
		
		print("Dir {} is newer than {}".format(remove_me, compare_to), file=sys.stderr)
		return False

	def open_prefix(self, name):
		try:
			return self.prefixes.open(name, "r")
		except IOError:
			pass

		# Does not exist, create
		target = self.prefixes.open(name, "w")
		self.create_file(target, lambda l: l.endswith(name))
		return self.prefixes.open(name, "r")
					
	def open_suffix(self, name):
		try:
			return self.suffixes.open(name, "r")
		except IOError:
			pass

		# Does not exist, create
		target = self.suffixes.open(name, "w")
		self.create_file(target, lambda l: l.startswith(name))
		return self.suffixes.open(name, "r")


