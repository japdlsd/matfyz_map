#!/usr/bin/python3

import sys
import logging
from util_data import get_data, print_data, transitive_reduction_analysis, remove_hidden
from pprint import pprint, pformat
from collections import deque

def main():
    logging.basicConfig(level=logging.DEBUG)
    if len(sys.argv) != 3:
        logging.error("WRONG ARGUMENT COUNT!")
        logging.error("python3 txt2sankey.py <input.txt> <output.js>")
        exit(1)

    input_filename, output_filename = sys.argv[1:]
    data = get_data(input_filename)
    data = remove_hidden(data)
    data = transitive_reduction_analysis(data)
    
    courses_by_id = {dato["id"]:(dato, i) for i, dato in enumerate(data)}
    
    def get_charge(dato):
        if "B1" in dato["tags"]: return 10
        if "B2" in dato["tags"]: return min(5, len(dato["preqs"]))
        if "B0" in dato["tags"]: return min(5, len(dato["preqs"]))
        return 1

    #nodes = [{"id": i, "name": dato["fullname"], "shortname": dato["shortname"]} for i, dato in enumerate(data)]
    def short_id(idd):
        if idd[-3] == "/": return idd[:-3]
        return idd
    print(short_id("1-INF-110/12"))

    nodes = [
        {
            "id": i, 
            "name": short_id(dato["id"]) + " " + dato["fullname"], 
            "shortname": short_id(dato["id"]) + " " + dato["shortname"] if len(dato["shortname"]) > 0 else "",
            "charge": get_charge(dato)
        } 
    for i, dato in enumerate(data)]
    
    links = []
    for idd in courses_by_id:
        dato, i = courses_by_id[idd]
        for preq in dato["preqs"]:
            source = courses_by_id.get(preq, None)
            has_substo = (source is not None)
            if not has_substo:
                logging.info("Target: {}: {};\tUnknown course id: {}".format(dato["id"], dato["fullname"], preq))
                for j in range(30):
                    new_preq = preq + "/" + str(j).zfill(2)
                    if new_preq in courses_by_id:
                        logging.info("There is a close match: {}: {};\tWill do :)".format(new_preq, courses_by_id[new_preq][0]["fullname"]))
                        has_substo = True
                        source = courses_by_id[new_preq]
                        break
            #! not elif
            if has_substo:
                source_i = source[1]
                links.append({"target": i, "source": source_i, "value": 1})

    # now just BFS from terminating
    in_edges = [set() for x in range(len(nodes))]
    out_edges = [set() for x in range(len(nodes))]

    for link in links:
        source, target = link["source"], link["target"]
        out_edges[source].add(target)
        in_edges[target].add(source)

    left_out_edges = [len(out_edges[x]) for x in range(len(nodes))]
    q = deque([x for x in range(len(nodes)) if left_out_edges[x] == 0])

    new_links = []
    processed = set()

    while len(q) > 0:
        x = q.popleft()
        if x in processed: continue
        processed.add(x)
        #logging.debug("{} {}".format(x, nodes[x]["name"]))
        if len(in_edges[x]) == 0: continue
        link_val = nodes[x]["charge"] / len(in_edges[x])
        for source in in_edges[x]:
            nodes[source]["charge"] += link_val
            new_links.append({"source": source, "target": x, "value": link_val})
            left_out_edges[source] -= 1
            if left_out_edges[source] == 0:
                q.append(source)

    f = open(output_filename, "w")
    print("var json = ", file=f)
    #print(pformat({"nodes": nodes, "links": links}, width=700), file=f)
    print(pformat({"nodes": nodes, "links": new_links}, width=700), file=f)
    print(";", file=f)
    f.close()

if __name__ == "__main__":
    main()