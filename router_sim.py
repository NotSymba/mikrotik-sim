
class Switch:
    def __init__(self, name, type):
        self.name = name
        self.type = type
        self.vlans = [] # list of dicts {vlan-id, ports}
        self.ports = {} # dict mapping interface_name -> settings {vlan-mode, vlan-header, default-vlan-id}

class Interface:
    def __init__(self, name, type, mtu=1500):
        self.name = name
        self.type = type
        self.mtu = mtu
        self.mac_address = self._generate_mac()
        self.enabled = True
        self.running = False  # Simulación: asumir no conectado por defecto
        self.comment = ""
        # VLAN & Bridge support
        self.vlan_id = None # Para interfaces tipo vlan
        self.master_port = None # Para puertos en un bridge
        self.bridge_ports = [] # Para interfaces tipo bridge, lista de nombres de interfaces miembros
        # Switch Port Config
        self.switch_settings = {"vlan-mode": "disabled", "vlan-header": "leave-as-is", "default-vlan-id": "auto"}


    def _generate_mac(self):
        import random
        # Generar una dirección MAC aleatoria para simulación
        mac = [0x00, 0x0C, 0x29,
               random.randint(0x00, 0x7F),
               random.randint(0x00, 0xFF),
               random.randint(0x00, 0xFF)]
        return ':'.join(map(lambda x: "%02X" % x, mac))

    def __repr__(self):
        flags = ""
        if self.running: flags += "R"
        if not self.enabled: flags += "X"
        extra = ""
        if self.type == "vlan" and self.vlan_id:
            extra = f"vlan-id={self.vlan_id}"
        return f"{flags.ljust(3)} {self.name.ljust(10)} {self.type.ljust(10)} {str(self.mtu).ljust(5)} {self.mac_address} {extra}"

class Route:
    def __init__(self, dst_address, gateway, distance=1):
        self.dst_address = dst_address
        self.gateway = gateway
        self.distance = distance
        self.active = True
        self.dynamic = False
        self.disabled = False

class FirewallRule:
    def __init__(self, chain, action="accept", **matchers):
        self.chain = chain
        self.action = action
        self.matchers = matchers # user-defined dict e.g. src-address, dst-address, protocol, dst-port, src-port, in-interface, out-interface, connection-state
        self.disabled = False
        self.counters = {"packets": 0, "bytes": 0}

    def matches(self, packet):
        # Placeholder for future packet matching logic
        return True


class Router:
    def __init__(self):
        self.model = "RB2011UiAS-2HnD"
        self.serial_number = "HE123456789"
        self.firmware = "6.49.6"
        self.identity = "MikroTik"
        
        # Especificaciones de Hardware
        self.cpu = "MIPS 74Kc V4.12"
        self.cpu_count = 1
        self.cpu_frequency = 600 # MHz
        self.memory = 128 * 1024 * 1024 # 128 MB
        self.hdd = 128 * 1024 * 1024 # 128 MB NAND

        self.interfaces = []
        self._init_interfaces()
        
        self.ip_addresses = []
        self.ip_addresses = []
        self.routes = []
        self.firewall_filter = []
        self.routes = []
        self.firewall_filter = []
        self.firewall_nat = []
        self.ip_pools = []
        self.dhcp_servers = []
        self.dns_settings = {"servers": [], "allow-remote-requests": False}
        self.logs = []
        self.neighbors = [] # neighbors list
        
        self.switches = [
            Switch("switch1", "Atheros-8327"),
            Switch("switch2", "Atheros-8227")
        ]
        
        # OpenWrt UCI Configuration Store (File simulation)
        self.uci_config = {
            "network": {}, 
            "wireless": {},
            "dhcp": {},
            "firewall": {},
            "system": {"system": {"hostname": "OpenWrt", "timezone": "UTC"}}
        }




        
        # Estado de la simulación
        self.uptime = 0

    def _init_interfaces(self):
        # Distribución de puertos RB2011
        # Ether1-5: Gigabit
        for i in range(1, 6):
            self.interfaces.append(Interface(f"ether{i}", "ether", mtu=1500))
        
        # Ether6-10: Fast Ethernet
        for i in range(6, 11):
            self.interfaces.append(Interface(f"ether{i}", "ether", mtu=1500))
            
        # SFP1
        self.interfaces.append(Interface("sfp1", "ether", mtu=1500))
        
        # Wireless
        self.interfaces.append(Interface("wlan1", "wlan", mtu=1500))
        
        # Bridge (a menudo la configuración por defecto tiene un bridge)
        # Empezamos limpio por ahora.

    def add_ip_address(self, address, interface_name):
        if not address or not interface_name:
            return "fallo: dirección e interfaz requeridas"

        # Basic validation
        if not any(iface.name == interface_name for iface in self.interfaces):
            return "fallo: interfaz no encontrada"
        
        try:
           network = address.split('/')[0]
        except:
           network = address

        self.ip_addresses.append({
            "address": address,
            "network": network, 
            "interface": interface_name,
            "dynamic": False,
            "disabled": False
        })
        return None

    def remove_ip_address(self, index):
        if index is None:
            return "fallo: índice requerido"
        try:
            del self.ip_addresses[int(index)]
            return None
        except (IndexError, ValueError):
            return "fallo: índice inválido"

    def add_route(self, dst_address, gateway, distance=1):
        self.routes.append(Route(dst_address, gateway, distance))
        return None

    def remove_route(self, index):
        try:
            del self.routes[int(index)]
            return None
        except (IndexError, ValueError):
            return "fallo: índice inválido"
            
    def add_firewall_rule(self, table, chain, action, **kwargs):
        rule = FirewallRule(chain, action, **kwargs)
        if table == "filter":
            self.firewall_filter.append(rule)
        elif table == "nat":
            self.firewall_nat.append(rule)
        # Verify if action is log, add to log immediately? 
        # In simulation, we might not traffic gen, so logging happens on matching. 
        # But we don't have traffic gen. 
        # So maybe we just log "Rule added" or sim.
        return None
        
    def log_message(self, topics, message):
         import datetime
         ts = datetime.datetime.now().strftime("%H:%M:%S")
         self.logs.append({"time": ts, "topics": topics, "message": message})

    def reset_configuration(self):
         self.interfaces = []
         self._init_interfaces()
         self.ip_addresses = []
         self.routes = []
         self.firewall_filter = []
         self.firewall_nat = []
         self.ip_pools = []
         self.dhcp_servers = []
         self.dns_settings = {"servers": [], "allow-remote-requests": False}
         self.logs = []
         self.log_message("system,info", "Configuration reset by user")
         return "Configuración reseteada. Reiniciando..."

    def add_switch_vlan(self, switch_name, vlan_id, ports):
        # find switch
        sw = next((s for s in self.switches if s.name == switch_name), None)
        if not sw: return "fallo: switch no encontrado"
        sw.vlans.append({"vlan-id": vlan_id, "ports": ports})
        return None

    def remove_switch_vlan(self, switch_name, index):
        sw = next((s for s in self.switches if s.name == switch_name), None)
        if not sw: return "fallo: switch no encontrado"
        try:
             del sw.vlans[int(index)]
             return None
        except: return "fallo: índice inválido"

    def set_switch_port(self, interface_name, vlan_mode=None, vlan_header=None, default_vlan_id=None):
        iface = next((i for i in self.interfaces if i.name == interface_name), None)
        if not iface: return "fallo: interfaz no encontrada"
        
        if vlan_mode: iface.switch_settings["vlan-mode"] = vlan_mode
        if vlan_header: iface.switch_settings["vlan-header"] = vlan_header
        if default_vlan_id: iface.switch_settings["default-vlan-id"] = default_vlan_id
        return None



    def remove_firewall_rule(self, table, index):
        target = self.firewall_filter if table == "filter" else self.firewall_nat
        try:
            del target[int(index)]
            return None
        except (IndexError, ValueError):
            return "fallo: índice inválido"

    def add_ip_pool(self, name, ranges):
        self.ip_pools.append({"name": name, "ranges": ranges})
        return None

    def remove_ip_pool(self, index):
        try:
            del self.ip_pools[int(index)]
            return None
        except:
            return "fallo: error al eliminar pool"

    def add_dhcp_server(self, name, interface, address_pool, disabled=False):
        self.dhcp_servers.append({
            "name": name,
            "interface": interface,
            "address-pool": address_pool,
            "disabled": disabled
        })
        return None

    def remove_dhcp_server(self, index):
        try:
            del self.dhcp_servers[int(index)]
            return None
        except:
            return "fallo: error al eliminar dhcp server"

    def set_dns(self, servers=None, allow_remote=None):
        if servers is not None:
            self.dns_settings["servers"] = servers.split(",")
        if allow_remote is not None:
             self.dns_settings["allow-remote-requests"] = (allow_remote.lower() == "yes")
        return None


    def add_interface(self, name, type, **kwargs):
        # Check uniqueness
        if any(i.name == name for i in self.interfaces):
            return "fallo: ya existe una interfaz con ese nombre"
        
        iface = Interface(name, type)
        if type == "vlan":
             if "vlan-id" in kwargs:
                 iface.vlan_id = kwargs["vlan-id"]
             else:
                 return "fallo: vlan-id requerido"
             if "interface" in kwargs:
                 # In RouterOS VLAN is attached to an interface, logical link
                 # For sim we just keep it as property? Or maybe master?
                 # Let's say vlan is on an interface.
                 pass
        
        if type == "bridge":
             pass # Bridge creation
             
        self.interfaces.append(iface)
        return None

    def remove_interface(self, index):
        try:
            # Prevent removing hardware interfaces?
            iface = self.interfaces[int(index)]
            if iface.type == "ether" or iface.type == "wlan":
                 return "fallo: no se puede eliminar interfaz de hardware"
            del self.interfaces[int(index)]
            return None
        except (IndexError, ValueError):
            return "fallo: índice inválido"

    def get_resource_data(self):
        import time
        # Retorna un diccionario con info de recursos
        return {
            "uptime": "1h2m3s", # Placeholder
            "version": self.firmware,
            "free-memory": f"{self.memory // 1024}KiB",
            "total-memory": f"{self.memory // 1024 // 1024}MiB",
            "cpu": self.cpu,
            "cpu-count": self.cpu_count,
            "cpu-frequency": f"{self.cpu_frequency}MHz",
            "cpu-load": "1%",
            "free-hdd-space": f"{self.hdd // 1024}KiB",
            "total-hdd-space": f"{self.hdd // 1024 // 1024}MiB",
            "architecture-name": "mipsbe",
            "board-name": self.model,
            "platform": "MikroTik"
        }
