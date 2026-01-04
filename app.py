import customtkinter as ctk

from layout.start_screen import StartScreen
from layout.register_screen import RegisterScreen
from layout.camera_screen import CameraScreen
from layout.logged_in_screen import LoggedInScreen

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Panel logowania")
        self.wm_attributes('-fullscreen', True)
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)

        self.frames = {}

        for Screen in (
            StartScreen,
            RegisterScreen,
            CameraScreen,
            LoggedInScreen,
        ):
            frame = Screen(self.container, self)
            self.frames[Screen.__name__] = frame
            frame.place(relwidth=1, relheight=1)

        self.show_frame("StartScreen")

    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()
        if hasattr(frame, "on_show"):
            frame.on_show()

if __name__ == "__main__":
    app = App()
    app.mainloop()