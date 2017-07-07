#!/usr/bin/python3
import sys
import logging
from collections import deque

def get_data(filename):
    f = open(filename, "r")
    data = []
    data_ids = set()
    dato = None
    for line in f:
        line = line.strip()
        if line.find("ID:") == 0:
            dato = {"id": line[len("ID:"):]}
            dato["tags"] = [] # nepovinne, preto mozeme pridat
            if dato["id"] in data_ids:
                #raise Exception("ERROR: mulitple occurences of id:{}".format(dato["id"]))
                logging.warning("Multiple occurences of the same id:{}; SKIPPING".format(dato["id"]))
            data_ids.add(dato["id"])
        if line.find("FULLNAME:") == 0:
            dato["fullname"] = line[len("FULLNAME:"):].strip()
        if line.find("SHORTNAME:") == 0:
            dato["shortname"] = line[len("SHORTNAME:"):].strip()
        if line.find("PREQS") == 0:
            dato["preqs"] = [s.strip() for s in line[len("PREQS:"):].strip().split(",") if len(s) > 0]
        if line.find("TAGS:") == 0:
            dato["tags"] = [s.strip() for s in line[len("TAGS:"):].strip().split(",") if len(s) > 0 ]
        if line == "":
            data.append(dato)
            dato = None
    if dato is not None:
        data.append(dato)
    f.close()
    return data

def print_data(data, filename=None):
    data_ids = set()
    if filename is None:
        f = sys.stdout
    else:
        f = open(filename, "w")
    for dato in data:
        if dato["id"] in data_ids: 
            logging.warning("Multiple occurences of the same id:{}; SKIPPING".format(dato["id"]))
            continue
        data_ids.add(dato["id"])
        print("ID:{}".format(dato["id"]), file=f)
        print("FULLNAME:{}".format(dato["fullname"]), file=f)
        print("SHORTNAME:{}".format(""), file=f)
        print("PREQS:{}".format(",".join(dato["preqs"])), file=f)
        print("TAGS:{}".format(",".join(dato["tags"])), file=f)
        print("", file=f)
    if filename is not None:
        f.close()

def extract_edges(graph_filename, output_edges_filename):
    raise Exception("Not implemented yet!")

def add_edges(input_edges_filename, output_graph_filename):
    raise Exception("Not implemented yet!")

def transitive_reduction_analysis(data):
    # just analysis, doesn't change the data
    edges = {}
    nonredundant = set()
    course_by_id = {dato["id"]:dato for dato in data}
    for dato in data:
        if "NONREDUNDANT" in dato["tags"]:
            nonredundant.add(dato["id"])
        for preq in dato["preqs"]:
            if preq not in edges:
                edges[preq] = set()
            edges[preq].add(dato["id"])

    some_changes = True
    while some_changes:
        some_changes = False
        for source in edges:
            for target in edges[source]:
                if target in nonredundant: continue
                q = deque(edges[source] - set([target]))
                reached = {source}
                while len(q) > 0:
                    x = q.popleft()
                    if x not in reached:
                        reached.add(x)
                        if x not in edges: continue
                        for y in edges[x]:
                            q.append(y)
                if target in reached:
                    logging.info("Edge: {} {} -> {} {} is redundant.".format(source, course_by_id[source]["fullname"], target, course_by_id[target]["fullname"]))
                    edges[source].remove(target)
                    some_changes = True
                    break
    for dato in data:
        dato["preqs"] = [preq for preq in dato["preqs"] if dato["id"] in edges[preq]]
    return data

def remove_hidden(data):
    new_data = [dato for dato in data if "HIDE" not in dato["tags"]]
    logging.debug("Hidden: {} items.".format(len(data) - len(new_data)))
    return new_data