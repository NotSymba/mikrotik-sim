
import sys
import os

# Add parent directory to path to import backend
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import run_interactive
from router_sim import Router

def start_lab_3():
    print("=== Preparando Entorno para Práctica 3: VLAN ===")
    print("Estado: Reiniciando configuración a valores por defecto...")
    router = Router()
    
    # Optional: Pre-configuration specific to VLAN lab if needed.
    # For now, just a clean state is usually what's needed to start.
    
    print("Simulador listo. Inicie los ejercicios de VLAN.")
    run_interactive(router)

if __name__ == "__main__":
    start_lab_3()
