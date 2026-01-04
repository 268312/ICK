import os
import time
import numpy as np
from layout.camera_screen import get_feature_vector
from PIL import Image


"""
Test checks if average recognition time is smaller than 2 seconds. 
"""
# Simulate frames captured from camera
timing_folder = "test_data/timing"

image_files = [
    os.path.join(timing_folder, f)
    for f in os.listdir(timing_folder)
    if f.endswith((".jpg", ".png"))
]

times = []
for img_path in image_files:
    # Load image and convert to BGR for OpenCV
    img = np.array(Image.open(img_path).convert("RGB"))[..., ::-1]

    start = time.time()
    vec = get_feature_vector(img)
    end = time.time()

    times.append(end - start)

avg_time = sum(times) / len(times)
print(f"Average recognition time: {avg_time:.3f}s")

if avg_time <= 2.0:
    print("Time is within acceptable limit (<2s)")
else:
    print("⚠ Recognition too slow")