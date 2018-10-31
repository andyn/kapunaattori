#!/usr/bin/env python3
# encoding: utf-8

from __future__ import print_function
import os
import sys
import argparse
from random import choice
from splitword import split_word
from wordcache import WordCache


# "This directory" is the directory that contains this script file
THIS_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

# Cache and word list directories. Change if you want them somewhere else
CACHE_DIRECTORY = "{}/cache".format(THIS_DIRECTORY)
WORDLIST_DIRECTORY = "{}/wordlists".format(THIS_DIRECTORY)


def main():
    cache = WordCache(CACHE_DIRECTORY, WORDLIST_DIRECTORY)
    num_words = 1
    word = "kapu"

    parser = argparse.ArgumentParser(description="Creates funny word pairings "
                                     "from lists of words. The default word is kapu.")
    parser.add_argument("word", type=str, nargs='?', help="the word to use")
    parser.add_argument("-n", type=int, help="number of results to generate")
    args = parser.parse_args()

    if args.word:
        word = args.word.lower()
    if args.n:
        num_words = args.n

    # Get all possible positions to split the word
    try:
        parts = list(split_word(word))
    except Exception:
        print(
            "You need at least two letters to get any meaningful results",
            file=sys.stderr)
        sys.exit(1)

    while num_words > 0 and len(parts) > 0:
        first, second = choice(parts)

        try:
            if first == "":
                match = choice(cache.read_matches(second)).rstrip()
                print(match)
            elif second == "":
                match = choice(cache.read_matches(first)).rstrip()
                print(match)
            else:
                prefixes = cache.read_prefix(first)
                suffixes = cache.read_suffix(second)

                print("{}{}".format(
                    choice(prefixes).rstrip(),
                    choice(suffixes).rstrip()))
            num_words -= 1

        except IndexError:
            # Either of the two random.choices got an empty string,
            # so try again with another permutation. Don't try this one again
            parts.remove((first, second))

if __name__ == "__main__":
    main()
