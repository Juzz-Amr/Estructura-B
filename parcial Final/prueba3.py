import tarfile, urllib.request , os, re
from datetime import datetime
from collections import defaultdict, Counter

url = "http://log-sharing.dreamhosters.com/SotM34-anton.tar.gz"
Archivo = "SotM34-anton.tar.gz"
if not os.path.exists(Archivo):
    print("Descargando archivo")
    urllib.request.urlretrieve(url, Archivo)

extract_dir = "logs"
if not os.path.exists(extract_dir):
    os.makedirs(extract_dir)
    print("Extrayendo archivos")
    with tarfile.open(Archivo, "r:gz") as tar:
        tar.extractall(path=extract_dir)

def listar_logs(directorio):
    logs = []
    for root, dirs, files in os.walk(directorio):
        for file in files:
            if file.endswith('.log') or 'access' in file or 'error' in file:
                logs.append(os.path.join(root, file))
    return logs

log_files = listar_logs(extract_dir)
print("Archivos de log encontrados:")
for log in log_files:
    print(f"- {log}")

def analisis_simplificado(log_files):
    ip = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    usuario_pattern = r'(usuario|nombre)=([^\s&]+)'
    Fecha = r'\[(\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2})'
    
    ip_contador = Counter()
    USUARIO = Counter()
    ataque = Counter()
    horario = defaultdict(int)
    
    for log_file in log_files:
        try:
            with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    ips = re.search(ip, line)
                    if ips:
                        ip = ips.group()
                        ip_contador[ip] += 1
                    
                    usuarios_encontrados = re.search(user_pattern, line, re.IGNORECASE)
                    if usuarios_encontrados:
                        user = usuarios_encontrados.group(2)
                        USUARIO[user] += 1
                    
                    Fecha_encontrada = re.search(Fecha, line)
                    if Fecha_encontrada:
                        try:
                            dt = datetime.strptime(Fecha_encontrada.group(1), '%d/%b/%Y:%H:%M:%S')
                            hora = dt.hour
                            
                            for Tipo_ataque, pattern in ataque.items():
                                if re.search(pattern, line, re.IGNORECASE):
                                    ataque[Tipo_ataque] += 1
                                    horario[hora] += 1
                                    break
                        except ValueError:
                            pass
        except Exception as e:
            print(f"Error al procesar {log_file}: {str(e)}")
