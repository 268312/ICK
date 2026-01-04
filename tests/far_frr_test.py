import numpy as np
import os

"""
Test lets iterate over multiple thresholds, measures how often:
- users are falsely accepted (FAR)
- users are falsely rejected (FRR)

0.7 - very tolerant 
0.6 - default
0.5 - strict
0.4 - very scrict
"""

registered_root = "test_data/registered"
unregistered_root = "test_data/unregistered"

def load_embeddings(root):
    data = {}
    for person in os.listdir(root):
        person_dir = os.path.join(root, person)
        if not os.path.isdir(person_dir):
            continue
        data[person] = [
            np.load(os.path.join(person_dir, f), allow_pickle=True).astype(np.float32)
            for f in os.listdir(person_dir)
            if f.endswith(".npy")
        ]
    return data

registered = load_embeddings(registered_root)
unregistered = load_embeddings(unregistered_root)

registered_all = [e for v in registered.values() for e in v]
unregistered_all = [e for v in unregistered.values() for e in v]

thresholds = [0.7, 0.6, 0.5, 0.4]  # 70%, 80%, 90%, 95% approximation

def match(vec, others, threshold):
    return any(np.linalg.norm(vec - other) < threshold for other in others)

for thresh in thresholds:
    # FAR: unregistered accepted as registered
    false_accepts = sum(
        match(vec, registered_all, thresh)
        for vec in unregistered_all
    )
    far = false_accepts / len(unregistered_all)

    # FRR: registered rejected (no match with same person)
    false_rejects = 0
    total = 0
    for person, embeds in registered.items():
        for vec in embeds:
            total += 1
            other_embeds = [e for e in embeds if not np.array_equal(e, vec)]
            if not match(vec, other_embeds, thresh):
                false_rejects += 1

    frr = false_rejects / total

    print(f"Threshold = {thresh:.2f}, FAR: {far:.2%}, FRR: {frr:.2%}")