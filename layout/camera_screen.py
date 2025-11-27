import customtkinter as ctk
import cv2
from PIL import Image, ImageTk
import face_recognition
import firebase_admin
from firebase_admin import credentials, firestore
import numpy as np

if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

class OknoKamera(ctk.CTkToplevel):
    def __init__(self, master, mode="register", username=None):
        """
        mode: "register" lub "login"
        username: przy logowaniu trzeba podać login
        """
        super().__init__(master)
        self.mode = mode
        self.username = username
        self.title("Kamera z rozpoznawaniem twarzy")
        self.geometry("700x500")

        # ramka na podgląd z kamerki i przycisk
        self.frame = ctk.CTkFrame(self)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        # label z obrazem z kamerki
        self.video_frame = ctk.CTkLabel(self.frame, text="")
        self.video_frame.pack(pady=(0, 10))  # mały odstęp poniżej obrazu

        # przycisk "zatwierdź" dla rejestracji i zaloguj dla logowania
        if self.mode == "register":
            self.btn_action = ctk.CTkButton(self.frame, text="Zatwierdź", command=self.save)
        else:
            self.btn_action = ctk.CTkButton(self.frame, text="Zaloguj", command=self.login)

        self.btn_action.pack()

        # uruchom kamerę
        self.cap = cv2.VideoCapture(0)
        self.last_frame = None
        self.update_frame()

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.flip(frame, 1)
            frame = cv2.resize(frame, (400, 300))
            self.last_frame = frame.copy()

            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            img_tk = ImageTk.PhotoImage(image=img)

            self.video_frame.configure(image=img_tk)
            self.video_frame.image = img_tk
        self.after(20, self.update_frame)




    # *******************************************************
    # FUNKCJE REJESTRACJI
    # *******************************************************

    # Funkcja przechwytująca twarz i zapisująca go w firebase
    def save(self):
        if self.last_frame is None:
            print("Brak obrazu") #TODO
            return
        vector = self.get_feature_vector(self.last_frame)
        if vector is None:
            print("Nie udało się wygenerować wektora cech") #TODO
        else:
            self.save_embedding(self.username, vector)
        self.cap.release()
        self.destroy()

        # zapisanie embedding do firebase
    def save_embedding(self, username, embedding):
        user_ref = db.collection("users").document(username)
        user_ref.set({
            "login": username,
            "embedding": embedding
        })

    #************************************************
    #FUNKCJE LOGOWANIA
    #************************************************

    def login(self):
        if self.last_frame is None:
            print("Brak obrazu")
            return

        vector = self.get_feature_vector(self.last_frame)
        if vector is None:
            print("Nie wykryto twarzy")
            return

        match = self.find_user(vector)
        if match:
            print(f"Zalogowano użytkownika: {match['userID']}, {match['distance']}")
        else:
            print("Nieprawidłowa twarz dla podanego loginu")

    # Function to find the best matched user to the current embedding vector
    def find_user(self, vector, threshold=0.6):
        users_ref = db.collection("users")
        docs = users_ref.stream()

        best_match = None
        best_distance = 1e9

        for doc in docs:
            user = doc.to_dict()
            stored_embedding = user["embedding"]
            if stored_embedding is None:
                continue

            known = np.array(stored_embedding)
            unknown = np.array(vector)
            distance = face_recognition.face_distance([known], unknown)[0] # finds best match through distance
            if distance < best_distance:
                best_distance = distance
                best_match = {
                    "user": doc.id,
                    "embedding": user,
                    "distance": distance,
                }

        if best_match and best_match["distance"] < threshold:
            return best_match
        return None # TODO

    # ***********************************************
    # FUNKCJE POMOCNICZE
    # ***********************************************

    # Funkcja generująca wektor cech z obrazu
    def get_feature_vector(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        locations = face_recognition.face_locations(rgb)
        if len(locations) == 0:
            print("Nie wykryto twarzy") #TODO
            return None

        encodings = face_recognition.face_encodings(rgb, locations)

        if len(encodings) == 0:
            print("Nie udało się pobrać cech twarzy") #TODO
            return None

        return encodings[0].tolist()
