
import customtkinter as ctk

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("1280x720")
app.title("RLBot League Runner")

app.iconbitmap("assets/icon.ico")

label = ctk.CTkLabel(app, text="Welcome to My App", font=("Helvetica", 24), compound="left")
label.pack(pady=20)

app.mainloop()
