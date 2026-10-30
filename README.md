# 🐍📡 Netmiko Mock Lab: automatización de redes sin hardware físico

Laboratorio local para probar scripts de **Netmiko** sin necesitar un router o switch Cisco real. Un servidor SSH falso (hecho con **Paramiko**) imita un router Cisco IOS y responde al comando `show running-config`.

## ¿Cómo funciona?

```
┌────────────────────┐   SSH (127.0.0.1:2222)   ┌──────────────────────────┐
│ netmiko_client.py  │ ───────────────────────▶ │ mock_cisco_server.py     │
│ (Netmiko)          │ ◀─────────────────────── │ (Paramiko, "TestRouter") │
└────────────────────┘    running-config        └──────────────────────────┘
```

- `mock_cisco_server.py`: servidor SSH que acepta la autenticación, simula el prompt `Router#` y responde a `terminal width` y `show running-config`.
- `netmiko_client.py`: script con Netmiko (`device_type: cisco_ios`) que se conecta, ejecuta el comando e imprime la salida.

## Requisitos

- Python 3.9+
- `netmiko` y `paramiko` (ver `requirements.txt`)

## Uso

```bash
# 1. (Opcional) entorno virtual
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux / macOS

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Terminal 1: levantar el router simulado
python mock_cisco_server.py

# 4. Terminal 2: ejecutar el cliente
python netmiko_client.py
```

### Salida esperada

```
Building configuration...

Current configuration :
version 16.9
hostname TestRouter
!
interface GigabitEthernet0/0
 ip address 192.168.1.1 255.255.255.0
!
end
```

## Personalizar

Edita la constante `RUNNING_CONFIG` en `mock_cisco_server.py` para simular otras configuraciones, o agrega más ramas `elif` en `handle_client()` para soportar comandos como `show ip interface brief` o `show version`.

## ⚠️ Aviso

Este servidor es **solo para pruebas locales**: acepta cualquier usuario y contraseña y escucha únicamente en `127.0.0.1`. No lo expongas en una red real.

## Stack

Python · Netmiko · Paramiko · VS Code

## Próximos pasos

- [ ] Simular más comandos `show`
- [ ] Soportar modo de configuración (`configure terminal`)
- [ ] Pruebas automáticas con `pytest`
