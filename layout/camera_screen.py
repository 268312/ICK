import customtkinter as ctk
import cv2
from PIL import Image, ImageTk


class OknoKamera(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Kamera z rozpoznawaniem twarzy")
        self.geometry("700x500")

        # ramka na podgląd z kamerki i przycisk
        self.frame = ctk.CTkFrame(self)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        # label z obrazem z kamerki
        self.video_frame = ctk.CTkLabel(self.frame, text="")
        self.video_frame.pack(pady=(0, 10))  # mały odstęp poniżej obrazu

        # przycisk "zatwierdź"
        self.btn_zatwierdz = ctk.CTkButton(self.frame, text="Zatwierdź", command=self.zatwierdz)
        self.btn_zatwierdz.pack()

        # uruchom kamerę
        self.cap = cv2.VideoCapture(0)
        self.update_frame()

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.flip(frame, 1)
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            img_tk = ImageTk.PhotoImage(image=img)
            self.video_frame.configure(image=img_tk)
            self.video_frame.image = img_tk
        self.after(20, self.update_frame)

    def zatwierdz(self):
        # TODO: tu wywołanie funkcji przechwycającej twarz i tworzącej z niej wektor,
        # porównanie tego wektora z wektorem przechowywanym w bazie dla danego loginu
        print("Przycisk Zatwierdź kliknięty")  #tymczasowo
        self.cap.release()
        self.destroy()
