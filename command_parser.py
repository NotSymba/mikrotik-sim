
import shlex


import shlex

class CommandParser:
    def __init__(self, router):
        self.router = router
        self.current_cwd = "/root"
        
    def parse(self, command_line):
        command_line = command_line.strip()
        if not command_line:
            return None
            
        try:
            parts = shlex.split(command_line)
        except ValueError:
            return "syntax error"
            
        cmd = parts[0]
        args = parts[1:]
        
        if cmd == "ifconfig":
            return self._handle_ifconfig(args)
        elif cmd == "ip":
            return self._handle_ip(args)
        elif cmd == "route":
            return self._handle_route(args)
        elif cmd == "vconfig":
            return self._handle_vconfig(args)
        elif cmd == "brctl":
            return self._handle_brctl(args)
        elif cmd == "swconfig":
            return self._handle_swconfig(args)
        elif cmd == "iptables":
            return self._handle_iptables(args)
        elif cmd == "ping":
            return self._handle_ping(args)
        elif cmd == "cat":
            return self._handle_cat(args)
        elif cmd == "ls":
            return self._handle_ls(args)
        elif cmd == "pwd":
            return self.current_cwd
        elif cmd == "reboot":
            return "Rebooting system..."
        elif cmd == "exit" or cmd == "logout":
            raise EOFError
        else:
            return f"-ash: {cmd}: not found"

    def _handle_ifconfig(self, args):
        # ifconfig [interface] [options]
        # ifconfig eth0 192.168.1.1 netmask 255.255.255.0 up
        if not args:
            return self._format_ifconfig_all()
            
        iface_name = args[0]
        # Check if interface exists
        iface = next((i for i in self.router.interfaces if i.name == iface_name), None)
        
        # If no other args, show single iface
        if len(args) == 1:
            if iface: return self._format_ifconfig_one(iface)
            else: return f"ifconfig: {iface_name}: error fetching interface information: Device not found"

        # Setting configuration?
        if not iface: return f"ifconfig: {iface_name}: error fetching interface information: Device not found"
        
        idx = 1
        while idx < len(args):
            arg = args[idx]
            if arg == "up":
                iface.enabled = True
            elif arg == "down":
                iface.enabled = False
            elif arg == "netmask":
                idx += 1 # Skip mask value for simulation or store it?
                # We store IP as CIDR in router.ip_addresses usually.
                # Simplified: we assume previous arg was IP.
                pass
            elif arg == "hw": # hw ether MAC
                idx += 2
            else:
                # Assume IP address
                # Remove old IP on this iface for simplicity of "ifconfig eth0 <IP>" behavior?
                # or add? Linux usually adds alias if not replacing. 
                # Let's simple: add/replace primary.
                self.router.add_ip_address(arg, iface_name)
            idx += 1
        return None

    def _format_ifconfig_all(self):
        out = []
        for iface in self.router.interfaces:
            out.append(self._format_ifconfig_one(iface))
        return "\n".join(out)

    def _format_ifconfig_one(self, iface):
        out = []
        out.append(f"{iface.name}   Link encap:Ethernet  HWaddr {iface.mac_address}")
        for ip in self.router.ip_addresses:
            if ip['interface'] == iface.name:
                out.append(f"          inet addr:{ip['address'].split('/')[0]}  Mask:255.255.255.0")
        
        flags = "UP BROADCAST RUNNING MULTICAST" if iface.enabled else "BROADCAST MULTICAST"
        out.append(f"          {flags}  MTU:{iface.mtu}  Metric:1")
        out.append("          RX packets:0 errors:0 dropped:0 overruns:0 frame:0")
        out.append("          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0")
        out.append("")
        return "\n".join(out)

    def _handle_ip(self, args):
        # ip [OPTIONS] OBJECT { COMMAND | help }
        if not args: return "Usage: ip [ START | CODE ] OBJECT { COMMAND | help }"
        
        obj = args[0]
        if obj == "addr" or obj == "address" or obj == "a":
             # ip addr add 192.168.1.1/24 dev eth0
             if len(args) > 1 and args[1] == "add":
                 if len(args) < 5: return "Usage: ip addr add IP dev IFACE"
                 ip = args[2]
                 dev_idx = args.index("dev")
                 iface = args[dev_idx+1]
                 return self.router.add_ip_address(ip, iface)
             elif len(args) > 1 and args[1] == "del":
                 # Simplified del
                 return None 
             else:
                 return self._format_ifconfig_all()
        
        elif obj == "link":
             # ip link set eth0 up
             if len(args) >= 4 and args[1] == "set":
                 iface_name = args[2]
                 state = args[3]
                 iface = next((i for i in self.router.interfaces if i.name == iface_name), None)
                 if iface:
                     if state == "up": iface.enabled = True
                     elif state == "down": iface.enabled = False
                 return None
                 
        elif obj == "route":
             # ip route add 192.168.1.0/24 via 10.0.0.1
             if len(args) > 1 and args[1] == "add":
                 target = args[2]
                 gateway = None
                 if "via" in args:
                     desc_idx = args.index("via")
                     gateway = args[desc_idx+1]
                 return self.router.add_route(target, gateway if gateway else "0.0.0.0")
             else:
                 # show routes
                 return self._handle_route([])

        return "ip: Object not implemented"

    def _handle_route(self, args):
        # route add -net 192.168.1.0 netmask 255.255.255.0 gw 10.0.0.1
        # route (show)
        is_show = False
        if not args: is_show = True
        elif args[0].startswith("-"): is_show = True # handle -n
        
        if is_show:
             out = ["Kernel IP routing table", "Destination     Gateway         Genmask         Flags Metric Ref    Use Iface"]
             for r in self.router.routes:
                 out.append(f"{r.dst_address.ljust(15)} {r.gateway.ljust(15)} 255.255.255.0   UG    0      0        0 eth0")
             return "\n".join(out)
        
        if args[0] == "add":
             # Parsing "route add ..." is complex, simplifying: assume last arg is gw or similar?
             # Let's support: route add default gw 192.168.1.1
             if "gw" in args:
                 gw_idx = args.index("gw")
                 gw = args[gw_idx+1]
                 target_idx = args.index("add") + 1
                 # If target is "default", use 0.0.0.0/0 logic or store as default
                 target = args[target_idx]
                 if target == "-net": target = args[target_idx+1]
                 
                 final_target = "0.0.0.0/0" if target == "default" else target
                 return self.router.add_route(final_target, gw)
             
             # Support simple: route add 192.168.1.0/24 gw 1.1.1.1 (non-standard but helpful?)
             # No, stick to "gw" keyword which is standard 'route' syntax
        return "route: invalid syntax"


    def _handle_vconfig(self, args):
        # vconfig add eth0 10
        if not args: return "Usage: vconfig add [interface] [vlan_id]"
        if args[0] == "add":
            if len(args) < 3: return "Usage: vconfig add [interface] [vlan_id]"
            parent = args[1]
            vid = args[2]
            name = f"{parent}.{vid}"
            return self.router.add_interface(name, "vlan", **{"vlan-id": vid})
            
        elif args[0] == "rem":
            if len(args) < 2: return "Usage: vconfig rem [vlan-name]"
            # Remove interface by name lookup needed in router...
            # We implemented remove_interface by index. Let's assume we can map name.
            return None # Stub
        return "vconfig: command not found"

    def _handle_brctl(self, args):
        # brctl addbr br0
        # brctl addif br0 eth0
        if not args: return "Usage: brctl [command]"
        sub = args[0]
        if sub == "addbr":
             if len(args) < 2: return "Usage: brctl addbr <name>"
             return self.router.add_interface(args[1], "bridge")
        elif sub == "addif":
             if len(args) < 3: return "Usage: brctl addif <bridge> <iface>"
             br_name = args[1]
             if_name = args[2]
             # manual linking logic
             br = next((i for i in self.router.interfaces if i.name == br_name), None)
             iface = next((i for i in self.router.interfaces if i.name == if_name), None)
             if br and iface:
                 iface.master_port = br_name
                 br.bridge_ports.append(if_name)
        return None

    def _handle_swconfig(self, args):
        if not args: return "Usage: swconfig dev <dev> [cmd]"
        if args[0] != "dev": return "Usage: swconfig dev <dev> [cmd]"
        return "switch0: ports: 0 1 2 3 4 5 6t\n vlan 1:\n\tports: 0 1 2 3 6t"

    def _handle_iptables(self, args):
        # iptables -A INPUT -p tcp --dport 22 -j ACCEPT
        return None # Silent success for simulation

    def _handle_ping(self, args):
        target = args[0] if args else "unknown"
        return f"PING {target} ({target}): 56 data bytes\n64 bytes from {target}: seq=0 ttl=64 time=0.1 ms\n64 bytes from {target}: seq=1 ttl=64 time=0.1 ms"

    def _handle_cat(self, args):
        if not args: return "cat: usage error"
        f = args[0]
        if f == "/etc/openwrt_version":
            return "19.07.7"
        return f"cat: {f}: No such file or directory"

    def _handle_ls(self, args):
        return "bin  etc  lib  mnt  overlay  proc  rom  root  sbin  sys  tmp  usr  var  www"









