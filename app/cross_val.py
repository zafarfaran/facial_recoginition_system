from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsClassifier
import pickle
with open('D:/Projects/facial_recoginition_system/encodings/names.pkl', 'rb') as w:
    LABELS=pickle.load(w)
with open('D:/Projects/facial_recoginition_system/encodings/faces_data.pkl', 'rb') as f:
    FACES=pickle.load(f)
neighbor_range = range(1, 21)

avg_scores = []

for n in neighbor_range:
    knn = KNeighborsClassifier(n_neighbors=n)
    scores = cross_val_score(knn, FACES, LABELS, cv=5)  # 5-fold cross-validation
    avg_scores.append(scores.mean())

optimal_n = neighbor_range[avg_scores.index(max(avg_scores))]
print(avg_scores)
print(f"Optimal number of neighbors: {optimal_n}")

knn = KNeighborsClassifier(n_neighbors=optimal_n)
knn.fit(FACES, LABELS)
print("Training done with optimal n_neighbors")