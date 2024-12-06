class Dispositivo:
    def __init__(self, nombre, modelo, capa, interfaces, ips_masks, vlans, servicios):
        self.nombre = nombre
        self.modelo = modelo
        self.capa = capa
        self.interfaces = interfaces
        self.ips_masks = ips_masks
        self.vlans = vlans
        self.servicios = servicios
