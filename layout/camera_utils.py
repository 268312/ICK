from tkinter import messagebox as mbox
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from layout.firebase_service import get_db

def find_user(vector, threshold=0.6):
    """
    Function to find the best matched user to the current embedding vector. The higher the threshold - the more
     'ignorant' the recognition is. 0.6 - general match, 0.4 - strong match, 0.3 - duplicate embedding
     @:param vector
     @:param threshold default 0.6
     @returns dictionary
    """
    import face_recognition

    db = get_db()
    users_ref = db.collection("users")
    docs = users_ref.stream()

    best_match = None
    best_distance = float("inf")

    for doc in docs:
        user = doc.to_dict()
        stored = user.get("embedding")
        if not stored:
            continue

        known = np.array(stored)
        unknown = np.array(vector)

        distance = face_recognition.face_distance([known], unknown)[0]
        if distance < best_distance:
            best_distance = distance
            best_match = {
                "user": doc.id,
                "distance": distance
            }

    if best_match and best_match["distance"] < threshold:
        return best_match

    return None

def embedding_already_registered(vector, threshold=0.6):
    """
    Function checking if vector taken during registration is already registered (checks all usernames).
    @:param vector
    @param username
    @param threshold default 0.6
    @return boolean
    """
    import face_recognition

    db= get_db()
    user_ref = db.collection("users")
    docs = user_ref.stream()
    unknown_embedding = np.array(vector)

    for doc in docs:
        user = doc.to_dict()
        stored = user.get("embedding")
        if stored is None:
            continue
        known_embedding = np.array(stored)

        distance = face_recognition.face_distance([known_embedding], unknown_embedding)[0]
        # print(distance)
        if distance < threshold:
            return True
    return False

def make_circle(image: Image.Image) -> Image.Image:
    """
    Creates a circular face scan overlay with a fading rotating arc.
    :param image: PIL.Image frame
    :param border: thickness of outer circle
    :param scan_angle: current angle of scanning arc (degrees)
    :param segments: number of fading segments for tail
    """
    size = min(image.size)
    image = image.crop((
        (image.width - size) // 2,
        (image.height - size) // 2,
        (image.width + size) // 2,
        (image.height + size) // 2,
    ))

    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size, size), fill=255)
    image.putalpha(mask)

    # Optional soft glow
    glow = image.filter(ImageFilter.GaussianBlur(radius=4))
    image = Image.alpha_composite(glow, image.convert("RGBA"))

    return image

def user_already_exists(username):
    """
    Function to check if username already exists during registration.
    @param username
    @return boolean
    """
    db = get_db()
    doc = db.collection("users").document(username).get()
    return doc.exists

def compare_faces(known_vector, unknown_vector):
    """
    Function returning whether face embeddings are the same.
    @:param known_vector
    @:param unknown_vector
    @returns boolean
    """
    import face_recognition

    results = face_recognition.compare_faces([known_vector], unknown_vector)
    return results[0]

def get_feature_vector(frame):
    """
    Generates the face feature vector from a frame.
    :param frame: BGR frame from OpenCV
    :return: feature vector list or None
    """
    import cv2
    import face_recognition

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    locations = face_recognition.face_locations(rgb)

    if not locations:
        mbox.showerror("Błąd", "Nie wykryto twarzy. Spróbuj ponownie")
        return None

    encodings = face_recognition.face_encodings(rgb, locations)
    if not encodings:
        mbox.showerror("Błąd", "Nie udało się pobrać cech twarzy. Spróbuj ponownie")
        return None
    print(encodings[0].tolist())
    return encodings[0].tolist()