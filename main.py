
import sys
import getpass
from router_sim import Router
from command_parser import CommandParser

def run_interactive(router=None):
    if router is None:
        router = Router()
        
    parser = CommandParser(router)
    
    print(f"OpenWrt {router.firmware} simulation")
    print("Press F1 or type 'help' (not implemented) for help")
    
    # Simulación de Login (Simplificada para root)
    # OpenWrt a veces pide login, a veces drop to root shell en recovery. Haremos login simple.
    while True:
        try:
            login = "root" 
            # In OpenWrt connection usually SSH or Serial console asks for login.
            # We skip simulated login for "console" feel or ask?
            # Let's ask.
            l = input("login as: ")
            if l: login = l
            break
        except KeyboardInterrupt:
           sys.exit(0)

    # Banner OpenWrt
    print("""
  _______                     ________        __
 |       |.-----.-----.-----.|  |  |  |.----.|  |_
 |   -   ||  _  |  -__|     ||  |  |  ||   _||   _|
 |_______||   __|_____|__|__||________||__|  |____|
          |__| W I R E L E S S   F R E E D O M
 -----------------------------------------------------
 OpenWrt 19.07.7, r11306-c4a6851c72
 -----------------------------------------------------
""")
    
    # Bucle de comandos
    while True:
        try:
            # Prompt Style: root@OpenWrt:~#
            prompt_str = f"{login}@OpenWrt:{parser.current_cwd}# "
            
            cmd = input(prompt_str)
            
            if cmd.lower() in ["exit", "logout"]:
                print("Connection closed.")
                break
                
            res = parser.parse(cmd)
            if res:
                print(res)
                
        except KeyboardInterrupt:
            print("\n")
            continue
        except EOFError:
            break

def main():
    run_interactive()

if __name__ == "__main__":
    main()

