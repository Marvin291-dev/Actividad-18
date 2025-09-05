import tkinter as tk

class

class Bandas:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Banda en Quetzaltenango")
        self.ventana.geometry("500x350")

        self.menu()

        tk.Label(
            self.ventana,
            text = "Organizacion de bandas para el concurso del\ndesfile del 14 de septiembre",
            font = ("Arial", 15, "bold"),
            justify = "center",
        ).pack(pady = 50)

        self.ventana.mainloop()

    def menu(self):
        barra = tk.Menu(self.ventana)
        opcion = tk.Menu(barra, tearoff=0)
        opcion.add_command(label = "Inscribir bandas por categoría", command = self.inscribirporcategoria)
        opcion.add_command(label = "Registrar puntajes por criterios", command = self.Registrarpuntajesporcriterios)
        opcion.add_command(label = "Listar bandas inscritas", command = self.Listarbandasinscritas)
        opcion.add_command(label = "Generar un ranking final", command = self.Generarunrankingfinal)
        opcion.add_separator()
        opcion.add_command(label = "Salir", command = self.ventana.quit)
        barra.add_cascade(label = "Opción", menu = opcion)
        self.ventana.config(menu = barra)

    def inscribirporcategoria(self):
        print("Inscribiendo bandas por criterios")
        tk.Toplevel(self.ventana).title("Inscribiendo bandas por criterios")

    def Registrarpuntajesporcriterios(self):
        print("Registrando puntajes por criterios")

    def Listarbandasinscritas(self):
        print("Listando bandas inscritas")

    def Generarunrankingfinal(self):
        print("Generando ranking final")

if __name__ == "__main__":
    banda = Bandas()
