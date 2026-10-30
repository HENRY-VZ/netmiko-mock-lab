"""Cliente Netmiko que se conecta al router Cisco simulado y descarga la running-config."""
from importlib import import_module

try:
    ConnectHandler = import_module("netmiko").ConnectHandler
except ModuleNotFoundError as exc:
    if exc.name == "netmiko":
        raise SystemExit(
            "Netmiko no está instalado. Ejecuta: python -m pip install netmiko"
        ) from exc
    raise

cisco_device = {
    "device_type": "cisco_ios",
    "ip": "127.0.0.1",
    "port": 2222,
    "username": "admin",
    "password": "password",
}

net_connect = ConnectHandler(**cisco_device)

try:
    output = net_connect.send_command("show running-config")
    print(output)
finally:
    net_connect.disconnect()
