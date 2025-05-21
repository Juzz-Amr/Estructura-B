import tarfile, requests, json, re, os, urllib.request
from datetime import datetime
from collections import defaultdict, Counter
from time import sleep

IPINFO_TOKEN = 'e346ff7d09fcd8'  
IPINFO_URL = "https://ipinfo.io/{}/json?token={e346ff7d09fcd8}"

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

def obtener_info_ip(ip):
    try:
        response = requests.get(IPINFO_URL.format(ip, IPINFO_TOKEN))
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"Error al consultar IP {ip}: {str(e)}")
        return None

def analizar_logs(log_files):
    ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    fecha_pattern = r'\[(\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2})'
    metodo_pattern = r'"(GET|POST|PUT|DELETE|HEAD|OPTIONS|PATCH)'
    ruta_pattern = r'"(?:GET|POST|PUT|DELETE|HEAD|OPTIONS|PATCH)\s+([^\s"]+)'
    
    resultados = defaultdict(lambda: {"Country": "", "Hacks": []})
    ip_cache = {}  
    
    for log_file in log_files:
        try:
            with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    ip_match = re.search(ip_pattern, line)
                    if not ip_match:
                        continue
                    
                    ip = ip_match.group()
                    
                    fecha_match = re.search(fecha_pattern, line)
                    fecha = fecha_match.group(1) if fecha_match else "Desconocida"
                    
                    metodo_match = re.search(metodo_pattern, line)
                    metodo = metodo_match.group(1) if metodo_match else "Desconocido"
                    
                    ruta_match = re.search(ruta_pattern, line)
                    ruta = ruta_match.group(1) if ruta_match else "Desconocida"
                    
                    if ip not in ip_cache:
                        info_ip = obtener_info_ip(ip)
                        if info_ip:
                            ip_cache[ip] = info_ip.get('country', 'Desconocido')
                        else:
                            ip_cache[ip] = 'Desconocido'
                        sleep(1) 
                    
                    pais = ip_cache[ip]
                    
                    if pais not in resultados:
                        resultados[pais]["Country"] = pais
                    
                    resultados[pais]["Hacks"].append({
                        "fecha": fecha,
                        "método": metodo,
                        "ruta": ruta
                    })
                    
        except Exception as e:
            print(f"Error al procesar {log_file}: {str(e)}")
    
    return resultados

resultados = analizar_logs(log_files)

with open('resultados_hacks.json', 'w', encoding='utf-8') as f:
    json.dump(list(resultados.values()), f, indent=2, ensure_ascii=False)

print("Análisis completado y guardado en resultados_hacks.json")