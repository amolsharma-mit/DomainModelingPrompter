from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import time

print("Loading model...")
model = SentenceTransformer('all-MiniLM-L6-v2', cache_folder='./models')
print("Model loaded!")

def sim(a, b):
    emb = model.encode([a, b], convert_to_numpy=True)
    return cosine_similarity([emb[0]], [emb[1]])[0][0]

start = time.time()
print(sim("Teacher","Teacher"))
print("Time:", time.time() - start)

