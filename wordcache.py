#!/usr/bin/env python3
# encoding: utf-8


from __future__ import print_function
import os
import shutil
import time

# A simple class that allows opening files from a certain directory.
# Makes sure that the directory exists.


class Directory(object):

    def __init__(self, base_directory):
        try:
            self.directory = base_directory
            os.makedirs(self.directory)
        # FIXME Pokemon exceptions because ocumentation says "except error" but
        # it does not work
        except:
            # Already exists
            pass
        self.open_files = {}

    def open(self, name, *args, **kwargs):
        filename = "{}/{}".format(self.directory, name)
        handle = open(filename, *args, **kwargs)
        return handle


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
        self.cached_prefixes = {}
        self.cached_suffixes = {}

    def create_file(self, target, filter):
        from os import listdir
        from os.path import isfile, join

        source_filenames = [
            join(self.wordlists, f) for f in listdir(self.wordlists)
            if isfile(join(self.wordlists, f))]
        source_files = [open(f, "r") for f in source_filenames]
        for source in source_files:
            for line in source:
                stripped = line.rstrip().lower()
                if filter(stripped):
                    target.write("{}\n".format(stripped))
            source.close()

    @staticmethod
    def remove_if_older_than(remove_me, compare_to):
        try:
            removable_time = time.ctime(os.path.getmtime(remove_me))
        except OSError:
            # Already removed, all good
            return False

        # If comparison directory is missing, this shall raise (=nothing to
        # compare against)
        comparison_time = time.ctime(os.path.getmtime(compare_to))

        if removable_time < comparison_time:
            shutil.rmtree(remove_me, ignore_errors=True)
            return True

        return False

    def open(self, directory, name, filter):
        try:
            return directory.open(name, "r")
        except IOError:
            pass

        # File does not exist, create
        target = directory.open(name, "w")
        self.create_file(target, filter)

        # Reopen the newly created file
        return directory.open(name, "r")

    def open_prefix(self, name):
        return self.open(self.prefixes, name, lambda l: l.endswith(name))

    def open_suffix(self, name):
        return self.open(self.suffixes, name, lambda l: l.startswith(name))

    # TODO refactor these two into one large function
    def read_prefix(self, name):
        cached = self.cached_prefixes.get(name)
        if cached:
            return cached

        handle = self.open_prefix(name)
        lines = handle.readlines()
        self.cached_prefixes[name] = lines
        return lines

    def read_suffix(self, name):
        cached = self.cached_suffixes.get(name)
        if cached:
            return cached

        handle = self.open_suffix(name)
        lines = handle.readlines()
        self.cached_suffixes[name] = lines
        return lines
