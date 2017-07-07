#!/usr/bin/python3

import logging
from bs4 import BeautifulSoup
import sys
from pprint import pprint, pformat
import re
from util_data import print_data

def main():
    logging.basicConfig(level=logging.DEBUG)
    filename = sys.argv[1]
    f = open(filename, "r")
    html_raw = f.read()
    page = BeautifulSoup(html_raw, "html.parser")    

    data = []

    def get_preqs_from_raw_string(s):
        s = s.strip()
        s = s.split(" ")
        s = [x for x in s if x not in ["", "a", "alebo"]]
        logging.debug(s)
        return s

    for row in page.find_all("tr"):
        if row.td is None or int(row.td.get("colspan", 0)) > 1:
            #print("!!!", row.td, "\t::::::\t", row)
            continue 
        #logging.debug(str(row.td) + "\t:::\t" + str(row))

        tds = row.find_all("td")
        dato = {}
        dato["id"] = tds[0].text
        dato["fullname"] = tds[2].a.text

        preq_text = tds[2].br.text if tds[2].br is not None else ""
        if len(preq_text) > 0:
            preq_text = preq_text[len("Prerekvizity: "):]
            dato["preqs"] = get_preqs_from_raw_string(preq_text)
        else:
            dato["preqs"] = []
        #logging.debug(dato)
        data.append(dato)

    print_data(data)

if __name__ == "__main__":
    main()
