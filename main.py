#!/usr/bin/env python3
"""
VETCARE - Sistema de Gestión Veterinaria
Punto de entrada principal de la aplicación
"""

import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.main_window import main

if __name__ == "__main__":
    print("🐾 Iniciando VetCare...")
    main()