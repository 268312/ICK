import os

import numpy as np

from layout.camera_utils import embedding_already_registered

"""
Tests registered users under different lighting, records FRR.
"""
lighting_conditions = ["bright", "artificial", "dim", "shadow"]
thresholds = [0.7, 0.6, 0.5, 0.4]

for thresh in thresholds:
    print(f"\n--- Threshold = {thresh} ---")
    for cond in lighting_conditions:
        cond_dir = os.path.join("test_data/lighting", cond)
        false_rejects = 0
        total_samples = 0

        for i in range(5):  # sample_0 to sample_4
            sample_folder = os.path.join(cond_dir, f"sample_{i}")
            for file in os.listdir(sample_folder):
                if file.endswith(".npy"):
                    embedding = np.load(os.path.join(sample_folder, file), allow_pickle=True).astype(np.float32)
                    total_samples += 1
                    if not embedding_already_registered(embedding, threshold=thresh):
                        false_rejects += 1

        frr = false_rejects / total_samples if total_samples else 0
        print(f"Lighting: {cond}, FRR: {frr:.2%}")