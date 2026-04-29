"""
Módulo: ui/main_window.py
Descripción: Ventana principal del sistema VetCare
"""

import tkinter as tk
from tkinter import ttk, messagebox
from services.dueno_service import DuenoService
from services.mascota_service import MascotaService
from services.cita_service import CitaService


class VetCareApp:
    """Aplicación principal del sistema veterinario"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("VetCare - Sistema de Gestión Veterinaria")
        self.root.geometry("1000x600")
        
        # Servicios
        self.dueno_service = DuenoService()
        self.mascota_service = MascotaService()
        self.cita_service = CitaService()
        
        self.setup_ui()
        self.show_dashboard()
    
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        # Barra de menú
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        menu_archivo = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=menu_archivo)
        menu_archivo.add_command(label="Salir", command=self.root.quit)
        
        menu_modulos = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Módulos", menu=menu_modulos)
        menu_modulos.add_command(label="Registrar Dueño", command=self.show_registrar_dueno)
        menu_modulos.add_command(label="Registrar Mascota", command=self.show_registrar_mascota)
        menu_modulos.add_command(label="Agendar Cita", command=self.show_agendar_cita)
        
        # Frame principal
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
    
    def clear_frame(self):
        """Limpia el frame principal"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
    def show_dashboard(self):
        """Muestra el dashboard principal"""
        self.clear_frame()
        
        ttk.Label(self.main_frame, text="🐾 Bienvenido a VetCare", 
                  font=("Arial", 20, "bold")).pack(pady=20)
        
        # Próximas citas
        ttk.Label(self.main_frame, text="📅 Próximas Citas", 
                  font=("Arial", 14, "bold")).pack(pady=10)
        
        citas = self.cita_service.obtener_proximas_citas(5)
        
        if citas:
            for cita in citas:
                frame = ttk.Frame(self.main_frame, relief=tk.RIDGE, padding="5")
                frame.pack(fill=tk.X, pady=2)
                ttk.Label(frame, text=f"{cita['fecha_hora'].strftime('%d/%m/%Y %H:%M')} - "
                                      f"{cita['mascota_nombre']} con {cita['veterinario_nombre']}").pack()
        else:
            ttk.Label(self.main_frame, text="No hay citas programadas").pack()
    
    def show_registrar_dueno(self):
        """Formulario para registrar dueño"""
        self.clear_frame()
        
        ttk.Label(self.main_frame, text="📝 Registrar Nuevo Dueño", 
                  font=("Arial", 16, "bold")).pack(pady=10)
        
        frame_form = ttk.Frame(self.main_frame)
        frame_form.pack(pady=10)
        
        # Campos del formulario
        ttk.Label(frame_form, text="Nombre:*").grid(row=0, column=0, pady=5, sticky=tk.W)
        entry_nombre = ttk.Entry(frame_form, width=40)
        entry_nombre.grid(row=0, column=1, pady=5)
        
        ttk.Label(frame_form, text="Teléfono:*").grid(row=1, column=0, pady=5, sticky=tk.W)
        entry_telefono = ttk.Entry(frame_form, width=40)
        entry_telefono.grid(row=1, column=1, pady=5)
        
        ttk.Label(frame_form, text="Email:").grid(row=2, column=0, pady=5, sticky=tk.W)
        entry_email = ttk.Entry(frame_form, width=40)
        entry_email.grid(row=2, column=1, pady=5)
        
        ttk.Label(frame_form, text="Dirección:").grid(row=3, column=0, pady=5, sticky=tk.W)
        entry_direccion = ttk.Entry(frame_form, width=40)
        entry_direccion.grid(row=3, column=1, pady=5)
        
        def guardar():
            try:
                self.dueno_service.registrar_dueno(
                    entry_nombre.get(),
                    entry_telefono.get(),
                    entry_email.get(),
                    entry_direccion.get()
                )
                messagebox.showinfo("Éxito", "Dueño registrado correctamente")
                self.show_dashboard()
            except ValueError as e:
                messagebox.showerror("Error", str(e))
        
        ttk.Button(self.main_frame, text="Guardar", command=guardar).pack(pady=20)
        ttk.Button(self.main_frame, text="Volver", command=self.show_dashboard).pack()
    
    def show_registrar_mascota(self):
        """Formulario para registrar mascota"""
        self.clear_frame()
        
        ttk.Label(self.main_frame, text="🐕 Registrar Nueva Mascota", 
                  font=("Arial", 16, "bold")).pack(pady=10)
        
        # Obtener dueños
        duenos = self.dueno_service.obtener_todos()
        opciones_duenos = {f"{d.nombre} (ID: {d.id})": d.id for d in duenos}
        
        frame_form = ttk.Frame(self.main_frame)
        frame_form.pack(pady=10)
        
        ttk.Label(frame_form, text="Dueño:*").grid(row=0, column=0, pady=5, sticky=tk.W)
        combo_dueno = ttk.Combobox(frame_form, values=list(opciones_duenos.keys()), width=37)
        combo_dueno.grid(row=0, column=1, pady=5)
        
        ttk.Label(frame_form, text="Nombre:*").grid(row=1, column=0, pady=5, sticky=tk.W)
        entry_nombre = ttk.Entry(frame_form, width=40)
        entry_nombre.grid(row=1, column=1, pady=5)
        
        ttk.Label(frame_form, text="Especie:*").grid(row=2, column=0, pady=5, sticky=tk.W)
        combo_especie = ttk.Combobox(frame_form, values=['Perro', 'Gato', 'Conejo', 'Hamster', 'Ave', 'Reptil'], width=37)
        combo_especie.grid(row=2, column=1, pady=5)
        
        ttk.Label(frame_form, text="Raza:").grid(row=3, column=0, pady=5, sticky=tk.W)
        entry_raza = ttk.Entry(frame_form, width=40)
        entry_raza.grid(row=3, column=1, pady=5)
        
        ttk.Label(frame_form, text="Edad (años):").grid(row=4, column=0, pady=5, sticky=tk.W)
        entry_edad = ttk.Entry(frame_form, width=40)
        entry_edad.grid(row=4, column=1, pady=5)
        
        ttk.Label(frame_form, text="Peso (kg):").grid(row=5, column=0, pady=5, sticky=tk.W)
        entry_peso = ttk.Entry(frame_form, width=40)
        entry_peso.grid(row=5, column=1, pady=5)
        
        def guardar():
            if not combo_dueno.get():
                messagebox.showerror("Error", "Seleccione un dueño")
                return
            
            try:
                dueno_id = opciones_duenos[combo_dueno.get()]
                edad = int(entry_edad.get()) if entry_edad.get() else None
                peso = float(entry_peso.get()) if entry_peso.get() else None
                
                self.mascota_service.registrar_mascota(
                    entry_nombre.get(),
                    combo_especie.get(),
                    dueno_id,
                    entry_raza.get(),
                    edad,
                    peso
                )
                messagebox.showinfo("Éxito", "Mascota registrada correctamente")
                self.show_dashboard()
            except ValueError as e:
                messagebox.showerror("Error", str(e))
        
        ttk.Button(self.main_frame, text="Guardar", command=guardar).pack(pady=20)
        ttk.Button(self.main_frame, text="Volver", command=self.show_dashboard).pack()
    
    def show_agendar_cita(self):
        """Formulario para agendar cita"""
        self.clear_frame()
        
        ttk.Label(self.main_frame, text="📅 Agendar Nueva Cita", 
                  font=("Arial", 16, "bold")).pack(pady=10)
        
        # Obtener mascotas
        mascotas = self.mascota_service.obtener_todas()
        opciones_mascotas = {f"{m.nombre} (ID: {m.id})": m.id for m in mascotas}
        
        frame_form = ttk.Frame(self.main_frame)
        frame_form.pack(pady=10)
        
        ttk.Label(frame_form, text="Mascota:*").grid(row=0, column=0, pady=5, sticky=tk.W)
        combo_mascota = ttk.Combobox(frame_form, values=list(opciones_mascotas.keys()), width=37)
        combo_mascota.grid(row=0, column=1, pady=5)
        
        ttk.Label(frame_form, text="Fecha (YYYY-MM-DD):*").grid(row=1, column=0, pady=5, sticky=tk.W)
        entry_fecha = ttk.Entry(frame_form, width=40)
        entry_fecha.grid(row=1, column=1, pady=5)
        entry_fecha.insert(0, "2026-05-15")
        
        ttk.Label(frame_form, text="Hora (HH:MM):*").grid(row=2, column=0, pady=5, sticky=tk.W)
        entry_hora = ttk.Entry(frame_form, width=40)
        entry_hora.grid(row=2, column=1, pady=5)
        entry_hora.insert(0, "10:00")
        
        ttk.Label(frame_form, text="Motivo:").grid(row=3, column=0, pady=5, sticky=tk.W)
        entry_motivo = ttk.Entry(frame_form, width=40)
        entry_motivo.grid(row=3, column=1, pady=5)
        
        def guardar():
            try:
                fecha_hora = datetime.strptime(f"{entry_fecha.get()} {entry_hora.get()}", "%Y-%m-%d %H:%M")
                self.cita_service.agendar_cita(
                    opciones_mascotas[combo_mascota.get()],
                    1,  # Veterinario por defecto
                    fecha_hora,
                    entry_motivo.get()
                )
                messagebox.showinfo("Éxito", "Cita agendada correctamente")
                self.show_dashboard()
            except ValueError as e:
                messagebox.showerror("Error", str(e))
        
        ttk.Button(self.main_frame, text="Agendar", command=guardar).pack(pady=20)
        ttk.Button(self.main_frame, text="Volver", command=self.show_dashboard).pack()


def main():
    root = tk.Tk()
    app = VetCareApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()