import pickle
import numpy as np

# Load the vectorizer from the pickle file
with open('vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)
    
answer_arr = np.load("answers.npy",allow_pickle=True)