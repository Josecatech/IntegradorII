from tkinter import *
from tkinter import font as tkfont


class UniformMessageBox(Toplevel):
    def __init__(self, parent, title, message, message_type="success"):
        super().__init__(parent)
        self.title(title)
        self.geometry("400x220")  # Tamaño unificado
        self.resizable(False, False)
        self.overrideredirect(True)
        # colores según el tipo
        color_config = {
            "success": {
                "bg": "#4CAF50",  # Verde
                "button_bg": "#388E3C",  # Verde oscuro
                "separator": "#81C784"  # Verde claro
            },
            "error": {
                "bg": "#F44336",  # Rojo
                "button_bg": "#D32F2F",  # Rojo oscuro
                "separator": "#EF9A9A"  # Rojo claro
            }
        }
        colors = color_config.get(message_type, color_config["success"])

        self.configure(bg=colors["bg"])

        # Frame principal
        main_frame = Frame(self, bg=colors["bg"])
        main_frame.pack(fill=BOTH, expand=True, padx=25, pady=45)



        # Mensaje principal (Texto normal)
        message_font = tkfont.Font(family="Arial", size=12)
        message_label = Label(main_frame, text=message,
                              font=message_font,
                              bg=colors["bg"], fg="white",
                              wraplength=350)
        message_label.pack(pady=15)

        # Botón "Aceptar" (centrado)
        button_frame = Frame(main_frame, bg=colors["bg"])
        button_frame.pack(pady=(27, 0))

        self.ok_button = Button(button_frame, text="  Aceptar  ",
                                font=("Arial", 11, "bold"),
                                bg=colors["button_bg"],
                                fg="white",
                                activebackground=colors["button_bg"],
                                activeforeground="white",
                                relief=FLAT,
                                borderwidth=0,
                                padx=25,
                                pady=6,
                                command=self.destroy)
        self.ok_button.pack()

        # Efecto hover (ligero cambio de tonalidad)
        self.ok_button.bind("<Enter>", lambda e: self.ok_button.config(
            bg="#0D7037" if message_type == "success" else "#A4291C"))
        self.ok_button.bind("<Leave>", lambda e: self.ok_button.config(
            bg=colors["button_bg"]))

        # Centrado y comportamiento modal
        self.center_window()
        self.grab_set()
        self.focus_set()

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")


def show_uniform_message(parent, title, message, message_type="success"):
    msg = UniformMessageBox(parent, title, message, message_type)
    parent.wait_window(msg)
