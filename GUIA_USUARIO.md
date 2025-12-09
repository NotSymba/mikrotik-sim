# Guía de Usuario - Simulador Mikrotik RB2011 (Modo Linux)

Bienvenido al simulador de Mikrotik RB2011. Esta herramienta permite realizar prácticas de redes avanzadas (VLAN, Routing, Firewall) simulando un entorno **Linux/OpenWrt** sobre el hardware del router, tal como se utiliza en cursos de administración de redes.

## 1. Instalación y Requisitos

### Requisitos previos
*   Tener instalado **Python 3.6** o superior.
*   No se requieren librerías externas.

### Instalación
Simplemente descargue o descomprima la carpeta del proyecto en su ordenador.

---

## 2. Cómo Iniciar el Simulador

Tiene dos formas de usar el simulador: en modo libre o cargando un entorno de laboratorio específico.

### A. Modo Libre
Arranca el simulador con un router "limpio" (configuración por defecto). Ideal para explorar comandos.

**Comando:**
```bash
python main.py
```

### B. Modo Laboratorio (Prácticas)
Arranca el simulador pre-cargado o preparado para una práctica específica. Use estos scripts si va a realizar los ejercicios de los PDFs.

*   **Práctica 3: VLANs**
    *   Comando: `python labs/lab_3_vlan.py`
    *   Objetivo: Configurar VLANs utilizando `swconfig` y `vconfig`.
*   **Práctica 5: Enrutamiento**
    *   Comando: `python labs/lab_5_routing.py`
    *   Objetivo: Configurar rutas estáticas e interconectar redes.
*   **Práctica 6: Firewall**
    *   Comando: `python labs/lab_6_firewall.py`
    *   Objetivo: Configurar reglas de filtrado con `iptables`.

---

## 3. Interfaz y Uso

Al iniciar, verá un banner de tipo "OpenWrt".
*   **Login**: El usuario por defecto es `root`.
*   **Prompt**: Verá `root@OpenWrt:~#`, indicando que está en una shell de Linux con privilegios de administrador.
*   **Salir**: Escriba `exit` o `logout` para cerrar el simulador.

---

## 4. Referencia de Comandos Soportados

El simulador acepta los siguientes comandos estándar de Linux para redes.

### Gestión de Interfaces
*   **`ifconfig`**: Muestras todas las interfaces activas.
    *   Ejemplo: `ifconfig`
*   **`ifconfig <interfaz> <ip> netmask <mask> up`**: Configura IP y máscara.
    *   Ejemplo: `ifconfig eth0 192.168.1.1 netmask 255.255.255.0 up`
*   **`ip addr add <ip/cidr> dev <interfaz>`**: Alternativa para añadir IPs.
    *   Ejemplo: `ip addr add 10.0.0.1/30 dev eth1`

### VLANs (802.1Q)
*   **`vconfig add <padre> <id>`**: Crea una sub-interfaz VLAN.
    *   Ejemplo: `vconfig add eth0 10` (Crea la interfaz `eth0.10`)
    *   *Nota: Después recuerde configurarle IP con `ifconfig eth0.10 ...`*

### Switch Hardware (Chip Atheros)
Para prácticas que requieren configuración de switch a nivel físico.
*   **`swconfig dev switch0 ...`**: Configuración del switch.
    *   Ejemplo: `swconfig dev switch0 show` (Ver estado)
    *   Ejemplo: `swconfig dev switch0 vlan 10 set ports "0t 2"` (Asignar VLAN 10 al puerto 2 y Trunk al CPU)

### Enrutamiento
*   **`route -n`**: Ver tabla de rutas.
*   **`route add default gw <ip>`**: Añadir puerta de enlace predeterminada.
*   **`route add -net <red> netmask <mask> gw <ip>`**: Añadir ruta estática.
    *   Ejemplo: `route add -net 192.168.50.0 netmask 255.255.255.0 gw 10.0.0.2`

### Bridges (Puentes)
*   **`brctl addbr <nombre>`**: Crear un bridge.
*   **`brctl addif <bridge> <interfaz>`**: Añadir puertos al bridge.
    *   Ejemplo: `brctl addif br0 eth1`

### Firewall
*   **`iptables`**: Se acepta la sintaxis básica para simular reglas.
    *   Ejemplo: `iptables -A INPUT -p icmp -j DROP`

### Otros Comandos Útiles
*   **`ping <host>`**: Simula un ping a una dirección.
*   **`reboot`**: Reinicia el router simulado.
*   **`ls`, `cat`, `pwd`**: Navegación básica de archivos simulados.

---

## 5. Solución de Problemas

*   **"Command not found"**: Asegúrese de estar usando la sintaxis de Linux (`ifconfig`, `route`) y no la de RouterOS (que usa `/ip address print`).
*   **Errores de Python**: Asegúrese de estar ejecutando el comando desde la carpeta raíz del proyecto.
