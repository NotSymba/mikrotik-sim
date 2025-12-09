# Soluciones Paso a Paso de las Prácticas (Comandos Linux Estándar)

Este documento detalla cómo resolver las prácticas propuestas utilizando comandos estándar de Linux disponibles en el simulador.

## Práctica 3: VLANs (Capa 2 y vconfig/swconfig)

**Objetivo**: Configurar VLANs.

### Paso 1: Configurar switch hardware (swconfig)
Si la práctica pide configuración de switch chip:
```bash
swconfig dev switch0 vlan 10 set ports "0t 2"
swconfig dev switch0 vlan 20 set ports "0t 3"
swconfig dev switch0 set apply
```

### Paso 2: Crear Interfaces VLAN (Linux)
Si la práctica pide crear interfaces virtuales en el SO:
```bash
vconfig add eth0 10
vconfig add eth0 20
ifconfig eth0.10 192.168.10.1 netmask 255.255.255.0 up
ifconfig eth0.20 192.168.20.1 netmask 255.255.255.0 up
```

### Paso 3: Verificar
```bash
ifconfig
# Debe ver eth0.10 y eth0.20
```

---

## Práctica 5: Routing (Comando route)

**Objetivo**: Enrutamiento estático.

### Paso 1: Configurar IP WAN
```bash
ifconfig eth1 10.0.0.1 netmask 255.255.255.252 up
```

### Paso 2: Añadir Ruta Estática
Para llegar a la red 192.168.50.0/24 vía el router vecino 10.0.0.2:

```bash
route add -net 192.168.50.0 netmask 255.255.255.0 gw 10.0.0.2
```
O usando iproute2:
```bash
ip route add 192.168.50.0/24 via 10.0.0.2
```

### Paso 3: Verificar
```bash
route -n
# ó
ip route
```

---

## Práctica 6: Firewall (iptables)

**Objetivo**: Filtrado de paquetes.

### Paso 1: Bloquear Ping (INPUT DROP)
```bash
iptables -A INPUT -p icmp --icmp-type echo-request -s 0.0.0.0/0 -j DROP
```

### Paso 2: NAT (Masquerade)
```bash
iptables -t nat -A POSTROUTING -o eth1 -j MASQUERADE
```

### Paso 3: Port Forwarding (DNAT)
```bash
iptables -t nat -A PREROUTING -p tcp --dport 80 -i eth1 -j DNAT --to-destination 192.168.1.50:80
```
