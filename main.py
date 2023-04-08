from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import pickle
import sqlite3
from sklearn.metrics.pairwise import cosine_similarity

# load the vectorizer from file
with open('vectorizer_0.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

# load the transformed questions from file
qns = np.load('qns.npy',allow_pickle=True)

# create a Flask app
app = Flask(__name__)
CORS(app)

# define a function to transform an input question using the saved vectorizer
def transform_question(input_qn, vectorizer):
    input_qn_vec = vectorizer.transform([input_qn])
    return input_qn_vec

# define a function to compute the cosine similarity between an input question vector and all questions in a dataset
def compute_similarity(input_qn_vec, dataset):
    sim_scores = []
    for qn_vec in dataset:
        sim_score = cosine_similarity(input_qn_vec, qn_vec.reshape(1, -1))[0][0]
        sim_scores.append(sim_score)
    return sim_scores

# define a function to retrieve the top similar questions and their links from a SQLite database
def retrieve_top_questions(top_indices, db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute('SELECT qn, link, idx FROM qas WHERE idx IN ({})'.format(', '.join(['?']*len(top_indices))), top_indices)
    results = cur.fetchall()
    conn.close()
    return results

# define a function to compute the cosine similarity between an input question vector and a set of question vectors
def compute_question_similarity(input_qn_vec, qn_vecs):
    sim_scores = cosine_similarity(input_qn_vec, qn_vecs)[0]
    return sim_scores

# define the route for the API
@app.route('/similar_qns', methods=['POST'])
def similar_qns():
    # get the input question from the POST request
    input_qn = request.json['input_qn']
    
    # transform the input question using the saved vectorizer
    input_qn_vec = transform_question(input_qn, vectorizer)
    
    # compute the cosine similarity between the input question and all questions in the database
    sim_scores = compute_similarity(input_qn_vec, qns)

    
    top_indices = sorted(range(len(sim_scores)), key=lambda i: sim_scores[i], reverse=True)[:3]

    
    # retrieve the top five similar questions and their links from the database
    results = retrieve_top_questions(top_indices, 'new_qa.db')
    
    # get the corresponding question vectors from qns
    qn_vecs = [qns[row[2]] for row in results]
    
    # compute the cosine similarity between the input question vector and the retrieved question vectors
    sim_scores = compute_question_similarity(input_qn_vec, qn_vecs)
    
    # format the results as a list of dictionaries
    result_dicts = [{'qn': row[0], 'link': row[1], 'similarity': sim_scores[i]} for i, row in enumerate(results)]
    
    # sort the results by descending similarity score
    result_dicts = sorted(result_dicts, key=lambda x: x['similarity'], reverse=True)
    
    # return the top five similar questions with their links and similarity scores as JSON
    queries = [v for v in result_dicts[:3] if v['similarity'] < 0.3]
    if not queries:
        queries = [{"qn":"No related queries","link":"#"}]
    
    return jsonify(queries)
