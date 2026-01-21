import os
import paramiko
import smtplib
from email.message import EmailMessage
from datetime import datetime

ip = "0.0.0.0"
puerto = 00
usuario = "admin"
clave = "admin"

ruta_base = "/ruta/base/ejemplo"   
carpeta_local_root ="carpeta/ruta/final"
 


smtp_host = "example@example.com"
smtp_port = 000
smtp_user = "example@example.com"
smtp_pass = "pasword"
to_email = [
    "example@example.com"
]



def enviar_correo(asunto, cuerpo):
    msg = EmailMessage()
    msg["Subject"] = asunto
    msg["From"] = smtp_user
    msg["To"] = to_email
    msg.set_content(cuerpo)

    if smtp_port == 00:
        with smtplib.SMTP_SSL(smtp_host, smtp_port) as server:
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)
    else:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)


def conectar_sftp():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, port=puerto, username=usuario, password=clave)
    sftp = ssh.open_sftp()
    return ssh, sftp


def verificar_carpeta_local(path):
    os.makedirs(path, exist_ok=True)


def listar_safe(sftp, remote_path):
    try:
        return sftp.listdir(remote_path)
    except Exception:
        return []


def es_directorio(sftp, remote_path):
    try:
        return (sftp.stat(remote_path).st_mode & 0o040000) != 0
    except Exception:
        return False


def ruta_remota_por_fecha(fecha) -> str:
    return f"{ruta_base}/{fecha.year:04d}/{fecha.month:02d}/{fecha.day:02d}"


def ruta_local_por_fecha(fecha) -> str:
    return os.path.join(carpeta_local_root, f"{fecha.month:02d}", f"{fecha.day:02d}")


def descargar_carpeta_dia(sftp, remote_day_path, local_day_path, logs, errores):
    verificar_carpeta_local(local_day_path)

    logs.append(f"Ruta remota (día): {remote_day_path}")
    logs.append(f"Ruta local  (día): {local_day_path}")

    nombres = listar_safe(sftp, remote_day_path)
    if not nombres:
        logs.append("No se pudo listar la carpeta remota, no existe o está vacía")
        return 0, 0, True

    archivos = []
    for n in nombres:
        rp = f"{remote_day_path}/{n}"
        if not es_directorio(sftp, rp):
            archivos.append(n)

    total_remoto = len(archivos)
    logs.append(f"Total remoto (archivos): {total_remoto}")

    descargados = []
    nuevos = 0

    for nombre in archivos:
        remoto = f"{remote_day_path}/{nombre}"
        local = os.path.join(local_day_path, nombre)

        if os.path.exists(local):
            descargados.append(nombre)
            continue

        try:
            sftp.get(remoto, local)
            nuevos += 1
            descargados.append(nombre)
        except Exception as e:
            errores.append(f"Error descargando {remoto}: {e}")

    logs.append(f"Nuevos descargados: {nuevos}")

    set_remoto = set(archivos)
    set_local = set(descargados)
    faltan_local = sorted(list(set_remoto - set_local))

    if not faltan_local:
        logs.append("Validacion OK")
        validacion_ok = True
    else:
        logs.append("Validacion NO coincide")
        logs.append(f"Faltan en local: {len(faltan_local)}; ejemplos: {', '.join(faltan_local[:10])}")
        validacion_ok = False

    return total_remoto, nuevos, validacion_ok


def main():
    logs = []
    errores = []
    hoy = datetime.now().date()
    verificar_carpeta_local(carpeta_local_root)

    try:
        ssh, sftp = conectar_sftp()
    except Exception as e:
        enviar_correo(
            "Error Script Grabaciones: no conecta SFTP",
            f"No se pudo conectar a {ip} por SFTP.\n\nError:\n{e}"
        )
        return

    remote_day_path = ruta_remota_por_fecha(hoy)
    local_day_path = ruta_local_por_fecha(hoy)

    total_remoto, nuevos, validacion_ok = descargar_carpeta_dia(
        sftp, remote_day_path, local_day_path, logs, errores
    )

    try:
        sftp.close()
        ssh.close()
    except Exception:
        pass

    estado = "OK" if (validacion_ok and len(errores) == 0) else "REVISAR"
    asunto = f"{estado} Descarga {hoy.isoformat()} Remoto:{total_remoto} Nuevos:{nuevos}"

    cuerpo = []
    cuerpo.append("REPORTE SCRIPT GRABACIONES (SFTP)")
    cuerpo.append("")
    cuerpo.extend(logs)
    cuerpo.append("")
    if errores:
        cuerpo.append("ERRORES")
        cuerpo.extend(errores)

    enviar_correo(asunto, "\n".join(cuerpo))



main()