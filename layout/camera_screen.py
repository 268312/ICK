import customtkinter as ctk
from tkinter import messagebox as mbox
import cv2
from PIL import Image, ImageTk
import face_recognition
import firebase_admin
from firebase_admin import credentials, firestore

from layout.camera_utils import user_already_exists, get_feature_vector, find_user, make_circle, \
    embedding_already_registered
from tests.test_data import import_embeddings

if not firebase_admin._apps:
    cred = credentials.Certificate("layout/serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

class CameraScreen(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.mode = "login"
        self.username = None
        self.scan_angle = 0

        self.cap = None
        self.last_frame = None
        self.running = False

        # --- Frame skipping ---
        self.frame_counter = 0
        self.faces_detected = []

        self.container = ctk.CTkFrame(self, corner_radius=20)
        self.container.pack(fill="both", expand=True, padx=40, pady=40)

        self.content = ctk.CTkFrame(self.container, fg_color="transparent")
        self.content.pack(fill="both", expand=True, padx=20, pady=20)

        self.back_btn = ctk.CTkButton(
            self.content,
            text="← Powrót",
            fg_color="transparent",
            hover_color="gray20",
            corner_radius=20,
            width=80,
            command=lambda: app.show_frame("StartScreen")
        )
        self.back_btn.pack(anchor="nw", padx=10, pady=10)

        self.hint_label = ctk.CTkLabel(self.content, text="", font=("Arial", 24, "bold"))
        self.hint_label.pack()

        self.video_frame = ctk.CTkLabel(self.content, text="", height=600)
        self.video_frame.pack(fill="x")

        self.btn_action = ctk.CTkButton(
            self.content,
            text="Zaloguj",
            width=220,
            height=44,
            corner_radius=12,
            command=self.login
        )
        self.btn_action.pack(pady=(0, 10))

    def on_show(self):
        """Called automatically when frame is shown"""
        if not self.cap:
            self.cap = cv2.VideoCapture(0)
            self.running = True
            self.update_frame()

    def on_hide(self):
        """Called manually before leaving the screen"""
        self.running = False
        if self.cap:
            self.cap.release()
            self.cap = None

    def set_mode(self, mode, username=None):
        """
        mode: 'login' | 'register'
        Returns True if mode was set, False if blocked
        """
        self.mode = mode
        self.username = username

        if mode == "register" and user_already_exists(username):
            return False

        if mode == "register":
            self.btn_action.configure(
                text="Zatwierdź",
                command=self.save
            )
        else:
            self.btn_action.configure(
                text="Zaloguj",
                command=self.login
            )
        return True

    def update_frame(self):
        if not self.running or not self.cap:
            return

        ret, frame = self.cap.read()
        if not ret:
            self.after(20, self.update_frame)
            return

        frame = cv2.flip(frame, 1)
        self.last_frame = frame.copy()

        w = self.video_frame.winfo_width()
        h = self.video_frame.winfo_height()
        if w > 1 and h > 1:
            fh, fw = frame.shape[:2]
            scale = min(w / fw, h / fh) * 0.7
            frame = cv2.resize(frame, (int(fw * scale), int(fh * scale)))

        self.frame_counter += 1
        if self.frame_counter % 10 == 0:  # detect every 5th frame
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            self.faces_detected = face_recognition.face_locations(cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB))

        if len(self.faces_detected) == 0:
            self.hint_label.configure(text="Nie wykryto twarzy. Umieść twarz w kółku", text_color="gray")
        else:
            self.hint_label.configure(text="Twarz wykryta. Nie ruszaj się", text_color="green")

        img = Image.fromarray(frame[..., ::-1])  # BGR -> RGB
        img = make_circle(img)
        img_tk = ImageTk.PhotoImage(img)

        self.video_frame.configure(image=img_tk)
        self.video_frame.image = img_tk

        self.after(20, self.update_frame)

    # *******************************************************
    # FUNKCJE REJESTRACJI
    # *******************************************************

    def save(self):
        """
        Functions creating and saving the embedding in firebase, along with username.
        Also checks if the face or username are already registered.
        """
        if self.last_frame is None:
            mbox.showerror("Błąd", "Nie wykryto obrazu. Spróbuj ponownie")
            return

        vector = get_feature_vector(self.last_frame)
        img = Image.fromarray(cv2.cvtColor(self.last_frame, cv2.COLOR_BGR2RGB))
        import_embeddings.save_angle_embedding(vector, img, "from_above", 0)
        if vector is None:
            return

        if embedding_already_registered(vector):
            mbox.showerror("Błąd", "Użytkownik o takiej twarzy istnieje już w systemie")
            self.app.show_frame("StartScreen")
            return

        db.collection("users").document(self.username).set({
            "login": self.username,
            "embedding": vector
        })

        mbox.showinfo("Rejestracja", "Zarejestrowano pomyślnie")
        self.on_hide()
        self.app.show_frame("StartScreen")

    #************************************************
    # FUNKCJE LOGOWANIA
    #************************************************
    def login(self):
        if self.last_frame is None:
            mbox.showerror("Błąd", "Nie wykryto obrazu. Spróbuj ponownie")
            return

        vector = get_feature_vector(self.last_frame)
        if vector is None:
            return

        match = find_user(vector)
        if match:
            self.on_hide()
            logged = self.app.frames["LoggedInScreen"]
            logged.set_user(match["user"])
            self.app.show_frame("LoggedInScreen")
        else:
            mbox.showerror("Błąd", "Nie wykryto twarzy. Spróbuj ponownie")