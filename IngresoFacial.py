from tkinter import Toplevel, Label
from PIL import ImageTk, Image
import cv2

def mostrar_ventana_acceso(pantalla):
    ventana_acceso = Toplevel(pantalla)
    ventana_acceso.title("Acceso Concedido")
    ventana_acceso.geometry("400x200")
    ventana_acceso.configure(bg="#d0f0c0")
    Label(ventana_acceso, text="✅ Acceso Permitido", font=("Arial", 18, "bold"), bg="#d0f0c0", fg="green").pack(pady=40)

def abrir_reconocimiento_para_ingreso(pantalla):
    ventana_facial = Toplevel(pantalla)
    ventana_facial.title("Verificación Facial - Ingreso")
    ventana_facial.geometry("800x500")

    label_video = Label(ventana_facial)
    label_video.pack()

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)

    rostro_detectado = [False]

    def actualizar_frame():
        ret, frame = cap.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            if len(faces) > 0 and not rostro_detectado[0]:
                rostro_detectado[0] = True
                ventana_facial.after(500, lambda: mostrar_ventana_acceso(pantalla))
                ventana_facial.after(1000, ventana_facial.destroy)
                cap.release()
                return

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            imgtk = ImageTk.PhotoImage(image=img)
            label_video.imgtk = imgtk
            label_video.configure(image=imgtk)

        label_video.after(50, actualizar_frame)

    actualizar_frame()

    def cerrar():
        cap.release()
        ventana_facial.destroy()

    ventana_facial.protocol("WM_DELETE_WINDOW", cerrar)
