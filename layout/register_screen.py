import customtkinter as ctk

from layout.camera_screen import OknoKamera


class OknoRejestracji(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Rejestracja z rozpoznawaniem twarzy")
        self.geometry("700x500")

        # do wyśrodkowania
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        frame = ctk.CTkFrame(self)
        frame.grid(row=0, column=0)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        self.label = ctk.CTkLabel(frame, text="Wprowadź login:", font=("Arial", 16))
        self.label.pack(pady=(0, 5))

        self.entry_login = ctk.CTkEntry(frame, width=200, placeholder_text="Twój login")
        self.entry_login.pack(pady=(0, 10))

        self.btn_przejdzdalej = ctk.CTkButton(frame, text="Przejdź dalej", command=self.przejdz_dalej)
        self.btn_przejdzdalej.pack()

    def przejdz_dalej(self):
        username = self.entry_login.get().strip()
        if username == "":
            print("Login nie może być pusty") #TODO
            return

        self.withdraw()
        OknoKamera(self, mode="register", username=username)

