from flask import Flask
from flask import render_template
from flask import request,jsonify
import sqlite3
import numpy as np
import pickle
import json
from sklearn.metrics.pairwise import cosine_similarity


appl = Flask(__name__)

# Load the array from the binary file
answer_arr = np.load('answers.npy',allow_pickle=True)

# Load the vectorizer from the pickle file
with open('vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

with open("metrics.json",'r') as f:
    metrics = json.loads(f.read())

@appl.route("/answers")
def answers():
    qn = request.args.get("qn")
    qn_vector = vectorizer.transform([qn])
    tmp = {"index":0,"value":0,"related":[]}
    minimum = metrics["mean"] - metrics["std"]
    for i,ans_arr in enumerate(answer_arr):
        similar = cosine_similarity(qn_vector,ans_arr)
        if similar[0][0] < minimum:
            continue
        if similar[0][0]>tmp["value"]:
            tmp["related"].insert(0,i)
            tmp["index"] = i
            tmp["value"] = similar[0][0]
    
    if not tmp["value"]:
        return jsonify({"data":None})
    
    conn = sqlite3.connect('qa.db')
    c = conn.cursor()
    faq_ids = [k+1 for k in tmp["related"]]
    placeholders = ','.join(['?' for _ in faq_ids])
    query = f"SELECT * FROM faqs WHERE id IN ({placeholders})"

    c.execute(query, faq_ids)
    rows = c.fetchall()
    results = sorted(rows,key=lambda fa:tmp["related"].index(fa[0]-1))
    faq = results.pop(0)
    # Close the database connection
    conn.close()
    return jsonify({"data":{
            'id': faq[0],
            'topic': faq[1],
            'link': faq[2],
            'qn': qn,
            'ans': faq[4]
        },"related":[{"qn":v[3],"link":v[2]} for v in results]})

    

@appl.route('/')
def index():
    return render_template("index.html")

