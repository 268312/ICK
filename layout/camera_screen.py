import encodings

import customtkinter as ctk
import cv2
from PIL import Image, ImageTk
import face_recognition
import firebase_admin
from firebase_admin import credentials, firestore

if not firebase_admin._apps:
    cred = credentials.Certificate("./serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

class OknoKamera(ctk.CTkToplevel):
    def __init__(self, master, username):
        super().__init__(master)
        self.username = username
        self.title("Kamera z rozpoznawaniem twarzy")
        self.geometry("700x500")

        # ramka na podgląd z kamerki i przycisk
        self.frame = ctk.CTkFrame(self)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        # label z obrazem z kamerki
        self.video_frame = ctk.CTkLabel(self.frame, text="")
        self.video_frame.pack(pady=(0, 10))  # mały odstęp poniżej obrazu

        # przycisk "zatwierdź"
        self.btn_zatwierdz = ctk.CTkButton(self.frame, text="Zatwierdź", command=self.save)
        self.btn_zatwierdz.pack()

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

    # Funkcja przechwytująca twarz i zapisująca go w firebase
    def save(self):
        if self.last_frame is None:
            print("Brak obrazu") #TODO
            return
        vector = self.get_feature_vector(self.last_frame)
        if vector is None:
            print("Nie udasło się wyegenrować wektora cech") #TODO
        else:
            self.save_embedding(self.username, vector)
        self.cap.release()
        self.destroy()

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

    # zapisanie embedding do firebase
    def save_embedding(self, username, embedding):
        user_ref = db.collection("users").document(username)
        user_ref.set({
            "login": username,
            "embedding": embedding
        })