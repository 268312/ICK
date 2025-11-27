import customtkinter as ctk

from layout.camera_screen import OknoKamera


class OknoLogowania(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Logowanie z rozpoznawaniem twarzy")
        self.geometry("700x500")

        # do wyśrodkowania
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        frame = ctk.CTkFrame(self)
        frame.grid(row=0, column=0)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        self.withdraw()
        OknoKamera(self, mode="login")
