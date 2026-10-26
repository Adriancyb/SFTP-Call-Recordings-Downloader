# SFTP Call Recordings Downloader & Email Reporter

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SSH/SFTP](https://img.shields.io/badge/Protocol-SFTP%20%2F%20SSH-black?style=for-the-badge&logo=openssh&logoColor=white)
![Automation](https://img.shields.io/badge/Focus-Automation%20%26%20ETL-orange?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Portfolio%20%2F%20Sanitized-green?style=for-the-badge)

Herramienta de automatización para la sincronización programada, validación de integridad y descarga de grabaciones telefónicas desde servidores remotos a través del protocolo SFTP/SSH, con despacho automatizado de reportes de estado vía SMTP.

> Nota: Repositorio anonimizado con fines de portfolio y demostración técnica. No contiene credenciales reales, hosts productivos ni datos sensibles.

---

## Arquitectura y Flujo de Trabajo

El script implementa una rutina de ingesta y validación de datos:

```text
[ Servidor Remoto SFTP ]
          │
          ▼  (Autenticación SSH / Paramiko)
[ Inspección de Árbol de Directorios ] ──► Filtrado por fechas
          │
          ▼
[ Descarga Selectiva ] ──────────────────► Evita duplicados en almacenamiento local
          │
          ▼
[ Validación de Integridad ] ───────────► Comparación de nombres y verificación
          │
          ▼
[ Despacho SMTP ] ──────────────────────► Correo con log consolidado (OK / REVISAR)
```
## Características Principales

- **Sincronización incremental:** Comprueba el almacenamiento local antes de transferir archivos, optimizando ancho de banda y tiempo de cómputo.
- **Manejo de directorios:** Navegación recursiva a través de estructuras dinámicas de carpetas organizadas por fecha.
- **Validación de consistencia:** Control cruzado entre archivos remotos y locales para asegurar la completitud de la transferencia.
- **Notificaciones por correo:** Despacho automático de reportes vía SMTP con el resumen operativo del lote procesado.

---

## Stack Tecnológico

- **Lenguaje:** Python 3.9+
- **Conectividad segura:** `paramiko` (cliente SSHv2 y SFTP)
- **Notificaciones:** `smtplib`, `email.mime`
- **Sistema operativo de despliegue:** Linux / Unix

---

## Configuración y Uso

### 1. Clonar el repositorio

```bash
git clone [https://github.com/Adriancyb/SFTP-Call-Recordings-Downloader.git](https://github.com/Adriancyb/SFTP-Call-Recordings-Downloader.git)
cd SFTP-Call-Recordings-Downloader
```
### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```
### 3. Variables de configuración

Definir los parámetros de conexión dentro del script o cargar mediante variables de entorno:

```python
# Conexión SFTP
ip = "192.168.1.50"
puerto = 22
usuario = "usuario_backup"
clave = "contraseña_segura"

# Rutas
ruta_base = "/var/log/recordings"
carpeta_local_root = "./storage"

# Configuración SMTP
smtp_host = "smtp.servidor.com"
smtp_port = 587
smtp_user = "notificaciones@dominio.com"
smtp_pass = "contraseña_correo"
to_email = [
    "responsable@dominio.com"
]
```
### 4. Ejecución

```bash
python automatizacion.py
```
## Roadmap de Mejoras

- [ ] Soporte para configuración mediante archivo `.env` (`python-dotenv`).
- [ ] Validación de integridad mediante hashes criptográficos (`SHA-256`).
- [ ] Sincronización concurrente de múltiples archivos usando `ThreadPoolExecutor`.
- [ ] Rotación y persistencia de logs en disco con la librería estándar `logging`.
