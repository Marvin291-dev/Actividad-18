import tkinter as tk
from tkinter import messagebox
import os

class Bandas:
    def __init__(self):
        self.concurso = Concurso()
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
                banda = BandaEscolares(nombre.get(), institucion.get(), categoria.get())
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

        listado = self.concurso.listarbandas()
        for infor in listado:
            tk.Label(ventana, text = infor, justify = "left").pack(anchor = "w")

    def mostrarranking(self):
        ventana = tk.Toplevel(self.ventana_principal)
        ventana.title("Ranking puntajes")
        ventana.geometry("400x300")

        ranking = self.concurso.ranking()
        tk.Label(ventana, text = f"Ranking de Bandas", font = ("Arial", 12, "bold")).pack(pady = 20)
        for i, banda in enumerate(ranking, start = 1):
            tk.Label(ventana, text = f" {i}. {banda.mostrarinformacion()},", justify = "left").pack(anchor = "w")

class BandaEscolares:
    def __init__(self, nombre, institucion, categoria):
        self.nombre = nombre
        self.institucion = institucion
        self.categoria = categoria
        self.puntajes = {}

    def registrarpuntajes(self, puntajes):
        criterios_validos = ["ritmo", "uniformidad", "coreografía", "alineación", "puntualidad"]
        if set(puntajes.keys()) != set(criterios_validos):
            raise ValueError("Criterios incompletos o incorrectos")
        for criterio, valor in puntajes.items():
            if not isinstance(valor, (int, float)) or not (0 <= valor <= 10):
                raise ValueError(f"Puntajes fuera de rango en {criterio}")
        self.puntajes = puntajes

    def get_total(self):
        return sum(self.puntajes.values()) if self.puntajes else 0

    def get_promedio(self):
        return self.get_total() / len(self.puntajes) if self.puntajes else 0

    def mostrarinformacion(self):
        info = f"Banda: {self.nombre} | Institucion: {self.institucion} | Categoria: {self.categoria}"
        if self.puntajes:
            info += f" | Total: {self.get_total()}"
        return info

class Concurso:
    def __init__(self):
        self.bandas = {}
        self.archivos = "bandas.txt"
        self.cargardesdearchivo()

    def inscribirbanda(self, banda):
        if banda.nombre in self.bandas:
            raise ValueError("Ya existe una banda con ese nombre")
        self.bandas[banda.nombre] = banda
        self.guardarenarchivos()

    def registrarevaluacion(self, nombrebanda, puntajes):
        if nombrebanda not in self.bandas:
            raise ValueError("Ya no existe una banda con ese nombre")
        self.bandas[nombrebanda].registrarpuntajes(puntajes)
        self.guardarenarchivos()

    def listarbandas(self):
        return [b.mostrarinformacion() for b in self.bandas.values()]

    def ranking(self):
        evaluaciones = [b for b in self.bandas.values() if b.puntajes]
        return sorted(evaluaciones, key = lambda b: (b.get_total(), b.get_promedio), reverse = True)

    def guardarenarchivos(self):
        with open(self.archivos, "w", encoding = "utf-8") as archivo:
            for banda in self.bandas.values():
                linea = f"{banda.nombre} | {banda.institucion} | {banda.categoria}"
                if banda.puntajes:
                    puntajes_str = ",".join(f"{k} : {v}" for k, v in banda.puntajes.items())
                    linea += f" | {puntajes_str}"
                archivo.write(linea + "\n")

    def cargardesdearchivo(self):
        if not os.path.exists(self.archivos):
            return
        with open(self.archivos, "r", encoding = "utf-8") as archivo:
            for linea in archivo:
                partes = linea.strip().split("|")
                if len(partes) >= 3:
                    banda = BandaEscolares(partes[0], partes[1],partes[2])
                    if len(partes) == 4:
                        puntajes = {}
                        for par in partes[3].split(","):
                            crit, valor = par.split(":")
                            puntajes[crit] = int(valor)
                        banda.registrarpuntajes(puntajes)
                    self.bandas[banda.nombre] = banda

if __name__ == "__main__":
    Bandas()