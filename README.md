# Mikrotik RB2011 Simulator (OpenWrt/Linux Edition)

A Python-based simulator for the **Mikrotik RB2011UiAS-2HnD-IN** router, configured to emulate an **OpenWrt/Linux** environment. This tool is designed for students and network engineers to practice advanced networking concepts (VLANs, Routing, Firewall) using standard Linux commands without the need for physical hardware.

## 🚀 Features

*   **Linux Root Shell**: Interactive `root@OpenWrt:~#` prompt.
*   **Core Networking Tools**:
    *   `ifconfig`, `ip` (address/route/link)
    *   `route` (static routing)
    *   `vconfig` (802.1Q VLANs)
    *   `brctl` (Linux Bridging)
    *   `iptables` (Firewall/NAT rules simulation)
*   **Hardware Simulation**:
    *   **Switch Chip**: Includes `swconfig` to simulate the Atheros 8327 hardware switch configuration for VLANs.
*   **Lab Scenarios**:
    *   Dedicated scripts to load environments for VLAN, Routing, and Firewall labs.
*   **Zero Dependencies**: Runs with standard Python 3. No external libraries required.

## 📦 Requirements

*   Python 3.6 or newer.
*   (Optional) Git to manage the repository.

## 🛠️ How to Run

### Quick Start (Free Mode)
Open a terminal in the project folder and run:

```bash
python main.py
```

This starts the simulator with a default configuration. You can explore standard Linux commands like `ifconfig`, `ls`, or `cat /etc/openwrt_version`.

### Running Labs (Prácticas)
To load a specific lab environment:

1.  **VLAN Lab**:
    ```bash
    python labs/lab_3_vlan.py
    ```
2.  **Routing Lab**:
    ```bash
    python labs/lab_5_routing.py
    ```
3.  **Firewall Lab**:
    ```bash
    python labs/lab_6_firewall.py
    ```

## 📚 Documentation

*   **[User Guide (GUIA_USUARIO.md)](GUIA_USUARIO.md)**: Detailed manual on how to use the simulator, command reference, and capabilities.
*   **[Lab Solutions (SOLUCIONES_PRACTICAS.md)](SOLUCIONES_PRACTICAS.md)**: Step-by-step solutions for the included PDF labs using the Linux command set.

## 🔧 Supported Commands

| Category | Commands |
|----------|----------|
| **Interfaces** | `ifconfig`, `ip addr`, `ip link` |
| **VLANs** | `vconfig` |
| **Switch** | `swconfig` |
| **Bridges** | `brctl` |
| **Routing** | `route`, `ip route` |
| **Firewall** | `iptables` |
| **System** | `ls`, `cat`, `pwd`, `reboot`, `ping` |

## 📄 License
This project is open source. Feel free to modify and adapt it for your educational needs.
