import customtkinter as ctk

class RegisterScreen(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        # main container
        container = ctk.CTkFrame(
            self,
            corner_radius=20
        )
        container.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkButton(
            container,
            text="← Powrót",
            fg_color="transparent",
            hover_color="gray20",
            width=80,
            command=lambda: app.show_frame("StartScreen")
        ).place(x=20, y=20)

        content = ctk.CTkFrame(container, fg_color="transparent")
        content.pack(padx=300, pady=(50, 30))

        ctk.CTkLabel(
            content,
            text="Rejestracja",
            font=("Arial", 28, "bold")
        ).pack(pady=(0, 10))

        ctk.CTkLabel(content, text="Wprowadź nazwę użytkownika", font=("Arial", 14), text_color="gray").pack(pady=(0, 20))
        self.entry_login = ctk.CTkEntry(
            content,
            width=240,
            height=36,
            placeholder_text="Twój login"
        )
        self.entry_login.pack(pady=(0, 5))

        self.error_label = ctk.CTkLabel(
            content,
            text="",
            text_color="red",
            font=("Arial", 12)
        )
        self.error_label.pack(pady=(5, 15))

        self.next_button = ctk.CTkButton(
            content,
            text="Przejdź dalej",
            width=220,
            height=44,
            corner_radius=12,
            command=self.next,
            state="disabled"
        )
        self.next_button.pack()

    def next(self):
        username = self.entry_login.get().strip()
        self.error_label.configure(text="")
        if not username:
            self.error_label.configure(
                text="Login nie może być pusty"
            )
            return

        camera = self.app.frames["CameraScreen"]
        if not camera.set_mode("register", username):
            self.error_label.configure(
                text="Użytkownik o takiej nazwie już istnieje"
            )
            return
        self.app.show_frame("CameraScreen")

    def on_show(self):
        self.entry_login.delete(0, "end")
        self.error_label.configure(text="")
        self.next_button.configure(state="disabled")
        self.entry_login.focus_set()
        self.entry_login.bind("<Return>", lambda e: self.next())
        self.entry_login.bind("<KeyRelease>", self.validate_input)

    def validate_input(self, event=None):
        text = self.entry_login.get().strip()
        if text:
            self.next_button.configure(state="normal")
        else:
            self.next_button.configure(state="disabled")