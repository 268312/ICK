import numpy as np
import os

from layout.camera_utils import embedding_already_registered

"""
Test measures accuracy for different face orientations. 
"""

angles = ["straight", "tilt_right", "tilt_left", "from_below", "from_above"]
thresholds = [0.7, 0.6, 0.5, 0.4]

for thresh in thresholds:
    print(f"\n--- Threshold = {thresh} ---")
    for angle in angles:
        angle_dir = os.path.join("test_data/angles", angle)
        false_rejects = 0
        total_samples = 0

        for i in range(5):  # sample_0 to sample_4
            sample_folder = os.path.join(angle_dir, f"sample_{i}")
            for file in os.listdir(sample_folder):
                if file.endswith(".npy"):
                    embedding = np.load(os.path.join(sample_folder, file), allow_pickle=True).astype(np.float32)
                    total_samples += 1
                    if not embedding_already_registered(embedding, threshold=thresh):
                        false_rejects += 1

        frr = false_rejects / total_samples if total_samples else 0
        print(f"Angle: {angle}, FRR: {frr:.2%}")