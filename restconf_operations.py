import requests
import json

# Desactivar las advertencias de seguridad SSL
requests.packages.urllib3.disable_warnings()

class RESTCONFOperations:
    def __init__(self, ip, usuario, contrasena):
        self.ip = ip
        self.usuario = usuario
        self.contrasena = contrasena
        self.base_url = f"https://{ip}/restconf/data"

    def es_dispositivo_operativo(self):
        try:
            response = requests.get(self.base_url, auth=(self.usuario, self.contrasena), verify=False)
            return response.status_code == 200
        except requests.RequestException as e:
            print(f"Error al verificar el dispositivo: {e}")
            return False

    def obtener_configuracion_running(self):
        api_url = f"{self.base_url}/Cisco-IOS-XE-native:native"
        headers = {"Accept": "application/yang-data+json"}
        return self._realizar_solicitud_get(api_url, headers)

    def obtener_tabla_enrutamiento(self):
        api_url = f"{self.base_url}/Cisco-IOS-XE-routing:routing-state"
        headers = {"Accept": "application/yang-data+json"}
        return self._realizar_solicitud_get(api_url, headers)

    def crear_interfaz(self, nombre_interfaz, descripcion, direccion_ip, mascara):
        api_url = f"{self.base_url}/ietf-interfaces:interfaces/interface={nombre_interfaz}"
        headers = {"Content-Type": "application/yang-data+json"}
        data = {
            "ietf-interfaces:interface": {
                "name": nombre_interfaz,
                "description": descripcion,
                "type": "iana-if-type:ethernetCsmacd",
                "enabled": True,
                "ietf-ip:ipv4": {
                    "address": [
                        {
                            "ip": direccion_ip,
                            "netmask": mascara
                        }
                    ]
                }
            }
        }
        return self._realizar_solicitud_put(api_url, headers, data)

    def borrar_interfaz(self, nombre_interfaz):
        api_url = f"{self.base_url}/ietf-interfaces:interfaces/interface={nombre_interfaz}"
        return self._realizar_solicitud_delete(api_url)

    def crear_ruta(self, destino, mascara, siguiente_salto):
        api_url = f"{self.base_url}/ietf-routing:routing/routing-instance=default/ribs/rib=ipv4/ipv4-routes/static-routes/static"
        headers = {"Content-Type": "application/yang-data+json"}
        data = {
            "ietf-routing:static-routes": {
                "route": [
                    {
                        "destination-prefix": f"{destino}/{mascara}",
                        "next-hop": {
                            "next-hop-address": siguiente_salto
                        }
                    }
                ]
            }
        }
        return self._realizar_solicitud_post(api_url, headers, data)

    def configurar_protocolo_enrutamiento(self, protocolo, instancia, parametros):
        api_url = f"{self.base_url}/ietf-routing:routing/routing-instance={instancia}/routing-protocols/routing-protocol={protocolo}"
        headers = {"Content-Type": "application/yang-data+json"}
        data = {
            "ietf-routing:routing-protocol": parametros
        }
        return self._realizar_solicitud_put(api_url, headers, data)

    def _realizar_solicitud_get(self, url, headers):
        response = requests.get(url, auth=(self.usuario, self.contrasena), headers=headers, verify=False)
        if response.status_code == 200:
            try:
                return response.json()
            except json.JSONDecodeError as e:
                print('Error al decodificar el JSON:', str(e))
                return None
        else:
            print(f"Error: {response.status_code} - {response.reason}")
            print(response.text)
            return None

    def _realizar_solicitud_put(self, url, headers, data):
        response = requests.put(url, auth=(self.usuario, self.contrasena), headers=headers, json=data, verify=False)
        if response.status_code in [200, 201]:
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.reason}")
            print(response.text)
            return None

    def _realizar_solicitud_post(self, url, headers, data):
        response = requests.post(url, auth=(self.usuario, self.contrasena), headers=headers, json=data, verify=False)
        if response.status_code in [200, 201]:
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.reason}")
            print(response.text)
            return None

    def _realizar_solicitud_delete(self, url):
        response = requests.delete(url, auth=(self.usuario, self.contrasena), verify=False)
        if response.status_code == 204:
            return True
        else:
            print(f"Error: {response.status_code} - {response.reason}")
            print(response.text)
            return False