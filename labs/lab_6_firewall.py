
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import run_interactive
from router_sim import Router

def start_lab_6():
    print("=== Preparando Entorno para Práctica 6: Firewall ===")
    print("Estado: Reiniciando configuración...")
    router = Router()
    
    # Pre-configuración: Interfaces WAN y LAN simuladas
    print("Configurando ether1 como WAN y bridge-lan como LAN...")
    router.add_ip_address("203.0.113.2/24", "ether1") # Public IP simulation
    
    # Create bridge and add ports
    router.add_interface("bridge-lan", "bridge")
    bridge = next(i for i in router.interfaces if i.name == "bridge-lan")
    
    # Add ether2-5 to bridge (manually or via parser logic reuse, doing manual property set for speed)
    for i in range(2, 6):
        iface_name = f"ether{i}"
        iface = next(x for x in router.interfaces if x.name == iface_name)
        iface.master_port = "bridge-lan"
        bridge.bridge_ports.append(iface_name)
        
    router.add_ip_address("192.168.88.1/24", "bridge-lan")
    
    print("Simulador listo. Configure reglas de Firewall y NAT.")
    run_interactive(router)

if __name__ == "__main__":
    start_lab_6()
