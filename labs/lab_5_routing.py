
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import run_interactive
from router_sim import Router
from command_parser import CommandParser

def start_lab_5():
    print("=== Preparando Entorno para Práctica 5: Enrutamiento ===")
    print("Estado: Reiniciando configuración...")
    router = Router()
    
    # Pre-configuración: Añadir algunas IPs para facilitar el inicio
    print("Aplicando configuración base de IPs en ether1 y ether2...")
    router.add_ip_address("192.168.1.1/24", "ether1")
    router.add_ip_address("10.0.0.1/30", "ether2")
    
    print("Simulador listo. Inicie los ejercicios de Enrutamiento (/ip route).")
    run_interactive(router)

if __name__ == "__main__":
    start_lab_5()
