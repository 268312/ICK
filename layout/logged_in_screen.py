import customtkinter as ctk


class LoggedInScreen(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.username = None

        self.container = ctk.CTkFrame(self, corner_radius=20)
        self.container.pack(fill="both", expand=True, padx=40, pady=40)

        self.content = ctk.CTkFrame(self.container, fg_color="transparent")
        self.content.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkButton(
            self.content,
            text="← Wyloguj",
            fg_color="transparent",
            hover_color="gray20",
            corner_radius=20,
            width=80,
            command=lambda: app.show_frame("StartScreen")
        ).place(anchor="nw",x=10, y=10)

        self.label = ctk.CTkLabel(self.content, text="", font=("Arial", 24, "bold"))
        self.label.pack(expand=True)

    def on_show(self):
        if self.username:
            self.label.configure(text=f"Witaj, {self.username}!")
        else:
            self.label.configure(text="Zalogowano pomyślnie!")

    def set_user(self, username):
        self.username = username
        self.label.configure(text=f"Witaj, {username}!")