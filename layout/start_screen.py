import customtkinter as ctk

class StartScreen(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        # main container
        container = ctk.CTkFrame(
            self,
            corner_radius=20
        )
        container.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            container,
            text="Witaj!",
            font=("Arial", 28, "bold")
        ).pack(padx=382, pady=(50, 30))

        ctk.CTkLabel(
            container,
            text="Zaloguj się przy użyciu rozpoznawania twarzy",
            font=("Arial", 14),
            text_color="gray"
        ).pack(pady=(0, 30))

        ctk.CTkButton(
            container,
            text="Zaloguj się",
            width=220,
            height=44,
            corner_radius=12,
            command=lambda: (
                self.app.frames["CameraScreen"].set_mode("login"),
                self.app.show_frame("CameraScreen")
            )
        ).pack(pady=(0,15))

        ctk.CTkButton(
            container,
            text="Zarejestruj się",
            width=220,
            height=44,
            corner_radius=12,
            fg_color="gray25",
            hover_color="gray35",
            command=lambda: app.show_frame("RegisterScreen")
        ).pack(pady=(0, 30))