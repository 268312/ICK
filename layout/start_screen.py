import customtkinter as ctk

from layout.login_screen import OknoLogowania

# ustawienia wygladu
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# glowne okno
app = ctk.CTk()
app.title("Panel logowania")
app.geometry("400x300")

# tytul
label = ctk.CTkLabel(app, text="Witaj w aplikacji!", font=("Arial", 20, "bold"))
label.pack(pady=40)

# obsluga przyciskow
def otworz_okno_logowania():
    app.withdraw()  # ukryj główne okno
    OknoLogowania(app)

def zarejestruj_sie():
    print("Kliknięto: Zarejestruj się")

# przyciski
btn_login = ctk.CTkButton(app, text="Zaloguj się", command=otworz_okno_logowania)
btn_login.pack(pady=10)

btn_register = ctk.CTkButton(app, text="Zarejestruj się", command=zarejestruj_sie, fg_color="gray", hover_color="darkgray")
btn_register.pack(pady=10)


app.mainloop()