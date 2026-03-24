import pandas as pd
import numpy as np
import requests

import utils

from flask import (
    Flask, request, abort, 
    render_template, url_for, 
    jsonify, send_file
    )

# Read in dataframes for NUS-DSA, NTU and SMU
smu_df = pd.read_csv('data/smu.csv')
ntu_df = pd.read_csv('data/ntu.csv')
nus_dsa_df = pd.read_csv('data/nus-dsa.csv')

def switch(uni_name):
    if uni_name.lower() == "nus":
        return nus_dsa_df
    elif uni_name.lower() == "ntu":
        return ntu_df
    else:
        return smu_df

app = Flask(__name__)

@app.route("/prereq/<string:mod_code>", methods=["POST"])
def check_prereq(mod_code):
    # get pre-req tree for mod_code
    mod_code = mod_code.upper()
    response = requests.get(f'https://api.nusmods.com/v2/2025-2026/modules/{mod_code}.json')
    prereq_tree = response.json()['prereqTree']

    # get modules done
    out = request.json

    # check prerequisites
    check_flag = utils.satisfies_prerequisites(prereq_tree, out)
    return jsonify(check_flag)
        
@app.route("/getgraph/<string:mod_code>", methods=["GET"])
def get_graph(mod_code):
    # get pre-req tree for mod_code
    mod_code = mod_code.upper()
    response = requests.get(f'https://api.nusmods.com/v2/2025-2026/modules/{mod_code}.json')
    prereq_tree = response.json()['prereqTree']

    G = utils.build_graph_from_prereq(prereq_tree)
    img_bytes = utils.draw_prereq_graph(G)
    return send_file(img_bytes, 
                     mimetype="image/png") 

@app.route("/similarity/concepts", methods=["GET"])
def compute_sim_concepts():
    uni1 = switch(request.args.get("uni1"))
    uni2 = switch(request.args.get("uni2"))
    mod1 = request.args.get("mod1")
    mod2 = request.args.get("mod2")
    mod1 = mod1.upper()
    mod2 = mod2.upper()

    k1 = uni1[uni1.module_code == mod1].key_concepts.iloc[0] 
    k2 = uni2[uni2.module_code == mod2].key_concepts.iloc[0] 

    sim_score = utils.jacc_sim(k1, k2)

    return jsonify(sim_score)
