#!/usr/bin/python3

from util_data import get_data, print_data
import sys

if __name__ == "__main__":
    data = get_data(sys.argv[1])
    print_data(data, sys.argv[1])