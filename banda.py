import tkinter as tk
from tkinter import messagebox


class Bandas:
    def __init__(self):
        #self.concurso = Concurso()
        self.ventana_principal = tk.Tk()
        self.ventana_principal.title("Concurso de Bandas - Quetzaltenango")
        self.ventana_principal.geometry("500x300")

        tk.Label(
            self.ventana_principal,
            text = "Sistema de Inscripción y Evaluación de Bandas Escolares\nConcurso 14 de Septiembre - Quetzaltenango",
            font = ("Arial", 12),
            justify = "center",
        ).pack(pady = 20)
        opciones = ["Inscribir Banda", "Registrar Puntajes", "Listar Bandas", "Ver Ranking"]
        self.opcion = tk.StringVar()
        self.opcion.set(opciones[0])
        tk.OptionMenu(self.ventana_principal, self.opcion, *opciones).pack(pady = 20)

        tk.Button(self.ventana_principal, text = "Aceptar", command = self.ejecutaropcion, bg = "blue", fg = "white").pack(pady = 20)

        self.ventana_principal.mainloop()

    def ejecutaropcion(self):
        opcciones_bandas = self.opcion.get()
        if opcciones_bandas == "Inscribir Banda":
            self.formularioinscripcion()
        elif opcciones_bandas == "Registrar Puntajes":
            self.evaluacion()
        elif opcciones_bandas == "Listar Bandas":
            self.mostrarlistado()
        elif opcciones_bandas == "Ver Ranking":
            self.mostrarranking()

    def formularioinscripcion(self):
        ventana = tk.Toplevel(self.ventana_principal)
        ventana.title("Inscripcion de Bandas")
        ventana.geometry("400x300")

        tk.Label(ventana, text = "Nombre de la Banda: ").pack()
        nombre = tk.Entry(ventana)
        nombre.pack()

        tk.Label(ventana, text = "Institucion: ").pack()
        institucion = tk.Entry(ventana)
        institucion.pack()

        tk.Label(ventana, text = "Categoría: ").pack()
        categoria = tk.StringVar(ventana)
        categoria.set("Primaria")
        tk.OptionMenu(ventana, categoria, "Primaria", "Basico ", "Diversificado").pack()

        def guardar():
            try:
                banda = Bandaescolar(nombre.get(), institucion.get())
                banda.set_categoria(categoria.get())
                self.concurso.inscribirbanda(banda)
                messagebox.showinfo("Exito", "Banda Inscribibida correctamente")
                ventana.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(ventana, text = "Guardar", command = guardar, bg = "green", fg = "white").pack(pady = 20)

    def evaluacion(self):
        ventana = tk.Toplevel(self.ventana_principal)
        ventana.title("Registrar puntajes")
        ventana.geometry("400x300")

        tk.Label(ventana, text = "Nombre de la banda: ").pack()
        nombre = tk.Entry(ventana)
        nombre.pack()

        criterios = ["ritmo", "Uniformidad", "Coreografía", "Alineación", "Puntualidad"]
        entredas = {}

        for criterio in criterios:
            tk.Label(ventana, text = f"{criterio.capitalize()}: ").pack()
            entrada = tk.Entry(ventana)
            entrada.pack()
            entredas[criterio] = entrada

        def guardar():
            try:
                puntajes = {c: int(e.get()) for c, e in entredas.items()}
                self.concurso.registrarevaluacion(nombre.get(), puntajes)
                messagebox.showinfo("Exito", "Puntajes registrada correctamente")
                ventana.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(ventana, text = "Guardar", command= guardar, bg = "green", fg = "white").pack(pady = 20)

    def mostrarlistado(self):
        ventana = tk.Toplevel(self.ventana_principal)
        ventana.title("Listar puntajes")
        ventana.geometry("400x300")

if __name__ == "__main__":
    Bandas()