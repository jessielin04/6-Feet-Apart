print("starting...") #debuggg g g gg

from flask import Flask, jsonify, request
import csv
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

#import oreoluwa's backend 
from hash_map_graph import HashMapGraph
from redblacktree_graph import RBTreeGraph
from BFS import bfs_shortest_path

app = Flask(__name__)

@app.after_request
#CORS HEADERES
def add_cors(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response

hash_graph = HashMapGraph()
rb_graph   = RBTreeGraph()
data_loaded = False

def load_data():
    global data_loaded
    edges_file = "large_twitch_edges.csv"
    with open(edges_file, "r") as f:
        reader = csv.reader(f)
        next(reader) #skip header bcs it's just column names :B
        #for-loop: iterates through every row
        for row in reader:
            #if-condition: less than 2 rows = skip grrr
            if len(row) < 2:
                continue
            try:
                u = int(row[0])
                v = int(row[1])
                hash_graph.add_edge(u, v)
                rb_graph.add_edge(u, v)
            except ValueError:
                continue
    data_loaded = True
load_data()

#TO-DO: work on error cases handling + page
@app.route("/search")
def search():
    #get user input values 
    a_str = request.args.get("a")
    b_str = request.args.get("b")
    #if-condition: nonnumeric input = error 
    if not a_str or not b_str:
        return jsonify({"error": "nonnumeric"}), 400
    try:
        a = int(a_str)
        b = int(b_str)
    except ValueError:
        return jsonify({"error": "nonnumeric"}), 400
    #if-condition: does userID exist? if no = error
    if not hash_graph.has_node(a):
        return jsonify({"error": "notfound"}), 404
    if not hash_graph.has_node(b):
        return jsonify({"error": "notfound"}), 404
    
    hash_result = bfs_shortest_path(hash_graph, a, b, "HashMap")
    rb_result   = bfs_shortest_path(rb_graph,   a, b, "RBTree")

    #if-conditionL: no relationship :[
    if not hash_result.found:
        return jsonify({"error": "nopath"}), 404

    #send my data to me plz
    return jsonify({
        "path":    hash_result.path,
        "degrees": hash_result.degrees,
        "hash":    hash_result.to_dict(),
        "rbtree":  rb_result.to_dict(),
    })

if __name__ == "__main__":
    print("server starting on port 5000")
    app.run(debug=False, port=5000)