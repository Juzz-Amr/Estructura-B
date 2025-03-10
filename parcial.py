import re
ip_unica = set()
fechas={}
contador_error = {200 : 0, 300 :0, 400 : 0, 500 :0}
def extractFromRegularExpression(regex, data):
  if data:
    return re.findall(regex, data)
  return None

Log= open("C:\\Users\\306\\Downloads\\log\\access.log", "r")
regex= r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s-\s-\s\[(\d{2}\/\b[a-zA-Z]{3}\b\/\d{4})\:(\d{2}\:\d{2}\:\d{2})\s\+\d{1,4}]\s\"(\b[A-Z]{3,6})\s(\/\S+)\sHTTP\/\d{1}\.\d{1}\"\s(\d{1,3})"
resultado=extractFromRegularExpression(regex, Log.read())

for ip, fecha, hora, metodo, espacio,error in resultado:
    error = int(error)
    
    if error in contador_error:
        contador_error[error]+=1
    if ip not in ip_unica:
        ip_unica.add(ip)
        fechas[ip] = (fecha, hora, metodo, espacio, error)
for ip, (fecha, hora, metodo, espacio, error) in fechas.items():
    print(f"La IP {ip} ya la fecha es {fecha} la hora es {hora}  el modo es {metodo} y el error es {error} ")
    print("\nConteo de códigos de estado HTTP:")
for codigo, cantidad in contador_error.items():
    print(f"Código {codigo}: {cantidad} veces")
