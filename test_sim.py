
import sys
from io import StringIO
from router_sim import Router
from command_parser import CommandParser

def run_test(name, command, parser, expected_keywords=[]):
    print(f"\n[TEST] {name}...")
    res = parser.parse(command)
    if not res and expected_keywords:
        print(f"FALLO: No hubo respuesta, se esperaba: {expected_keywords}")
        return False
    
    if res:
        # Check against keywords
        missing = [k for k in expected_keywords if k.lower() not in str(res).lower()]
        if missing:
             print(f"FALLO: Respuesta '{res}' no contiene: {missing}")
             return False
        # Also check error format
        lower_res = str(res).lower()
        if "fallo" in lower_res or "not found" in lower_res or "syntax error" in lower_res:
             print(f"FALLO: Error devuelto: {res}")
             return False

             
    print("PASÓ")
    return True

def main():
    print("=== Iniciando Pruebas de Simulador (Modo Linux) ===")
    router = Router()
    parser = CommandParser(router)

    # 1. Configurar IP
    if not run_test("ifconfig set IP", "ifconfig ether1 192.168.1.1 netmask 255.255.255.0 up", parser): pass
    
    # 2. Verificar IP
    if not run_test("ifconfig show", "ifconfig ether1", parser, ["192.168.1.1", "UP"]): pass
    
    # 3. Routes
    if not run_test("route add", "route add -net 10.0.0.0 netmask 255.0.0.0 gw 192.168.1.254", parser): pass
    if not run_test("route show", "route -n", parser, ["10.0.0.0", "192.168.1.254"]): pass
    
    # 4. VLANs
    if not run_test("vconfig add", "vconfig add ether1 10", parser): pass
    
    # 5. Brctl
    if not run_test("brctl addbr", "brctl addbr br0", parser): pass

    print("\n=== Pruebas Completadas ===")

if __name__ == "__main__":
    main()
